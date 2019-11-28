from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import pickle
import openmesh
import random
import scipy
import operator
import numpy as np
from pprint import pprint
from mytest.gaussian_curvature import surface_curvature
from collections import OrderedDict
from Data.drape_object import DrapeTriMesh
from gui.gui_main import *
from gui.viewer.result import Result
import tqdm
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def unit_vector(v):
    return v / np.linalg.norm(v)


def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.rad2deg(np.arccos(np.clip(np.dot(v1_u, v2_u), -1., 1.)))


np.set_printoptions(threshold=sys.maxsize)
app = QApplication(sys.argv)
path_mesh = "../gui/Pyramidenstumpf_P40_35_B412C.obj"
path_expected_node = "../gui/node_expected_useful.p"

node_expected = pickle.load(open(path_expected_node, "rb"))
DEFAULT_MESH_OPTION = openmesh.Options()
DEFAULT_MESH_OPTION += openmesh.Options.FaceNormal
DEFAULT_MESH_OPTION += openmesh.Options.VertexNormal
DEFAULT_MESH_OPTION += openmesh.Options.FaceColor
DEFAULT_MESH_OPTION += openmesh.Options.VertexColor
DEFAULT_MESH_OPTION += openmesh.Options.VertexTexCoord
DEFAULT_MESH_OPTION += openmesh.Options.FaceTexCoord
mesh = DrapeTriMesh(name="test", has_face=True)

openmesh.read_mesh(mesh, path_mesh, DEFAULT_MESH_OPTION)
mesh.update_normals()
mesh.mesh_option_request()
mesh.request_vertex_colors()
mesh.request_face_colors()
mesh.update_viewer()

# try to get the coordinates of the selected nodes
node_coordinates = []
node_angle = []
face_expected = []
for node_id in node_expected:
    _node_handle = mesh.vertex_handle(node_id)

    node_coordinates.append([mesh.point(_node_handle)[i] for i in range(3)])
    node_angle.append(angle_between(v1=np.asarray([mesh.normal(_node_handle)[i] for i in range(3)]),
                                    v2=np.array([0, 0, -1])))

# and then we could sort the coordinates according to z coordinates
face_vertex_list = mesh.viewer.face_vertex_idx_in_np.tolist()

for face_map in face_vertex_list:
    for v in face_map:
        if v in node_expected:
            vfi = mesh.vf(mesh.vertex_handle(v))

            for fh in vfi:
                face_id = fh.idx()
                if face_id not in face_expected:
                    face_expected.append(face_id)

#print(face_expected)


def reset_mesh_color_for_mutation(mesh, node_expected, mutated_node=None):
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
                    mesh.set_color(mesh.vertex_handle(int(n_node)), openmesh.Vec4f(1 - this_color, 1 - this_color, 1 - this_color, 1))


#############################################################################################
#############################################################################################
#############################################################################################
#############################################################################################

#--------------------------------------------Here begins the EA test

population = []

for i in range(5):
    population.append(mesh.deepcopy(name=str(i)))

# we generate a node dist map

"""
dist_between_nodes_dict = {}
for vex_from in node_expected:
    this_vex_dist_dict = {}
    vex_from_point = np.array([mesh.point(mesh.vertex_handle(int(vex_from)))[i] for i in range(3)])
    for vex_to in node_expected:
        vex_to_point = np.array([mesh.point(mesh.vertex_handle(int(vex_to)))[i] for i in range(3)])
        this_vex_dist_dict.update({vex_to: np.linalg.norm(vex_from_point - vex_to_point)})
    this_vex_dist_dict_sorted = OrderedDict(sorted(this_vex_dist_dict.items(), key=operator.itemgetter(1)))
    this_vex_dist_dict_sorted.pop(vex_from, None)
    dist_between_nodes_dict.update({vex_from:  this_vex_dist_dict_sorted})


pickle.dump(dist_between_nodes_dict, open("./dist_between_nodes_dict_car.p", "wb"))

exit()
"""
dist_between_nodes_dict = pickle.load(open("./dist_between_nodes_dict.p", "rb"))


def select_mutation_basis(this_mesh, node_expected):
    global dist_between_nodes_dict
    n_vex = np.random.randint(500, 800)
    node2mutate = []
    node2mutate2color = {}
    # then we pick up the vertex with the id respected to the policy
    # before that, we need to calculate the probibility that a vertex will be sampled

    node_angle_norm = this_mesh.calc_vertex_normal_angle(node_expected=node_expected,
                                                         normalize=True)
    n_iterate = 0
    #print("Num of vex to mutate ", n_vex)
    while len(node2mutate) < n_vex:
        #print("Begin of iterate --------- ", n_iterate)
        n_iterate += 1
        target_vex_id = np.random.choice(node_expected, size=None, p=node_angle_norm)

        this_target_neighbours = []
        n_grp = np.random.randint(5, 12)
        node2mutate.append(target_vex_id)
        # dis_othernodes_to_target_node = {}
        # point_of_target_node = np.array([mesh.point(mesh.vertex_handle(int(target_vex_id)))[i] for i in range(3)])
        # print("selected target mutation vertex: ", target_vex_id)

        neighbouring_nodes_of_target_node = list(dist_between_nodes_dict[target_vex_id].keys())
        nearest_8_neighbour_nodes_of_target_node = neighbouring_nodes_of_target_node[:8]
        # print("nearest 8 neighbours of target node: ", nearest_8_neighbour_nodes_of_target_node)

        for grp_i in range(n_grp):
            #print("--- Begin select neighbours in %s grps." % str(n_grp))
            neighbour_grp = []
            num_vertex_needed = n_vex - len(node2mutate)
            if not num_vertex_needed:
                break
            n_neighbour_vex = np.random.randint(10, 20)
            #print("Neighbours to select: ", n_neighbour_vex)
            if n_neighbour_vex > num_vertex_needed:
                n_neighbour_vex = num_vertex_needed
                #print("Neighbours to select normalized: ", n_neighbour_vex)
            # select one of the connected vertex among the 8 neighboring vertexes
            #                  1 2 3
            #                  4 T 5
            #                  6 7 8

            this_neighbour_id = neighbouring_nodes_of_target_node[np.random.randint(0, 8)]

            i = 1
            while this_neighbour_id in node2mutate:
                this_neighbour_id = neighbouring_nodes_of_target_node[np.random.randint(0, 8 * i)]
                i += 1

            #print("Target neighbour id: ", this_neighbour_id)
            # we got the id of one vertex around the target vertex, next step
            neighbour_grp.append(this_neighbour_id)
            neighbouring_nodes_of_this_neighbour = list(dist_between_nodes_dict[this_neighbour_id].keys())

            for i, neighbour_of_neighbour in enumerate(neighbouring_nodes_of_this_neighbour):
                if neighbour_grp.__len__() > n_neighbour_vex - 1:
                    break
                if neighbour_of_neighbour not in node2mutate: # and neighbour_of_neighbour not in nearest_8_neighbour_nodes_of_target_node:
                    neighbour_grp.append(neighbour_of_neighbour)

            #print("Neighbours selected: ", neighbour_grp)
            #print("Number of Neighbours selected: ", neighbour_grp.__len__())
            node2mutate += neighbour_grp
            this_target_neighbours.append(neighbour_grp)

        # choose a target vertex

        node2mutate2color.update({target_vex_id: this_target_neighbours})
        #print("Current length of node2mutate ", node2mutate.__len__())
    return node2mutate, node2mutate2color


def do_mutate(this_mesh, mutation_basis):
    # we need to define a mutation operation
    x_discount = 1 - np.random.uniform(high=0.001) * np.random.choice([-1, 1], p=[.2, .8])
    z_discount = 1 - np.random.uniform(high=0.004) * np.random.choice([-1, 1], p=[.1, .9])
    for vex in mutation_basis:
        vh = this_mesh.vertex_handle(int(vex))
        point = [this_mesh.point(vh)[i]for i in range(3)]
        this_mesh.set_point(vh, openmesh.Vec3d(point[0] * x_discount, point[1] * x_discount, point[2] * z_discount))


last_population = None
k_sum_statistics = {}

def run_ea():
    iter_num = 10
    global population, node_expected, last_population, k_sum_statistics
    with tqdm.tqdm(total=iter_num) as pbar:
        for i in range(iter_num):
            gc_list = []
            new_population = []
            population_mutated_node = []
            for pop_mesh in population:
                new_mutation_basis, node2mutate2color = select_mutation_basis(this_mesh=pop_mesh,
                                                                              node_expected=node_expected)
                do_mutate(this_mesh=pop_mesh,
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
                population_tmp_dict.update({gc: [population[j], population_mutated_node[j]]})

            selected = []
            if i < iter_num - 1:
                if i == 500:
                    for pop_ in population:
                        pop_.update_viewer()
                        pop_.viewer.update_mesh_info(info=pop_.name + '_at_500')
                        pop_.viewer.show()

                for old_pop in np.random.choice(a=gc_list_norm, size=5, p=gc_list_norm):
                    mesh_deep_copy = population_tmp_dict[old_pop][0].deepcopy(name=str(gc_list[gc_list_norm.tolist().index(old_pop)]) + "/" + str(old_pop))
                    reset_mesh_color_for_mutation(mesh_deep_copy, node_expected=node_expected, mutated_node=population_tmp_dict[old_pop][1])
                    new_population.append(mesh_deep_copy)
                    selected.append(gc_list_norm.tolist().index(old_pop))
                population = new_population

            else:
                for ii, pop_ in enumerate(population):
                    reset_mesh_color_for_mutation(pop_, node_expected=node_expected,
                                                  mutated_node=population_mutated_node[ii])
                    pop_.set_name(str(gc_list[ii]) + "/" + str(gc_list_norm[ii]))

                t = gc_list_norm.tolist()
                openmesh.write_mesh(population[t.index(max(t))], "./max_fitness_mesh_2.obj")

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

            pbar.update()
        pickle.dump(k_sum_statistics, open("./k_sum_stat_with_sum.p", "wb"))


#print("Total length of node2mutate ", node2mutate.__len__())


"""
for node2mutate in node2mutate2color.keys():
    mesh.set_color(mesh.vertex_handle(int(node2mutate)), openmesh.Vec4f(1, 0, 0, 1))
    for neighbour_node2mutate in node2mutate2color[node2mutate]:
        mesh.set_color(mesh.vertex_handle(int(neighbour_node2mutate)), openmesh.Vec4f(0, 1, 0, 1))
"""

"""
for faceid in face_expected:
    fh = mesh.face_handle(faceid)
    print(mesh.normal(fh))
    mesh.set_color(fh, openmesh.Vec4f(0, 0, 1, 1))
"""


run_ea()

reset_mesh_color_for_mutation(mesh=mesh, node_expected=node_expected)
mesh.update_viewer()
#mesh.viewer.update_mesh_info()
#mesh.viewer.show()
""""""

# visu result

tool = DrapeTool()

result = Result(parent=tool.tab_result)

result.tabWidget.addTab(mesh.viewer, "Original Mesh")
for index, pop in enumerate(population):
    pop.update_viewer()
    #pop.viewer.update_mesh_info(info=pop.name)
    #pop.viewer.show()
    result.tabWidget.addTab(pop.viewer, "Individual %s" % str(index))


from Data.fit_data import *
import matplotlib.pyplot as plt

iter_500_pop_ave = []
iter_500_var = []
iter_500_max = []

for iter in range(len(k_sum_statistics)):
    #iter_500_sorted_population.append(sorted(k_sum_statistics[iter][0], reverse=True))
    iter_500_pop_ave.append(np.average(k_sum_statistics[iter][0]))
    iter_500_max.append(np.max(k_sum_statistics[iter][0]))
    iter_500_var.append(np.sqrt(np.std(k_sum_statistics[iter][0])))

for iteration in k_sum_statistics.keys():
    result.tB_text.append("Iteration %s" % str(iteration))
    result.tB_text.append("- Curvature: %s" % str(k_sum_statistics[iteration][0]))
    result.tB_text.append("- Selected: %s" % str(k_sum_statistics[iteration][1]))
    result.tB_text.append("- Ave. Curvature: %s" % str(iter_500_pop_ave[iteration]))
    result.tB_text.append("- Std. Curvature: %s" % str(iter_500_var[iteration]))


plot_figure = Figure()
plot_canvas = FigureCanvas(plot_figure)

iter_500_pop_ave = np.asarray(iter_500_pop_ave)
#iter_500_pop_ave = 1 / iter_500_pop_ave
iter_500_pop_ave = iter_500_pop_ave / iter_500_pop_ave.max()
iter_500_pop_ave = iter_500_pop_ave / iter_500_pop_ave.sum()
print(iter_500_pop_ave)
print(list(range(len(iter_500_pop_ave))))
_data_reg_func = fitted_data_func(fit_data(x=list(range(len(iter_500_pop_ave))), y=iter_500_pop_ave.tolist(), deg=3))

ax = plot_figure.add_subplot(111)

ax.plot(np.arange(len(iter_500_pop_ave)), iter_500_pop_ave, 'bo', label="Average gaussian curvature")
ax.plot(np.arange(1000), _data_reg_func(np.arange(1000)), 'r-', label="Approximation of average gaussian curvature")
ax.axis([0, 1000, min(iter_500_pop_ave), max(iter_500_pop_ave)])
ax.grid(True, linewidth=1)
ax.set_xlabel('Iteration')
ax.set_xlabel('Average gaussian curvature')
legend = ax.legend(loc='upper right', shadow=True)
ax.set_xticks(np.arange(0, 1001, 30))

result.plot_layout.addWidget(plot_canvas)
tool.tab_result.tB_manager.addItem(result, "P280E")
tool.show()



exit(app.exec())
#print(node_angle)


#print(a, b)

