class MeshViewerWidgetT(QGLViewerWidget):
    def __init__(self, parent=None):
        super(MeshViewerWidgetT, self).__init__()
        self._f_strips = False
        self._tex_id = 0
        self._tex_mode = GL_MODULATE
        self._strips = None
        self._mesh = openmesh.TriMesh()
        self._opt = None
        self.radius = 0
        self._fp_normal_base = openmesh.FPropHandle()
        self._show_vnormals = False
        self._show_fnormals = False
        self._use_color = False
        a = self.add_draw_mode('Points')
        a.setShortcut(QKeySequence(Qt.Key_P))
        a.setChecked(True)
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

        self._mesh.add_property(self._fp_normal_base, "fp_normal_base")

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
                # vertices_color.append([self._mesh.color(vh)[0], self._mesh.color(vh)[1], self._mesh.color(vh)[2]])
                pass
            if self._mesh.has_vertex_texcoords2D():
                _vertices_tex_2D.append([self._mesh.texcoord2D(vh)[0], self._mesh.texcoord2D(vh)[1]])
            bbMin.minimize(openmesh.Vec3f(_point[0], _point[1], _point[2]))
            bbMax.maximize(openmesh.Vec3f(_point[0], _point[1], _point[2]))

        self._mesh_raw_dict.update({'v': np.array(_vertices, dtype=np.float32),
                                    'vn': np.array(_vertices_normals, dtype=np.float32), 'vh': _vh,
                                    # 'vc': np.array(_vertices_color, dtype=np.float32),
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

        print("%s Vertices, %s edges, %s faces" % (
        str(self._mesh.n_vertices()), str(self._mesh.n_edges()), str(self._mesh.n_faces())))

        # create vertex buffer object in Server side

        self._vbo_vertexes = vbo.VBO(self._mesh_raw_dict['v'])

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
                print(p)
            print("test")
            glEnd()
            glEndList()

    def set_texture(self, texsrc):
        if not self._opt.vertex_has_texcoord(self._opt):
            return False

        w = texsrc.width()
        h = texsrc.height()
        tex_w = 0
        tex_h = 0
        for i in range(1, w + 1):
            tex_w <<= 1

        for i in range(1, h + 1):
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
            self._vbo_vertexes.bind()
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
            glDrawElements(GL_TRIANGLES, self._vbo_fv_idx.size, GL_UNSIGNED_INT, None)
            self._vbo_vertexes.unbind()
            self._vbo_fv_idx.unbind()
            glDisableVertexAttribArray(0)
            glDisableClientState(GL_VERTEX_ARRAY)

        elif draw_mode == 'Solid Flat':

            glEnableClientState(GL_VERTEX_ARRAY)
            self._vbo_fv_idx.bind()
            self._vbo_vertexes.bind()
            glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
            glEnableVertexAttribArray(0)

            glEnableClientState(GL_NORMAL_ARRAY)
            self._vbo_vn.bind()
            glNormalPointer(GL_FLOAT, 0, None)

            glDrawElements(GL_TRIANGLES, self._vbo_fv_idx.size, GL_UNSIGNED_INT, None)

            self._vbo_fv_idx.unbind()
            self._vbo_vn.unbind()
            self._vbo_vertexes.unbind()
            glDisableVertexAttribArray(0)
            glDisableClientState(GL_NORMAL_ARRAY)
            glDisableClientState(GL_VERTEX_ARRAY)

        elif draw_mode == 'Solid Smooth':

            glEnableClientState(GL_VERTEX_ARRAY)
            self._vbo_fv_idx.bind()
            self._vbo_vertexes.bind()
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
            self._vbo_vertexes.unbind()
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
            self._vbo_vertexes.bind()
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
            self._vbo_vertexes.unbind()
            glDisableVertexAttribArray(0)
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_NORMAL_ARRAY)
            glDisableClientState(GL_COLOR_ARRAY)

        elif draw_mode == 'Solid Colored Faces':
            pass

        elif draw_mode == 'Smooth Colored Faces':
            pass

        elif draw_mode == 'Points':
            glClearColor(0.3, 0.6, 0.9, 1)
            glEnableClientState(GL_VERTEX_ARRAY)
            self._vbo_vertexes.bind()
            glVertexPointer(3, GL_FLOAT, 0, None)

            if self._mesh.has_vertex_texcoords2D and self._use_color:
                glEnableClientState(GL_COLOR_ARRAY)
                self._vbo_vc.bind()
                glColorPointer(3, GL_UNSIGNED_BYTE, 0, None)

            glDrawArrays(GL_POINTS, 0, self._vbo_vertexes.size)

            self._vbo_vertexes.unbind()
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

        elif draw_mode == 'Colored Wireframe':
            glDisable(GL_LIGHTING)
            glShadeModel(GL_FLAT)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glColor4f(0.0, 0.0, 0.0, 1.0)
            glDepthRange(0.04, 1)
            self.draw_openmesh(draw_mode)

            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

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
