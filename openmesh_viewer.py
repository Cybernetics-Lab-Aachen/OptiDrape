from openmesh import *

import openmesh

from PyQt5.QtOpenGL import QGLWidget, QGLFormat, QGL
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
from pythonlangutil.overload import Overload, signature

from PyQt5 import QtGui

TRACKBALLradius = 0.6


class QGLViewerWidget(QGLWidget):
    def __init__(self, parent):
        super(QGLWidget, self).__init__(parent=parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAcceptDrops(True)
        self.setCursor(Qt.PointingHandCursor)
        self._n_draw_modes = 0
        self._action_dict = dict()

        self._popup_menu = QMenu(self)
        self._draw_modes_group = QActionGroup(self)

        self._draw_modes_group.pyqtConfigure(triggered=self.slotDrawMode)

        self._modelview_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        self._projection_matrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

        self._draw_mode = ''
        self._draw_mode_names = []

        self.radius = 0
        self.center = [0, 0]
        self._last_point_2D = QPoint(0, 0)
        self._last_point_3D = Vec3f(0, 0, 0)
        self._last_point_ok = True

        self.add_draw_mode("Solid Flat")
        a = self.add_draw_mode("Solid Smooth")
        a.setShortcut(QKeySequence(Qt.Key_S))
        a = self.add_draw_mode("Wireframe")
        a.setShortcut(QKeySequence(Qt.Key_W))
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
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, shine)

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
        print("initializeGL")
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glDisable(GL_DITHER)
        glEnable(GL_DEPTH_TEST)

        self.setDefaultMaterial()

        glLoadIdentity()
        self.setDefaultLight()

        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogfv(GL_FOG_COLOR, [0.3, 0.3, 0.4, 1.0])
        glFogf(GL_FOG_DENSITY, 0.35)
        glHint(GL_FOG_HINT, GL_DONT_CARE)
        glFogf(GL_FOG_START, 5.0)
        glFogf(GL_FOG_END, 25.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self._modelview_matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
        print("self._modelview_matrix")
        print(self._modelview_matrix)
        self.set_scene_pos([0, 0, 0], 1.0)

    def resizeGL(self, w, h):
        self.update_projection_matrix()
        glViewport(0, 0, w, h)
        self.updateGL()

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
            self._last_point_ok = self.map_to_sphere(self._last_point_2D, self._last_point_3D)
            self._last_point_2D = event.pos()

    def mouseMoveEvent(self, event):
        newPoint2D = event.pos()
        newPoint3D = Vec3f(0, 0, 0)
        newPoint_hitSphere = self.map_to_sphere(newPoint2D, newPoint3D)
        dx = newPoint2D.x() - self._last_point_2D.x()
        dy = newPoint2D.y() - self._last_point_2D.y()
        w = self.width()
        h = self.height()
        self.makeCurrent()
        if (event.buttons() == (Qt.RightButton + Qt.LeftButton)) or \
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

                    if t < -1:
                        t = - 1.0
                    elif t > 1:
                        t = 1.0

                    phi = 2 * math.asin(t)
                    angle = phi * 180 / math.pi

                    self.rotate(axis, angle)

        self._last_point_2D = newPoint2D
        self._last_point_3D = newPoint3D
        self._last_point_ok = newPoint_hitSphere

        self.updateGL()

    def mouseReleaseEvent(self, event):
        self._last_point_ok = False

    def wheelEvent(self, event):
        d = - event.angleDelta().y() / 120 * 2 * self.radius
        self.translate(np.array([0, 0, d]))
        self.updateGL()
        event.accept()

    def keyPressEvent(self, event):

        if event.key() is Qt.Key_Print:
            self.slotSnapshot()
        elif event.key() is Qt.Key_H:
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
        elif event.key() is Qt.Key_C:
            if glIsEnabled(GL_CULL_FACE):
                glDisable(GL_CULL_FACE)
                # TODO: Throw out sth
            else:
                glEnable(GL_FOG)
            self.updateGL()

        elif event.key() is Qt.Key_I:
            pass
            """"""

        elif event.modifiers() & Qt.ShiftModifier:
            fps = self.performance()
            # TODO: output performance

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
        xval = (2.0 * v2D.x() - self.width()) / self.width()
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
        gluPerspective(45.0, self.width()/self.height(), 0.01 * self.radius, 100.0 * self.radius)
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
        self.radius = radius
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
        print(str(self._draw_mode))
        self.updateGL()

    def performance(self):
        self.setCursor(Qt.WaitCursor)

        self.makeCurrent()
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        frames = 60.0
        angle = 360.0 / frames

        total_time = 0
        glFinish()
        for axis in [Vec3f(1, 0, 0), Vec3f(0, 1, 0), Vec3f(0, 0, 1)]:
            start = time.clock()
            for i in range(int(frames)):
                self.rotate(axis, angle)
                self.paintGL()
                self.swapBuffers()
            total_time += time.clock() - start
            QApplication.processEvents(self)


        glFinish()

        glPopMatrix()
        self.updateGL()

        fps = (3.0 * frames) / total_time

        self.setCursor(Qt.PointingHandCursor)

        return fps

    def slotSnapshot(self):
        image = QImage()
        w, h = self.width(), self.height()
        buffer = GLenum(GL_BACK)
        fbuffer = []
        try:

            QApplication.processEvents()
            self.makeCurrent()
            self.updateGL()
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
        self.add_draw_mode('Points')
        self.add_draw_mode('Hidden-Line')

        self._face_point = []


    def update_mesh(self, new_mesh, opt):
        #self._mesh.request_face_normals()
        #self._mesh.request_face_colors()
        #self._mesh.request_vertex_normals()
        #self._mesh.request_vertex_colors()
        #self._mesh.request_vertex_texcoords2D()
        self._mesh = new_mesh
        self._opt = opt

        print(self._mesh)

        if self._opt.check(openmesh.Options.FaceNormal):
            self._mesh.update_face_normals()

        if self._opt.check(Options.VertexNormal):
            self._mesh.update_vertex_normals()

        if self._opt.check(Options.VertexColor):
            self.add_draw_mode('Colored Vertices')
        else:
            self._mesh.release_vertex_colors()

        if self._opt.check(Options.FaceColor):
            self.add_draw_mode('Solid Colored Faces')
            self.add_draw_mode('Smooth Colored Faces')
        else:
            self._mesh.request_face_colors()

        bbMin = openmesh.Vec3f(100, 100, 100)
        bbMax = openmesh.Vec3f(0, 0, 0)

        for vh in self._mesh.vertices():
            _point = self._mesh.point(vh)
            bbMin.minimize(openmesh.Vec3f(_point[0], _point[1], _point[2]))
            bbMax.maximize(openmesh.Vec3f(_point[0], _point[1], _point[2]))

        for fh in self._mesh.faces():
            for fv in self._mesh.fv(fh):
                self._face_point.append([self._mesh.point(fv)[0], self._mesh.point(fv)[1], self._mesh.point(fv)[2]])

        print((bbMin - bbMax).norm() / 2)
        self.set_scene_pos(cog=(bbMin + bbMax) / 2,
                           radius=(bbMin - bbMax).norm() / 2)

        self._normal_scale = (bbMax - bbMin).min() * 0.05

        # TODO: INFO output
        """
        std::clog << mesh_.n_vertices() << " vertices, "
	      << mesh_.n_edges()    << " edge, "
	      << mesh_.n_faces()    << " faces\n";
        """
        print(bbMin.length())
        print("%s Vertices, %s edges, %s faces" % (str(self._mesh.n_vertices()), str(self._mesh.n_edges()), str(self._mesh.n_faces())))

        total_time = 0

        start = time.clock()

        self._mesh.add_property(self._fp_normal_base)

        v = Vec3f(0, 0, 0)
        for fh in self._mesh.faces():
            for fv in self._mesh.fv(fh):
                if fv.is_valid():
                    v += openmesh.Vec3f(self._mesh.point(fv)[0], self._mesh.point(fv)[1], self._mesh.point(fv)[2])
            v *= 1.0/3.0
            self._mesh.set_property(self._fp_normal_base, fh, v)

        total_time += time.clock() - start

        # TODO: output time
        """
        std::clog << "Computed base point for displaying face normals [" 
                << t.as_string() << "]" << std::endl;
                
        std::clog << "Computing strips.." << std::flush;
        OpenMesh::Utils::Timer t;
         t.start();
        compute_strips();
        t.stop();
        std::clog << "done [" << strips_.n_strips() 
		<< " strips created in " << t.as_string() << "]\n";
        """
        self.updateGL()
        return True

    def glVertex(self, VertexHandle=None, Meshpoint=None):
        if VertexHandle:
            glVertex3fv(self._mesh.point(VertexHandle)[0])
        if Meshpoint:
            glVertex3fv(Meshpoint[0])

    def glNormal(self, VertexHandle=None, FaceHandle=None):
        if VertexHandle:
            glNormal3fv(self._mesh.normal(VertexHandle)[0])
        if FaceHandle:
            glNormal3fv(self._mesh.normal(FaceHandle)[0])

    def glTexCoord(self, VertexHandle):
        glTexCoord2fv(self._mesh.texcoord(VertexHandle)[0])

    def glColor(self, VertexHandle=None, FaceHandle=None):
        if VertexHandle:
            glColor3ubv(self._mesh.color(VertexHandle)[0])
        if FaceHandle:
            glColor3ubv(self._mesh.color(FaceHandle)[0])

    def glMaterial(self, FaceHandle, _f=GL_FRONT_AND_BACK, _m=GL_DIFFUSE):
        c = Vec3f(self._mesh.color(FaceHandle))
        m = Vec4f(c[0], c[1], c[2], c[3], 1.0)
        glMaterialfv(_f, _m, m[0])

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


            glBegin(GL_TRIANGLES)
            """for fh in self._mesh.faces():
                for fv in self._mesh.fv(fh):
                    glVertex3fv([self._mesh.point(fv)[0], self._mesh.point(fv)[1], self._mesh.point(fv)[2]])"""
            for p in self._face_point:
                glVertex3fv(p)
            glEnd()

        elif draw_mode == 'Solid Flat':
            glBegin(GL_TRIANGLES)
            for fh in self._mesh.faces():
                glNormal3fv([self._mesh.normal(fh)[0], self._mesh.normal(fh)[1], self._mesh.normal(fh)[2]])
                for fv in self._mesh.fv(fh):
                    glVertex3fv([self._mesh.point(fv)[0], self._mesh.point(fv)[1], self._mesh.point(fv)[2]])
            glEnd()

        elif draw_mode == 'Solid Smooth':
            glEnableClientState(GL_VERTEX_ARRAY)
            #glVertexPointer(3, GL_FLOAT, 0, self._mesh.vertices())

            glEnableClientState(GL_NORMAL_ARRAY)
            #glNormalPointer(GL_FLOAT, 0, self._mesh.vertex_normals())

            if (self._tex_id and self._mesh.has_vertex_texcoords2D(self._mesh)):
                glEnableClientState(GL_TEXTURE_COORD_ARRAY)
                glTexCoordPointer(2, GL_FLOAT, 0, self._mesh.texcoords2D())
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, self._tex_id)
                glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, self._tex_mode)

            glBegin(GL_TRIANGLES)
            for fh in self._mesh.faces():
                for fv in self._mesh.fv(fh):
                    pass
                    #print(fv.idx())
                    #glArrayElement(fv.idx())
            glEnd()
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_NORMAL_ARRAY)
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)

            if self._tex_id and self._mesh.has_vertex_texcoords2D(self._mesh):
                glDisable(GL_TEXTURE_2D)

        elif draw_mode == 'Colored Vertices':
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, self._mesh.points())

            glEnableClientState(GL_NORMAL_ARRAY)
            glNormalPointer(GL_FLOAT, 0, self._mesh.vertex_normals())

            if self._mesh.has_vertex_colors(self._mesh):
                glEnableClientState(GL_COLOR_ARRAY)
                glColorPointer(3, GL_UNSIGNED_BYTE, 0, self._mesh.vertex_colors())

            glBegin(GL_TRIANGLES)
            for fh in self._mesh.faces():
                for fv in self._mesh.fv(fh):
                    glArrayElement(fv)
            glEnd()
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_NORMAL_ARRAY)
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)

        elif draw_mode == 'Solid Colored Faces':
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, self._mesh.points())

            glEnableClientState(GL_NORMAL_ARRAY)
            glNormalPointer(GL_FLOAT, 0, self._mesh.vertex_normals())

            glBegin(GL_TRIANGLES)
            for fh in self._mesh.faces():
                glColor(fh)
                for fv in self._mesh.fv(fh):
                    glArrayElement(fv)
            glEnd()
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_NORMAL_ARRAY)

        elif draw_mode == 'Smooth Colored Faces':
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, self._mesh.points())

            glEnableClientState(GL_NORMAL_ARRAY)
            glNormalPointer(GL_FLOAT, 0, self._mesh.vertex_normals())

            glBegin(GL_TRIANGLES)
            for fh in self._mesh.faces():
                glMaterial(fh, GL_DIFFUSE)
                for fv in self._mesh.fv(fh):
                    glArrayElement(fv)
            glEnd()
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_NORMAL_ARRAY)

        elif draw_mode == "Strips'n VertexArrays":
            '''glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, self._mesh.points())

            glEnableClientState(GL_NORMAL_ARRAY)
            glNormalPointer(GL_FLOAT, 0, self._mesh.vertex_normals())

            if self._tex_id and self._mesh.has_vertex_texcoords2D(self._mesh):
                glEnableClientState(GL_TEXTURE_COORD_ARRAY)
                glTexCoordPointer(2, GL_FLOAT, 0, self._mesh.texcoords2D())
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, self._tex_id)
                glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, self._tex_mode)'''
            pass

        elif draw_mode == 'Show Strips':
            pass
        elif draw_mode == 'Points':
            glEnableClientState(GL_VERTEX_ARRAY)

            test = np.zeros((self._mesh.n_vertices(), 3), dtype=np.float32)

            i = 0
            for vh in self._mesh.vertices():
                test[i] = np.array([self._mesh.point(vh)[0], self._mesh.point(vh)[1], self._mesh.point(vh)[2]])
                i += 1

            glVertexPointer(3, GL_FLOAT, 0, test)

            if self._mesh.has_vertex_texcoords2D() and self._use_color:
                glEnableClientState(GL_COLOR_ARRAY)
                glColorPointer(3, GL_UNSIGNED_BYTE, 0, [1,2,3,4,5,6])

                glDrawArrays(GL_POINTS, 0,  GLsizei(self._mesh.n_vertices(self._mesh)))
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
            glDepthRange(0.01, 1.0)
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
            glShadeModel(GL_FLAT)
            self.draw_openmesh(draw_mode)

        elif draw_mode == 'Colored Vertices':
            glDisable(GL_LIGHTING)
            glShadeModel(GL_SMOOTH)
            self.draw_openmesh(draw_mode)

        elif draw_mode == 'Solid Colored Faces':
            glDisable(GL_LIGHTING)
            glShadeModel(GL_FLAT)
            self.draw_openmesh(draw_mode)
            self.setDefaultMaterial()

        if self._show_vnormals:
            glDisable(GL_LIGHTING)
            glBegin(GL_LINES)
            glColor3f(1.000, 0.803, 0.027) # orange
            for vh in self._mesh.vertices():

                print(self._mesh.vertex(vh))
                vi = openmesh.VertexIter(self._mesh, vh)
                glVertex3d(self._mesh.point(vh)[0], self._mesh.point(vh)[1], self._mesh.point(vh)[2])
                p = self._mesh.point(vh) + self._normal_scale * self._mesh.normal(vh)
                glVertex3d(p[0], p[1], p[2])
            glEnd()

        if self._show_fnormals:
            glDisable(GL_LIGHTING)
            glBegin(GL_LINES)
            glColor3f(0.705, 0.976, 0.270)  # orange

            for fh in self._mesh.faces():
                fit_next = fh
                glVertex(self._mesh.property(fit_next, self._fp_normal_base))
                glVertex(self._mesh.property(fit_next, self._fp_normal_base) + self._normal_scale * self._mesh.normal(
                    fit_next))
            glEnd()

    def set_texmode(self, mode):
        self._tex_mode = mode

    def keyPressEvent(self, event):
        _event = event.key()
        if _event == Qt.Key_D:
            print("test D")
            if self._mesh.has_vertex_texcoords2D() and self.current_draw_mode() == 'Points':
                self._use_color = not self._use_color
                if not self._use_color:
                    glColor3f(1.0, 1.0, 1.0)
                    self.updateGL()

        elif _event == Qt.Key_N:
            if _event.modifiers() & Qt.ShiftModifier:
                self._show_fnormals = not self._show_fnormals
            else:
                self._show_vnormals = not self._show_vnormals
            self.updateGL()

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

            super(QGLViewerWidget, self).keyPressEvent(event)

        elif _event == Qt.Key_T:
            if self._tex_mode == GL_MODULATE:
                self.set_texmode(GL_DECAL)
            elif self._tex_mode == GL_DECAL:
                self.set_texmode(GL_BLEND)
            elif self._tex_mode == GL_BLEND:
                self.set_texmode(GL_REPLACE)
            elif self._tex_mode == GL_REPLACE:
                self.set_texmode(GL_MODULATE)
            self.updateGL()

        else:
            super(QGLViewerWidget, self).keyPressEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    opt = openmesh.Options()

    opt += openmesh.Options.FaceColor
    opt += openmesh.Options.FaceNormal
    opt += openmesh.Options.VertexColor
    opt += openmesh.Options.VertexNormal
    opt += openmesh.Options.VertexTexCoord
    opt += openmesh.Options.FaceTexCoord

    print(opt.check(openmesh.Options.VertexNormal))
    test_mesh = openmesh.PolyMesh()

    test_mesh.request_face_normals()
    test_mesh.request_face_colors()
    test_mesh.request_vertex_normals()
    test_mesh.request_vertex_colors()
    test_mesh.request_vertex_texcoords2D()

    openmesh.read_mesh(test_mesh, '/home/haoming/Desktop/Data/atest.obj')

    print(test_mesh)

    mainWin = QMainWindow(flags=Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

    #mainWiget = QWidget()
    w = MeshViewerWidgetT(parent=mainWin)

    w.update_mesh(test_mesh, opt)

    w.show()
    mainWin.setCentralWidget(w)
    #w.show()
    mainWin.show()



    sys.exit(app.exec_())














































