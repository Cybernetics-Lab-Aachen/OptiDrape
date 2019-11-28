from PyQt5.QtCore import QThread, pyqtSignal, Qt
import os
import traceback
from drape_object import DrapeTriMesh
import pickle
import openmesh
import numpy as np
import tqdm
import sys, os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class EAThread(QThread):
    pbar2progressSig = pyqtSignal(int)
    ind2visu = pyqtSignal(list)
    dodeepcopy = pyqtSignal(DrapeTriMesh, str)
    updateviewer = pyqtSignal(bool)
    puttext = pyqtSignal(int, list, list, list)

    def __init__(self, args, view, parent):
        super(EAThread, self).__init__(parent=parent)
        self.args = args
        self.finish_deepcopy = False
        self.path_mesh = "../gui/Pyramidenstumpf_P40_35_B412C.obj"
        self.path_expected_node = "../gui/node_expected_useful.p"
        self.node_expected = pickle.load(open(self.path_expected_node, "rb"))
        self.dist_between_nodes_dict = pickle.load(open("../evolAlgo/dist_between_nodes_dict.p", "rb"))
        self.view = view

        DEFAULT_MESH_OPTION = openmesh.Options()
        DEFAULT_MESH_OPTION += openmesh.Options.FaceNormal
        DEFAULT_MESH_OPTION += openmesh.Options.VertexNormal
        DEFAULT_MESH_OPTION += openmesh.Options.FaceColor
        DEFAULT_MESH_OPTION += openmesh.Options.VertexColor
        DEFAULT_MESH_OPTION += openmesh.Options.VertexTexCoord
        DEFAULT_MESH_OPTION += openmesh.Options.FaceTexCoord
        self.mesh = DrapeTriMesh(name="test", has_face=True, viewer_parent=None)

        openmesh.read_mesh(self.mesh, self.path_mesh, DEFAULT_MESH_OPTION)
        self.mesh.update_normals()
        self.mesh.mesh_option_request()
        self.mesh.request_vertex_colors()
        self.mesh.request_face_colors()
        self.mesh.update_viewer()

        self.node_coordinates = []
        self.node_angle = []
        self.face_expected = []

        for node_id in self.node_expected:
            _node_handle = self.mesh.vertex_handle(node_id)

            self.node_coordinates.append([self.mesh.point(_node_handle)[i] for i in range(3)])
            self.node_angle.append(self.angle_between(v1=np.asarray([self.mesh.normal(_node_handle)[i] for i in range(3)]),
                                                 v2=np.array([0, 0, -1])))

        face_vertex_list = self.mesh.viewer.face_vertex_idx_in_np.tolist()
        #print(face_vertex_list)
        for face_map in face_vertex_list:
            for v in face_map:
                if v in self.node_expected:
                    vfi = self.mesh.vf(self.mesh.vertex_handle(v))

                    for fh in vfi:
                        face_id = fh.idx()
                        if face_id not in self.face_expected:
                            self.face_expected.append(face_id)

        self.population = []

        for i in range(5):
            self.population.append(self.mesh.deepcopy(name=str(i)))

    def unit_vector(self, v):
        return v / np.linalg.norm(v)

    def angle_between(self, v1, v2):
        v1_u = self.unit_vector(v1)
        v2_u = self.unit_vector(v2)
        return np.rad2deg(np.arccos(np.clip(np.dot(v1_u, v2_u), -1., 1.)))

    def reset_mesh_color_for_mutation(self, mesh, node_expected, mutated_node=None):
        for vh in mesh.vertices():
            _id = vh.idx()
            if _id in node_expected:
                mesh.set_color(vh, openmesh.Vec4f(0, 1, 0, 1))
            else:
                mesh.set_color(vh, openmesh.Vec4f(0, 0, 1, 1))

        if mutated_node:
            for node in mutated_node.keys():
                mesh.set_color(mesh.vertex_handle(int(node)), openmesh.Vec4f(1, 0, 0, 1))
                for n_node_grp in mutated_node[node]:
                    this_color = np.random.randint(1, 10)
                    this_color = float(this_color / 10)
                    for n_node in n_node_grp:
                        mesh.set_color(mesh.vertex_handle(int(n_node)),
                                       openmesh.Vec4f(1 - this_color, 1 - this_color, 1 - this_color, 1))

    def select_mutation_basis(self, this_mesh, node_expected):
        n_vex = np.random.randint(500, 800)
        node2mutate = []
        node2mutate2color = {}
        # then we pick up the vertex with the id respected to the policy
        # before that, we need to calculate the probibility that a vertex will be sampled

        node_angle_norm = this_mesh.calc_vertex_normal_angle(node_expected=node_expected,
                                                             normalize=True)
        n_iterate = 0
        # print("Num of vex to mutate ", n_vex)
        while len(node2mutate) < n_vex:
            # print("Begin of iterate --------- ", n_iterate)
            n_iterate += 1
            target_vex_id = np.random.choice(node_expected, size=None, p=node_angle_norm)

            this_target_neighbours = []
            n_grp = np.random.randint(5, 12)
            node2mutate.append(target_vex_id)
            # dis_othernodes_to_target_node = {}
            # point_of_target_node = np.array([mesh.point(mesh.vertex_handle(int(target_vex_id)))[i] for i in range(3)])
            # print("selected target mutation vertex: ", target_vex_id)

            neighbouring_nodes_of_target_node = list(self.dist_between_nodes_dict[target_vex_id].keys())
            nearest_8_neighbour_nodes_of_target_node = neighbouring_nodes_of_target_node[:8]
            # print("nearest 8 neighbours of target node: ", nearest_8_neighbour_nodes_of_target_node)

            for grp_i in range(n_grp):
                # print("--- Begin select neighbours in %s grps." % str(n_grp))
                neighbour_grp = []
                num_vertex_needed = n_vex - len(node2mutate)
                if not num_vertex_needed:
                    break
                n_neighbour_vex = np.random.randint(10, 20)
                # print("Neighbours to select: ", n_neighbour_vex)
                if n_neighbour_vex > num_vertex_needed:
                    n_neighbour_vex = num_vertex_needed
                    # print("Neighbours to select normalized: ", n_neighbour_vex)
                # select one of the connected vertex among the 8 neighboring vertexes
                #                  1 2 3
                #                  4 T 5
                #                  6 7 8

                this_neighbour_id = neighbouring_nodes_of_target_node[np.random.randint(0, 8)]

                i = 1
                while this_neighbour_id in node2mutate:
                    this_neighbour_id = neighbouring_nodes_of_target_node[np.random.randint(0, 8 * i)]
                    i += 1

                # print("Target neighbour id: ", this_neighbour_id)
                # we got the id of one vertex around the target vertex, next step
                neighbour_grp.append(this_neighbour_id)
                neighbouring_nodes_of_this_neighbour = list(self.dist_between_nodes_dict[this_neighbour_id].keys())

                for i, neighbour_of_neighbour in enumerate(neighbouring_nodes_of_this_neighbour):
                    if neighbour_grp.__len__() > n_neighbour_vex - 1:
                        break
                    if neighbour_of_neighbour not in node2mutate:  # and neighbour_of_neighbour not in nearest_8_neighbour_nodes_of_target_node:
                        neighbour_grp.append(neighbour_of_neighbour)

                # print("Neighbours selected: ", neighbour_grp)
                # print("Number of Neighbours selected: ", neighbour_grp.__len__())
                node2mutate += neighbour_grp
                this_target_neighbours.append(neighbour_grp)

            # choose a target vertex

            node2mutate2color.update({target_vex_id: this_target_neighbours})
            # print("Current length of node2mutate ", node2mutate.__len__())
        return node2mutate, node2mutate2color

    @staticmethod
    def do_mutate(this_mesh, mutation_basis):
        # we need to define a mutation operation
        x_discount = 1 - np.random.uniform(high=0.001) * np.random.choice([-1, 1], p=[.2, .8])
        z_discount = 1 - np.random.uniform(high=0.004) * np.random.choice([-1, 1], p=[.1, .9])
        for vex in mutation_basis:
            vh = this_mesh.vertex_handle(int(vex))
            point = [this_mesh.point(vh)[i] for i in range(3)]
            this_mesh.set_point(vh, openmesh.Vec3d(point[0] * x_discount, point[1] * x_discount, point[2] * z_discount))

    def run(self):

        #self.moveToThread(QApplication.instance(self).thread())
        #self.pbar2progressSig.emit(80)

        last_population = None
        k_sum_statistics = {}

        iter_num = 10
        with tqdm.tqdm(total=iter_num) as pbar:
            for i in range(iter_num):
                gc_list = []
                new_population = []
                population_mutated_node = []
                for pop_mesh in self.population:
                    new_mutation_basis, node2mutate2color = self.select_mutation_basis(this_mesh=pop_mesh,
                                                                                       node_expected=self.node_expected)

                    self.do_mutate(this_mesh=pop_mesh,
                                   mutation_basis=new_mutation_basis)
                    k_sum, k_abs_sum, _ = pop_mesh.calc_gaussian_curvature()

                    gc_list.append(np.abs(k_sum))
                    population_mutated_node.append(node2mutate2color)

                gc_list_norm = np.asarray(gc_list)

                gc_list_norm = 1 / gc_list_norm

                gc_list_norm = gc_list_norm / gc_list_norm.max()

                gc_list_norm = gc_list_norm / gc_list_norm.sum()

                # we generate a tem dict to select the pop and recolor the mesh

                population_tmp_dict = {}

                for j, gc in enumerate(gc_list_norm):
                    population_tmp_dict.update({gc: [self.population[j], population_mutated_node[j]]})

                selected = []
                if i < iter_num - 1:

                    for old_pop in np.random.choice(a=gc_list_norm, size=5, p=gc_list_norm):
                        #print("Normal")
                        self.finish_deepcopy = False
                        self.mesh_deep_copy = None


                        self.dodeepcopy.emit(population_tmp_dict[old_pop][0],
                                             str(gc_list[gc_list_norm.tolist().index(old_pop)]) + "/" + str(old_pop))

                        while(not self.finish_deepcopy):
                            pass

                        if not self.mesh_deep_copy:
                            print("WORNG")
                            return

                        self.reset_mesh_color_for_mutation(self.mesh_deep_copy, node_expected=self.node_expected,
                                                           mutated_node=population_tmp_dict[old_pop][1])
                        new_population.append(self.mesh_deep_copy)

                        selected.append(gc_list_norm.tolist().index(old_pop))

                    self.population = new_population
                    self.finish_deepcopy = False
                    self.updateviewer.emit(True)
                    while (not self.finish_deepcopy):
                        pass

                else:
                    for ii, pop_ in enumerate(self.population):
                        self.reset_mesh_color_for_mutation(pop_, node_expected=self.node_expected,
                                                           mutated_node=population_mutated_node[ii])
                        pop_.set_name(str(gc_list[ii]) + "/" + str(gc_list_norm[ii]))

                    t = gc_list_norm.tolist()
                    #openmesh.write_mesh(self.population[t.index(max(t))], "./max_fitness_mesh_2.obj")

                # after mutation, we calculate the gc, and select three meshes in
                print()
                print('-', gc_list, '-', gc_list_norm, '-', selected)
                k_sum_statistics.update({i: [gc_list, selected]})

                """
                if False:
                    for pop in new_population:
                        reset_mesh_color_for_mutation(mesh=pop,
                                                      node_expected=node_expected)
                """

                self.ind2visu.emit(self.population)
                self.puttext.emit(i+1, gc_list, gc_list_norm.tolist(), selected)
                self.pbar2progressSig.emit(int((i+1) / iter_num * 100))
                pbar.update()
            #pickle.dump(k_sum_statistics, open("./k_sum_stat_with_sum.p", "wb"))

   # self.exec()





























