from openmesh import *

import openmesh


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
from OpenGL.GLUT.freeglut import *
from OpenGL.arrays import vbo
import math, time, sys
import numpy as np


TRACKBALLradius = 0.6


class QGLViewerWidget(QOpenGLWidget):
    def __init__(self, parent):
        super(QOpenGLWidget, self).__init__(parent=parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAcceptDrops(True)
        self.setCursor(Qt.PointingHandCursor)
        self._n_draw_modes = 0
        self._action_dict = dict()

        self._popup_menu = QMenu(self)
        self._draw_modes_group = QActionGroup(self)

        self._draw_modes_group.pyqtConfigure(triggered=self.slotDrawMode)

        self._modelview_matrix = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        self._projection_matrix = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

        self._draw_mode = 0
        self._draw_mode_names = []

        self.radius = 0
        self.center = [0, 0]
        self._last_point_2D = QPoint(0, 0)
        self._last_point_3D = Vec3f(0, 0, 0)
        self._last_point_ok = True

        a = self.add_draw_mode("Wireframe")
        a.setShortcut(QKeySequence(Qt.Key_W))
        a = self.add_draw_mode("Solid Flat")
        a.setShortcut(QKeySequence(Qt.Key_F))
        a = self.add_draw_mode("Solid Smooth")
        a.setShortcut(QKeySequence(Qt.Key_S))
        a.setChecked(True)
        self._nomode = False

        self.slotDrawMode(a)

    def setDefaultMaterial(self):
        mat_a = np.array([0.1, 0.1, 0.1, 1.0], dtype=np.float32)
        mat_d = np.array([0.7, 0.7, 0.5, 1.0], dtype=np.float32)
        mat_s = np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)
        shine = 120.0

        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_a)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_d)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_s)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, [120.0])

    def setDefaultLight(self):
        pos0 = np.array([0.1,  0.1, -0.02, 0.0], dtype=np.float32)
        pos1 = np.array([-0.1,  0.1, -0.02, 0.0], dtype=np.float32)
        pos2 = np.array([0.0,  0.0,  0.1,  0.0], dtype=np.float32)
        col0 = np.array([0.7,  0.7,  0.8,  1.0], dtype=np.float32)
        col1 = np.array([0.8,  0.7,  0.7,  1.0], dtype=np.float32)
        col2 = np.array([1.0,  1.0,  1.0,  1.0], dtype=np.float32)


        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, pos0)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, col0)
        glLightfv(GL_LIGHT0, GL_SPECULAR, col0)

        glEnable(GL_LIGHT1)
        glLightfv(GL_LIGHT1, GL_POSITION, pos1)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, col1)
        glLightfv(GL_LIGHT1, GL_SPECULAR, col1)

        glEnable(GL_LIGHT2)
        glLightfv(GL_LIGHT2, GL_POSITION, pos2)
        glLightfv(GL_LIGHT2, GL_DIFFUSE, col2)
        glLightfv(GL_LIGHT2, GL_SPECULAR, col2)

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glDisable(GL_DITHER)
        glEnable(GL_DEPTH_TEST)

        self.setDefaultMaterial()

        glLoadIdentity()
        self.setDefaultLight()

        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogfv(GL_FOG_COLOR, np.array([0.3, 0.3, 0.4, 1.0]))
        glFogf(GL_FOG_DENSITY, 0.35)
        glHint(GL_FOG_HINT, GL_DONT_CARE)
        glFogf(GL_FOG_START, 5.0)
        glFogf(GL_FOG_END, 25.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self._modelview_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        self.set_scene_pos(Vec3f(0.0, 0.0, 0.0), 1.0)

    def resizeGL(self, w, h):
        self.update_projection_matrix()
        glViewport(0, 0, w, h)
        self.update()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadMatrixd(self._projection_matrix)
        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixd(self._modelview_matrix)
        if self._draw_mode:
            assert(self._draw_mode <= self._n_draw_modes)
            self.draw_scene(self._draw_mode_names[self._draw_mode - 1])

    def draw_scene(self, draw_mode):
        if draw_mode is "Wireframe":
            glDisable(GL_LIGHTING)
            glutWireTeapot(0.5)
        elif draw_mode is "Solid Flat":
            glEnable(GL_LIGHTING)
            glShadeModel(GL_FLAT)
            glutSolidTeapot(0.5)
        elif draw_mode is "Solid Smooth":
            glEnable(GL_LIGHTING)
            glShadeModel(GL_SMOOTH)
            glutSolidTeapot(0.5)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton and event.buttons() == Qt.RightButton:
            self._popup_menu.exec(QCursor.pos())
        else:
            self._last_point_2D = event.pos()
            self._last_point_ok = self.map_to_sphere(self._last_point_2D, self._last_point_3D)

    def mouseMoveEvent(self, event):
        newPoint2D = event.pos()
        newPoint3D = Vec3f(0, 0, 0)
        newPoint_hitSphere = self.map_to_sphere(newPoint2D, newPoint3D)
        dx = newPoint2D.x() - self._last_point_2D.x()
        dy = newPoint2D.y() - self._last_point_2D.y()
        w = self.widthMM()
        h = self.heightMM()
        self.makeCurrent()

        if (event.buttons() == (Qt.LeftButton + Qt.MidButton)) or \
            (event.buttons() == Qt.LeftButton and event.modifiers() == Qt.ControlModifier):
            value_y = self.radius * dy * 3 / h
            self.translate([0, 0, value_y])
        elif event.buttons() == Qt.MidButton or \
            (event.buttons() == Qt.LeftButton and event.modifiers() == Qt.AltModifier):
            z = - (self._modelview_matrix[0, 2]*self.center[0] +
                   self._modelview_matrix[1, 2]*self.center[1] +
                   self._modelview_matrix[2, 2]*self.center[2] +
                   self._modelview_matrix[3, 2])\
                  /\
                  (self._modelview_matrix[0, 2]*self.center[0] +
                   self._modelview_matrix[1, 2]*self.center[1] +
                   self._modelview_matrix[2, 2]*self.center[2] +
                   self._modelview_matrix[3, 2])
            aspect = w / h
            near_plane = 0.01 * self.radius
            top = np.tan(45.0 / 2.0 * math.pi / 180.0) * near_plane
            right = aspect * top

            self.translate([2.0 * dx / w * right / near_plane * z,
                            -2.0 * dy / h * top / near_plane * z,
                            0.0])

        elif event.buttons() == Qt.LeftButton:

            if self._last_point_ok:
                newPoint_hit_Sphere = self.map_to_sphere(newPoint2D, newPoint3D)
                if newPoint_hit_Sphere:
                    axis = self._last_point_3D % newPoint3D
                    if axis.sqrnorm() < 1e-7:
                        axis = Vec3f(1, 0, 0)
                    else:
                        axis.normalize()

                    d = self._last_point_3D - newPoint3D
                    t = .5 * d.norm() / TRACKBALLradius
                    if t < -1.0:
                        t = -1.0
                    elif t > 1.0:
                        t = 1.0
                    phi = 2 * math.asin(t)
                    angle = phi * 180 / math.pi
                    self.rotate(axis, angle)
        self._last_point_2D = newPoint2D
        self._last_point_3D = newPoint3D
        self._last_point_ok = newPoint_hitSphere
        self.update()

    def mouseReleaseEvent(self, event):
        self._last_point_ok = False

    def wheelEvent(self, event):
        d = - event.angleDelta().y() / 360 * self.radius
        self.translate(np.array([0, 0, d]))
        self.update()
        event.accept()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Print:
            self.slotSnapshot()
        elif event.key() == Qt.Key_H:
            pass
            """
            std::cout << "Keys:\n";
            std::cout << "  Print\tMake snapshot\n";
            std::cout << "  C\tenable/disable back face culling\n";
            std::cout << "  F\tenable/disable fog\n";
            std::cout << "  I\tDisplay information\n";
            std::cout << "  N\tenable/disable display of vertex normals\n";
            std::cout << "  Shift N\tenable/disable display of face normals\n";
            std::cout << "  Shift P\tperformance check\n";
            """
        elif event.key() == Qt.Key_C:
            if glIsEnabled(GL_CULL_FACE):
                glDisable(GL_CULL_FACE)
                # TODO: Throw out sth
            else:
                glEnable(GL_FOG)
            self.update()

        elif event.key() == Qt.Key_I:
            pass
            """"""
        elif event.key() == Qt.Key_O:
            if event.modifiers() & Qt.ShiftModifier:
                fps = self.performance()
                print(fps)

        elif event.key() == Qt.Key_Escape or event.key() == Qt.Key_Q:
            qApp.quit()

        event.ignore()

    def translate(self, trans):
        self.makeCurrent()
        glLoadIdentity()
        glTranslated(trans[0], trans[1], trans[2])
        glMultMatrixd(self._modelview_matrix)
        self._modelview_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)

    def rotate(self, axis, angle):

        t = np.array([self._modelview_matrix[0, 0]*self.center[0] +
                      self._modelview_matrix[1, 0]*self.center[1] +
                      self._modelview_matrix[2, 0]*self.center[2] +
                      self._modelview_matrix[3, 0],
                      self._modelview_matrix[0, 1]*self.center[0] +
                      self._modelview_matrix[1, 1]*self.center[1] +
                      self._modelview_matrix[2, 1]*self.center[2] +
                      self._modelview_matrix[3, 1],
                      self._modelview_matrix[0, 2]*self.center[0] +
                      self._modelview_matrix[1, 2]*self.center[1] +
                      self._modelview_matrix[2, 2]*self.center[2] +
                      self._modelview_matrix[3, 2]])

        self.makeCurrent()
        glLoadIdentity()
        glTranslatef(t[0], t[1], t[2])
        glRotated(angle, axis[0], axis[1], axis[2])
        glTranslatef(-t[0], -t[1], -t[2])
        glMultMatrixd(self._modelview_matrix)
        self._modelview_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)

    def map_to_sphere(self, v2D, v3D):
        xval =  (2.0 * v2D.x() - self.width()) / self.width()
        yval = -(2.0 * v2D.y() - self.height()) / self.height()
        x2y2 = xval*xval + yval*yval
        rsqr = TRACKBALLradius * TRACKBALLradius
        v3D[0] = xval
        v3D[1] = yval
        if x2y2 < 0.5 * rsqr:
            v3D[2] = np.sqrt(rsqr - x2y2)
        else:
            v3D[2] = 0.5 * rsqr / np.sqrt(x2y2)
        return True

    def update_projection_matrix(self):
        self.makeCurrent()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, self.width()/self.height(), 0.01 * self.radius, 1000.0 * self.radius)
        self._projection_matrix = glGetDoublev(GL_PROJECTION_MATRIX)
        glMatrixMode(GL_MODELVIEW)

    def view_all(self):
        self.translate(np.array( [-(self._modelview_matrix[0, 0]*self.center[0] +
                                    self._modelview_matrix[1, 0]*self.center[1] +
                                    self._modelview_matrix[2, 0]*self.center[2] +
                                    self._modelview_matrix[3, 0]),
                                  -(self._modelview_matrix[0, 1]*self.center[0] +
                                    self._modelview_matrix[1, 1]*self.center[1] +
                                    self._modelview_matrix[2, 1]*self.center[2] +
                                    self._modelview_matrix[3, 1]),
                                  -(self._modelview_matrix[0, 2]*self.center[0] +
                                    self._modelview_matrix[1, 2]*self.center[1] +
                                    self._modelview_matrix[2, 2]*self.center[2] +
                                    self._modelview_matrix[3, 2] +
                                    3.0*self.radius)]))

    def set_scene_pos(self, cog, radius):
        self.center = cog
        self.radius = radius * 150
        glFogf(GL_FOG_START, 1.5 * radius)
        glFogf(GL_FOG_END, 3.0 * radius)
        self.update_projection_matrix()
        self.view_all()

    def add_draw_mode(self, _str):
        self._n_draw_modes += 1
        self._draw_mode_names.append(_str)

        _act = QAction(self.tr(_str), self)

        _act.setCheckable(True)
        _act.setData(self._n_draw_modes)

        self._draw_modes_group.addAction(_act)
        self._popup_menu.addAction(_act)

        self.addAction(_act, _str)

        return _act

    def addAction(self, act, name):
        self._action_dict[name] = act
        super(QGLViewerWidget, self).addAction(act)

    def removeAction(self, act):
        if type(act) is not str:
            for action_key in self._action_dict.keys():
                if act == self._action_dict[action_key]:
                    self._action_dict.pop(action_key)
                    break

            self._popup_menu.removeAction(act)
            self._draw_modes_group.removeAction(act)
            super(QGLViewerWidget, self).removeAction(act)
        else:
            try:
                act_to_remove = self._action_dict[name]
                self._action_dict.pop(name)
                super(QGLViewerWidget, self).removeAction(act_to_remove)
            except ValueError:
                pass

    def findAction(self, name):
        return self._action_dict.get(name, None)

    def del_draw_mode(self, s):
        actions = self._popup_menu.actions()

        for action in self._popup_menu.actions():
            if action.text() == s:
                self._popup_menu.removeAction(action)

    def slotDrawMode(self, mode):
        self._draw_mode = mode.data()
        self.update()
        #self.update()

    def performance(self):
        self.setCursor(Qt.WaitCursor)
        self.makeCurrent()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        frames = 60.0
        angle = 360.0 / frames

        total_time = 0
        glFinish()
        for axis in [Vec3f(1, 1, 1), Vec3f(1, 1, 0), Vec3f(0, 1, 1)]:
            start = time.clock()
            for i in range(int(frames)):
                self.rotate(axis, angle)
                self.paintGL()
                self.swapBuffers()

            total_time += time.clock() - start
            QApplication.processEvents()

        glFinish()

        glPopMatrix()
        self.update()

        fps = (3.0 * frames) / total_time

        self.setCursor(Qt.PointingHandCursor)

        return 'FPS: ' + str(int(fps))

    def slotSnapshot(self):
        image = QImage()
        w, h = self.width(), self.height()
        buffer = GLenum(GL_BACK)
        fbuffer = []
        try:

            QApplication.processEvents()
            self.makeCurrent()
            self.update()
            glFinish()

            glReadBuffer(buffer)
            glPixelStorei(GL_PACK_ALIGNMENT, 1)
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            self.paintGL()
            glReadPixels(0, 0, w, h, GL_RGB, GL_UNSIGNED_BYTE, array=fbuffer)

            for y in range(h):
                for x in range(w):
                    offset = 3 * (y * w + x)
                    image.setPixel(x, h-y-1, qRgb(fbuffer[offset],
                                                  fbuffer[offset+1],
                                                  fbuffer[offset+2]))

            name = "snapshot-" + QDateTime.currentDateTime().toString("yyMMddhhmmss")
            image.save(name, "PNG")

        except:
            pass

    def current_draw_mode(self):
        if self._draw_mode:
            print("current_Draw_Mode: %s" % self._draw_mode_names[self._draw_mode - 1])
            return self._draw_mode_names[self._draw_mode - 1]
        else:
            return self._nomode

    def getradius(self):
        return self.radius

    def get_modelview_matrix(self):
        return self._modelview_matrix

    def get_projection_matrix(self):
        return self._projection_matrix


class MeshViewerWidgetT(QGLViewerWidget):
    def __init__(self, parent=None):
        super(MeshViewerWidgetT, self).__init__(parent=parent)
        self._f_strips = False
        self._tex_id = 0
        self._tex_mode = GL_MODULATE
        self._strips = None
        self._mesh = openmesh.PolyMesh()
        self._opt = None
        self.radius = 0
        self._fp_normal_base = openmesh.FPropHandle()
        self._show_vnormals = False
        self._show_fnormals = False
        self._use_color = False
        a = self.add_draw_mode('Points')
        a.setShortcut(QKeySequence(Qt.Key_P))
        self.add_draw_mode('Hidden-Line')
        self._mesh_raw_dict = dict()

        self._vnormal_gl_list = None
        self._fnormal_gl_list = None

    def set_mesh(self, new_mesh, opt):
        self._mesh = new_mesh
        self._opt = opt
        # check options
        if self._opt.check(openmesh.Options.FaceNormal):
            self._mesh.update_face_normals()

        if self._opt.check(Options.VertexNormal):
            self._mesh.update_vertex_normals()

        if self._opt.check(Options.VertexColor):
            a = self.add_draw_mode('Colored Vertices')
            a.setShortcut(QKeySequence(Qt.Key_C))
        else:
            self._mesh.release_vertex_colors()

        if self._opt.check(Options.FaceColor):
            self.add_draw_mode('Solid Colored Faces')
            self.add_draw_mode('Smooth Colored Faces')
        else:
            self._mesh.request_face_colors()

        # compute center and radius and fill data holder as dict

        bbMin = openmesh.Vec3f(100, 100, 100)
        bbMax = openmesh.Vec3f(0, 0, 0)
        v = openmesh.TriMesh.Normal()

        self._mesh.add_property(self._fp_normal_base)

        _vertices = []
        _vertices_normals = []
        _vertices_color = []
        _vertices_tex_2D = []
        _vh = []

        for vh in self._mesh.vertices():
            _point = self._mesh.point(vh)
            _vh.append(vh)
            _vertices.append([_point[0], _point[1], _point[2]])
            if self._mesh.has_vertex_normals():
                _vertices_normals.append([self._mesh.normal(vh)[0], self._mesh.normal(vh)[1], self._mesh.normal(vh)[2]])
            if self._mesh.has_vertex_colors():
                #vertices_color.append([self._mesh.color(vh)[0], self._mesh.color(vh)[1], self._mesh.color(vh)[2]])
                pass
            if self._mesh.has_vertex_texcoords2D():
                _vertices_tex_2D.append([self._mesh.texcoord2D(vh)[0], self._mesh.texcoord2D(vh)[1]])
            bbMin.minimize(openmesh.Vec3f(_point[0], _point[1], _point[2]))
            bbMax.maximize(openmesh.Vec3f(_point[0], _point[1], _point[2]))

        self._mesh_raw_dict.update({'v': np.array(_vertices, dtype=np.float32),
                                    'vn': np.array(_vertices_normals, dtype=np.float32), 'vh':_vh,
                                     #'vc': np.array(_vertices_color, dtype=np.float32),
                                    'vc': np.random.rand(self._mesh.n_vertices(), 3),
                                    'vt2D': np.array(_vertices_tex_2D, dtype=np.float32)})

        _face_vertices_idx = []
        _face_normals = []
        _fh = []

        for fh in self._mesh.faces():
            if self._mesh.has_face_normals():
                _face_normals.append([self._mesh.normal(fh)[0], self._mesh.normal(fh)[1], self._mesh.normal(fh)[2]])
            _vh_idx = []
            _fh.append(fh)
            v = openmesh.TriMesh.Point(0, 0, 0)
            for fv in self._mesh.fv(fh):
                _vh_idx.append(fv.idx())
                if fv.is_valid() and self._mesh.has_face_normals():
                    v += self._mesh.point(fv)
            _face_vertices_idx.append(_vh_idx)
            v *= 1.0 / 3.0
            self._mesh.set_property(self._fp_normal_base, fh, v)

        self._mesh_raw_dict.update({'fn': np.array(_face_normals, dtype=np.float32), 'fh': _fh,
                                      'fv_idx': np.array(_face_vertices_idx, dtype=np.int32)})

        # display first impression
        self.set_scene_pos(cog=(bbMin + bbMax) * 0.5,
                           radius=(bbMin - bbMax).norm() * 0.5)

        self._normal_scale = (bbMax - bbMin).min() * 0.1

        print("%s Vertices, %s edges, %s faces" % (str(self._mesh.n_vertices()), str(self._mesh.n_edges()), str(self._mesh.n_faces())))

        # create vertex buffer object in Server side

        self._vbo_vertices = vbo.VBO(self._mesh_raw_dict['v'])

        self._vbo_fv_idx = vbo.VBO(self._mesh_raw_dict['fv_idx'], target=GL_ELEMENT_ARRAY_BUFFER)

        self._vbo_vn = vbo.VBO(self._mesh_raw_dict['vn'])
        
        self._vbo_vc = vbo.VBO(self._mesh_raw_dict['vc'])

        self._vbo_vt2D = vbo.VBO(self._mesh_raw_dict['vt2D'])

        return True


    def update_mesh(self):
        pass

    def update_normal_gl_list(self, vnormal=False, fnormal=False):
        if vnormal:
            self._vnormal_gl_list = glGenLists(1)
            glNewList(self._vnormal_gl_list, GL_COMPILE)
            glDisable(GL_LIGHTING)
            glBegin(GL_LINES)
            glColor3f(1.000, 0, 0)  # red
            for vh in self._mesh.vertices():
                glVertex3d(self._mesh.point(vh)[0], self._mesh.point(vh)[1], self._mesh.point(vh)[2])
                p = self._mesh.point(vh) + self._normal_scale * self._mesh.normal(vh)
                glVertex3d(p[0], p[1], p[2])
            glEnd()
            glEndList()

        if fnormal:
            self._fnormal_gl_list = glGenLists(1)
            glNewList(self._fnormal_gl_list, GL_COMPILE)
            glDisable(GL_LIGHTING)
            glBegin(GL_LINES)
            glColor3f(0, 0, 1)  # blue
            for fh in self._mesh.faces():
                _point = self._mesh.property(self._fp_normal_base, fh)
                glVertex3d(_point[0], _point[1], _point[2])
                p = _point + self._normal_scale * 1.5 * self._mesh.normal(fh)
                glVertex3d(p[0], p[1], p[2])
            glEnd()
            glEndList()

    def set_texture(self, texsrc):
        if not self._opt.vertex_has_texcoord(self._opt):
            return False

        w = texsrc.width()
        h = texsrc.height()
        tex_w = 0
        tex_h = 0
        for i in range(1, w+1):
            tex_w <<= 1

        for i in range(1, h+1):
            tex_h <<= 1
        tex_w >>= 1
        tex_h >>= 1
        texture = QImage(QGLWidget.convertToGLFormat(self, QImage=texsrc))

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glPixelStorei(GL_UNPACK_SKIP_ROWS, 0)
        glPixelStorei(GL_UNPACK_SKIP_PIXELS, 0)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glPixelStorei(GL_PACK_ROW_LENGTH, 0)
        glPixelStorei(GL_PACK_SKIP_ROWS, 0)
        glPixelStorei(GL_PACK_SKIP_PIXELS, 0)
        glPixelStorei(GL_PACK_ALIGNMENT, 1)

        if self._tex_id > 0:
            glDeleteTextures(1, self._tex_id)

        glGenTextures(1, self._tex_id)
        glBindTexture(GL_TEXTURE_2D, self._tex_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

        glTexImage2D(target=GL_TEXTURE_2D,
                     level=0,
                     internalformat=GL_RGBA,
                     width=texture.width(),
                     height=texture.height(),
                     border=0,
                     format=GL_RGBA,
                     type=GL_UNSIGNED_BYTE,
                     pixels=texture.bits())

        return True

    def draw_openmesh(self, draw_mode):

        if draw_mode == 'Wireframe':
            glEnableClientState(GL_VERTEX_ARRAY)
            self._vbo_fv_idx.bind()
            self._vbo_vertices.bind()
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
            glDrawElements(GL_TRIANGLES, self._vbo_fv_idx.size, GL_UNSIGNED_INT, None)
            self._vbo_vertices.unbind()
            self._vbo_fv_idx.unbind()
            glDisableVertexAttribArray(0)
            glDisableClientState(GL_VERTEX_ARRAY)

        elif draw_mode == 'Solid Flat':

            glEnableClientState(GL_VERTEX_ARRAY)
            self._vbo_fv_idx.bind()
            self._vbo_vertices.bind()
            glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
            glEnableVertexAttribArray(0)

            glEnableClientState(GL_NORMAL_ARRAY)
            self._vbo_vn.bind()
            glNormalPointer(GL_FLOAT, 0, None)

            glDrawElements(GL_TRIANGLES, self._vbo_fv_idx.size, GL_UNSIGNED_INT, None)

            self._vbo_fv_idx.unbind()
            self._vbo_vn.unbind()
            self._vbo_vertices.unbind()
            glDisableVertexAttribArray(0)
            glDisableClientState(GL_NORMAL_ARRAY)
            glDisableClientState(GL_VERTEX_ARRAY)

        elif draw_mode == 'Solid Smooth':

            glEnableClientState(GL_VERTEX_ARRAY)
            self._vbo_fv_idx.bind()
            self._vbo_vertices.bind()
            glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
            glEnableVertexAttribArray(0)

            glEnableClientState(GL_NORMAL_ARRAY)
            self._vbo_vn.bind()
            glNormalPointer(GL_FLOAT, 0, None)

            if (self._tex_id and self._mesh.has_vertex_texcoords2D()):
                glEnableClientState(GL_TEXTURE_COORD_ARRAY)
                self._vbo_vt2D.bind()
                glTexCoordPointer(2, GL_FLOAT, 0, None)
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, self._tex_id)
                glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, self._tex_mode)

            glDrawElements(GL_TRIANGLES, self._vbo_fv_idx.size, GL_UNSIGNED_INT, None)

            self._vbo_fv_idx.unbind()
            self._vbo_vn.unbind()
            self._vbo_vertices.unbind()
            glDisableVertexAttribArray(0)
            glDisableClientState(GL_NORMAL_ARRAY)
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)

            if self._tex_id and self._mesh.has_vertex_texcoords2D(self._mesh):
                self._vbo_vt2D.unbind()
                glDisable(GL_TEXTURE_2D)

        elif draw_mode == 'Colored Vertices':

            glEnableClientState(GL_VERTEX_ARRAY)
            self._vbo_fv_idx.bind()
            self._vbo_vertices.bind()
            glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
            glEnableVertexAttribArray(0)

            glEnableClientState(GL_NORMAL_ARRAY)
            self._vbo_vn.bind()
            glNormalPointer(GL_FLOAT, 0, None)

            if self._mesh.has_vertex_colors():
                glEnableClientState(GL_COLOR_ARRAY)
                self._vbo_vc.bind()
                glColorPointer(3, GL_UNSIGNED_BYTE, 0, None)

            glDrawElements(GL_TRIANGLES, self._vbo_fv_idx.size, GL_UNSIGNED_INT, None)
            self._vbo_fv_idx.unbind()
            self._vbo_vn.unbind()
            self._vbo_vc.unbind()
            self._vbo_vertices.unbind()
            glDisableVertexAttribArray(0)
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_NORMAL_ARRAY)
            glDisableClientState(GL_COLOR_ARRAY)

        elif draw_mode == 'Solid Colored Faces':
            pass

        elif draw_mode == 'Smooth Colored Faces':
            pass

        elif draw_mode == 'Points':

            glEnableClientState(GL_VERTEX_ARRAY)
            self._vbo_vertices.bind()
            glVertexPointer(3, GL_FLOAT, 0, None)

            if self._mesh.has_vertex_texcoords2D and self._use_color:
                glEnableClientState(GL_COLOR_ARRAY)
                self._vbo_vc.bind()
                glColorPointer(3, GL_UNSIGNED_BYTE, 0, None)

            glDrawArrays(GL_POINTS, 0,  self._vbo_vertices.size)

            self._vbo_vertices.unbind()
            if self._mesh.has_vertex_texcoords2D and self._use_color:
                self._vbo_vc.unbind()
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_COLOR_ARRAY)

    def draw_scene(self, draw_mode):
        if not self._mesh.n_vertices():
            return

        if draw_mode == 'Points':
            glDisable(GL_LIGHTING)
            self.draw_openmesh(draw_mode)

        elif draw_mode == 'Wireframe':
            glDisable(GL_LIGHTING)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            self.draw_openmesh(draw_mode)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        elif draw_mode == 'Hidden-Line':
            glDisable(GL_LIGHTING)
            glShadeModel(GL_FLAT)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glColor4f(0.0, 0.0, 0.0, 1.0 )
            glDepthRange(0.04, 1)
            self.draw_openmesh("Wireframe")

            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glColor4f(1.0, 1.0, 1.0, 1.0)
            glDepthRange(0.0, 1.0)
            self.draw_openmesh("Wireframe")
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        elif draw_mode == 'Solid Flat':
            glEnable(GL_LIGHTING)
            glShadeModel(GL_FLAT)
            self.draw_openmesh(draw_mode)

        elif draw_mode == 'Solid Smooth':
            glEnable(GL_LIGHTING)
            glShadeModel(GL_SMOOTH)
            self.draw_openmesh(draw_mode)

        elif draw_mode == 'Colored Vertices':
            glDisable(GL_LIGHTING)
            glShadeModel(GL_SMOOTH)
            self.draw_openmesh(draw_mode)

        elif draw_mode == 'Solid Colored Faces':
            pass
            glDisable(GL_LIGHTING)
            glShadeModel(GL_FLAT)
            self.draw_openmesh(draw_mode)
            self.setDefaultMaterial()

        elif draw_mode == 'Smooth Colored Faces':
            pass
            glDisable(GL_LIGHTING)
            glShadeModel(GL_SMOOTH)
            self.draw_openmesh(draw_mode)
            self.setDefaultMaterial()

        if self._show_vnormals:
            if self._vnormal_gl_list:
                glCallList(self._vnormal_gl_list)
            else:
                self.update_normal_gl_list(vnormal=True)

        if self._show_fnormals:
            if self._fnormal_gl_list:
                glCallList(self._fnormal_gl_list)
            else:
                self.update_normal_gl_list(fnormal=True)

    def set_texmode(self, mode):
        self._tex_mode = mode

    def keyPressEvent(self, event):
        _event = event.key()
        if _event == Qt.Key_D:
            if self._mesh.has_vertex_texcoords2D() and self.current_draw_mode() == 'Points':
                self._use_color = not self._use_color
                if not self._use_color:
                    glColor3f(1.0, 1.0, 1.0)
                    self.update()

        elif _event == Qt.Key_N:
            if event.modifiers() & Qt.ShiftModifier:
                self._show_fnormals = not self._show_fnormals
            else:
                self._show_vnormals = not self._show_vnormals
            self.update()

        elif _event == Qt.Key_I:
            '''
              std::cout << "\n# Vertices     : " << mesh_.n_vertices() << std::endl;
              std::cout << "# Edges        : " << mesh_.n_edges()    << std::endl;
              std::cout << "# Faces        : " << mesh_.n_faces()    << std::endl;
              std::cout << "binary  input  : " << opt_.check(opt_.Binary) << std::endl;
              std::cout << "swapped input  : " << opt_.check(opt_.Swap) << std::endl;
              std::cout << "vertex normal  : " 
                        << opt_.check(opt_.VertexNormal) << std::endl;
              std::cout << "vertex texcoord: " 
                        << opt_.check(opt_.VertexTexCoord) << std::endl;
              std::cout << "vertex color   : " 
                        << opt_.check(opt_.VertexColor) << std::endl;
              std::cout << "face normal    : " 
                        << opt_.check(opt_.FaceNormal) << std::endl;
              std::cout << "face color     : " 
                        << opt_.check(opt_.FaceColor) << std::endl;
            
            '''
            super(MeshViewerWidgetT, self).keyPressEvent(event)

        elif _event == Qt.Key_T:
            if self._tex_mode == GL_MODULATE:
                self.set_texmode(GL_DECAL)
            elif self._tex_mode == GL_DECAL:
                self.set_texmode(GL_BLEND)
            elif self._tex_mode == GL_BLEND:
                self.set_texmode(GL_REPLACE)
            elif self._tex_mode == GL_REPLACE:
                self.set_texmode(GL_MODULATE)
            self.update()

        else:
            super(MeshViewerWidgetT, self).keyPressEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    opt = openmesh.Options()

    opt += openmesh.Options.FaceColor
    opt += openmesh.Options.FaceNormal
    opt += openmesh.Options.VertexColor
    opt += openmesh.Options.VertexNormal
    opt += openmesh.Options.VertexTexCoord
    opt += openmesh.Options.FaceTexCoord

    _opt = opt
    test_mesh = openmesh.TriMesh()


    openmesh.read_mesh(test_mesh, '/home/haoming/Desktop/Data/atest.obj', opt)

    test_mesh.request_face_normals()
    test_mesh.request_face_colors()
    test_mesh.request_vertex_normals()
    test_mesh.request_vertex_colors()
    test_mesh.request_vertex_texcoords2D()

    mainWin = QMainWindow(flags=Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

    #mainWiget = QWidget()
    w = MeshViewerWidgetT(parent=mainWin)

    #opt += openmesh.Options.FaceColor
    opt += openmesh.Options.FaceNormal
    #opt += openmesh.Options.VertexColor
    opt += openmesh.Options.VertexNormal
    #opt += openmesh.Options.VertexTexCoord
    opt += openmesh.Options.FaceTexCoord
    w.set_mesh(test_mesh, _opt)

    #w.show()
    mainWin.setCentralWidget(w)
    #w.show()
    mainWin.resize(640, 480)
    mainWin.show()



    sys.exit(app.exec_())














































