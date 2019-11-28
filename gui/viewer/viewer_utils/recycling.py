def _connect_database(self):
    _url = self.le_dburl_input.text()
    if _url:
        _url += '/?connectTimeoutMS=2000'
        self.statusBar.showMessage('Connecting MongoDB...')
        try:
            self.mongo_client = MongoClient(_url)
            self.cBox_databases.clear()
            self.cBox_databases.addItems(
                item for item in self.mongo_client.database_names() if item not in ['admin', 'local', 'config'])
            self.cBox_databases.update()
            self.pB_connect_db.setDisabled(True)
            self.pB_disconnect_db.setDisabled(False)
            self.pB_refresh_db.setDisabled(False)
            self.pB_load_db.setDisabled(False)
            self.pB_export_db.setDisabled(False)
            self.pB_import_files.setDisabled(False)
            self.pB_delete_db.setDisabled(False)
            self.pB_set_db.setDisabled(False)
            self.statusBar.showMessage('MongoDB Server connected.')

        except mongo_error.ConnectionFailure:
            QMessageBox.critical(self, 'Connection Failed', 'Cannot connect the MongoDB Server! Is the Server running?',
                                 QMessageBox.Ok)
    else:
        QMessageBox.warning(self, 'Warning', 'Please specify the database URL!', QMessageBox.Ok)


def _disconnect_database(self):
    try:
        self.mongo_client.close()
        self.cBox_databases.clear()
        self.statusBar.showMessage('MongoDB Server disconnected.')
    except mongo_error.ConnectionFailure:
        # makes no sense to throw out the error
        pass

    self.pB_connect_db.setDisabled(False)
    self.pB_disconnect_db.setDisabled(True)
    self.pB_set_db.setDisabled(True)
    self.pB_load_db.setDisabled(True)
    self.pB_export_db.setDisabled(True)
    self.pB_import_files.setDisabled(True)
    self.pB_delete_db.setDisabled(True)
    self.pB_refresh_db.setDisabled(True)


def _refresh_database(self):
    self.statusBar.showMessage("Refreshing DataBase...")
    self.tree_db_viewer.reset()
    self.cBox_databases.clear()
    self.cBox_databases.addItems(self.mongo_client.database_names())
    self.cBox_databases.update()

    self.statusBar.showMessage("DataBase refreshed.")


def _set_model_db(self):
    _db_name = ''
    # check if there is model database in combo box
    AllItems = [self.cBox_databases.itemText(i) for i in range(self.cBox_databases.count())]
    for _item in AllItems:
        if _item == 'ModelDatabase':
            _db_name = _item
    if _db_name == '':
        _reply = QMessageBox.warning(self, "no model db built!",
                                     "please add your model database in tab : model manager \rnavigate you to model manager?",
                                     QMessageBox.Yes | QMessageBox.No)

        if _reply == QMessageBox.No:
            return

        else:
            self.tabWidget.setCurrentIndex(1)
            return

    # no we only allow the specific db name, expand when needed
    if _db_name != 'ModelDatabase':
        print('unidentifiedunidentified name')
        return

    self.model_obj.set_model_db_name(_db_name)
    self.model_obj.update_model_table()
    self.statusBar.showMessage("model data has been show on the table in Model Manager tab")


def _set_database(self):
    # we try to set all data, which was saved in the data base
    ## simulation datta
    ## textile data

    _db_names = [self.cBox_databases.itemText(i) for i in range(self.cBox_databases.count())]

    if not _db_names:
        QMessageBox.warning(self, "Warning", "No Valid Database was choosen!", QMessageBox.Ok)
        return

    self.statusBar.showMessage("View database as %s" % str(_db_names))

    try:
        # we will only grasp the collections, which are definied from user, not system
        self.gBox_viewer.setDisabled(False)
        build_data_view_tree(tree_handle=self.tree_db_viewer,
                             data_bases=_db_names,
                             database_instance=self.mongo_client)
    except:
        self.statusBar.showMessage("Failed to get the collections from %s" % self._database)


def _delete_database(self):
    _db_2_delete = self.cBox_databases.currentText()
    if _db_2_delete in self.mongo_client.database_names():
        self.mongo_client.drop_database(_db_2_delete)
    else:
        QMessageBox.warning(self, "Warning", "No Database named %s" % _db_2_delete,
                            QMessageBox.Ok)
    self._refresh_database()


def _import_files(self):
    self.statusBar.showMessage("Importing contents to Database...")

    if self._database:
        _reply = QMessageBox.question(self, "Question",
                                      "Database %s was choosen. Add Content to this Database?" % str(self._database),
                                      QMessageBox.Yes | QMessageBox.No | QMessageBox.Abort)

        if _reply == QMessageBox.No:
            _database_to_add, isok = QInputDialog.getText(self, "Please specify the new database name.",
                                                          "Database Name:",
                                                          QLineEdit.Normal, '')
            if not isok:
                return
        elif _reply == QMessageBox.Abort:
            return
        else:
            _database_to_add = self._database
    else:
        _database_to_add, isok = QInputDialog.getText(self, "Please specify the new database name.", "Database Name:",
                                                      QLineEdit.Normal, 'OptiDrape')
        if not isok:
            return

    _db_collection, isok = QInputDialog.getText(self, "Plase specify the database collection name.", "Collection Name:",
                                                QLineEdit.Normal, 'training')

    if not isok:
        return

    _folder_path = QFileDialog.getExistingDirectory(self, "Parent Directory of Content")

    self.statusBar.showMessage("Adding %s data in database %s" % (_db_collection, _database_to_add))
    self.pB_import_files.setDisabled(True)

    data_extraction.load_and_extract_data_from_simulation(path=_folder_path,
                                                          db_instance=self.mongo_client[_database_to_add])

    self.statusBar.showMessage("Add %s data in database %s Done!" % (_db_collection, _database_to_add))
    self.pB_import_files.setDisabled(False)
    self._refresh_database()


def _import_meta_data(self):
    _folder_path = QFileDialog.getOpenFileName(self, "meta data source")
    _needed_meta_data = self._get_meta_data_request()
    _meta_data = data_extraction.extract_meta_data(path=_folder_path, requests=_needed_meta_data)


def _load_database(self):
    # TODO: add database or collection in mongodb
    pass


def _export_database(self):
    # TODO: export database oder collection from mongodb
    pass



def _build_mesh_table(self):
        if self._mesh_table:
            self._mesh_table.destroy()

        _router, _data = self._get_data_from_tree()

        # table element, hidden when the program just run
        self._mesh_table = QWidget()

        _table = QTableWidget(self._mesh_table)
        _table.setRowCount(0)
        _table.setColumnCount(9)
        _table.setGeometry(QRect(200, 400, 700, 700))
        _table.verticalHeader().setVisible(False)
        _table.horizontalHeader().setVisible(False)

        _table.insertRow(0)
        _table.setItem(0, 0, QTableWidgetItem('Index'))
        _table.setItem(0, 1, QTableWidgetItem('StartPt_X'))
        _table.setItem(0, 2, QTableWidgetItem('StartPt_Y'))
        _table.setItem(0, 3, QTableWidgetItem('StartPt_Z'))
        _table.setItem(0, 4, QTableWidgetItem('EndPt_X'))
        _table.setItem(0, 5, QTableWidgetItem('EndPt_Y'))
        _table.setItem(0, 6, QTableWidgetItem('EndPt_Z'))
        _table.setItem(0, 7, QTableWidgetItem('ShearAngle'))
        _table.setItem(0, 8, QTableWidgetItem('Thinning'))

        # set table view
        for columeIndex in range(9):
            _table.setColumnWidth(columeIndex, 120)  # should figure out index meaning
            _table.item(0, columeIndex).setBackground(QColor(255, 204, 0))

        _data = _data['Vertex']

        for index, key in enumerate(sorted(_data, key=lambda t: int(t)), start=1):
            _table.insertRow(index)
            _table.setItem(index, 0, QTableWidgetItem(key))
            _table.item(index, 0).setBackground(QColor(255, 255, 0))
            for DataType in _data[key].keys():
                _this_data = _data[key][DataType]
                if DataType == 'point_start':
                    for i in range(3):
                        _table.setItem(index, i+1, QTableWidgetItem(str(_this_data[i])))
                elif DataType == 'point_end':
                    for i in range(3):
                        _table.setItem(index, i + 4, QTableWidgetItem(str(_this_data[i])))
                elif DataType == 'shear_angle':
                    _table.setItem(index, 7, QTableWidgetItem(str(_this_data)))
                elif DataType == 'thinning':
                    _table.setItem(index, 8, QTableWidgetItem(str(_this_data)))

        layout = QVBoxLayout(self._mesh_table)
        layout.addWidget(_table)
        self._mesh_table.setLayout(layout)

        _title = ""
        for s in _router:
            _title += str(s)

        # todo : clarify how table stretch with the colume
        self._mesh_table.resize(_table.geometry().width(),_table.geometry().height())
        self._mesh_table.show()