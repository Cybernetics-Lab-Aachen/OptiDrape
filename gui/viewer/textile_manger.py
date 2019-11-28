from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from gui.ui.ui_textile_manager import Ui_TextileManager
from gui.viewer.viewer_utils.utils import *
import numpy as np
from Data.fit_data import *
from Data.drape_utils import *
from Data.pickle_data import load_pickle_data, update_pickled_data, pickle_data
import pickle
import h5py, os
from gui.viewer.viewer_utils.utils import InfoType


class TextileManagerManager(QWidget, Ui_TextileManager):
    def __init__(self, parent):
        super(TextileManagerManager, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("TextileManagerManager")

        # Global variables
        self.parent = parent
        self._echo = parent.echo_info
        self._textile_selected = []
        self._textile_data_base_name = ""
        self._textile_data_base_path = ""
        self._textile_data_changed = False

        # Push Buttons
        self.pb_new_dataset.clicked.connect(self._new_dataset_clicked)
        self.pb_load_textile.clicked.connect(self._load_textile_clicked)
        self.pb_add_textile.clicked.connect(self._add_textile_clicked)
        self.pb_add_textile.setDisabled(True)
        self.pb_delete_textile.clicked.connect(self._del_textile_clicked)
        self.gb_add_model.setDisabled(True)
        self.pb_delete_textile.setDisabled(True)
        self.pb_save_textile.setDisabled(True)
        self.gb_model_raw.setDisabled(True)
        self.pb_save_cell.clicked.connect(self._save_cell_clicked)
        self.pb_del_cell.clicked.connect(self._del_cell_clicked)
        self.pb_save_textile.clicked.connect(self._save_textile_clicked)
        self.pb_save_variant.clicked.connect(self._save_variant_clicked)
        self.pb_delete_variant.clicked.connect(self._del_vaiant_cliecked)
        self.pB_calc_querstress.clicked.connect(self._calc_querstress_clicked)
        self.pB_save_querstress.clicked.connect(self._save_querstress_clicked)
       # self.pb_drop_database.clicked.connect(self._drop_data_base_clicked)
        self.treeView_textile.clicked.connect(self._textile_tree_clicked)

        self.hSlider_plot.valueChanged.connect(self._fit_data_and_plot)
        self.pB_insert_data.clicked.connect(self._pb_insert_data_clicked)

        # Setup raw data table view
        self._clean()

    @property
    def textile_database(self):
        if not self._textile_data_base_path:
            self._load_textile_clicked()
        return load_pickle_data(self._textile_data_base_path)

    def __set_edit_enable(self):
        self.pb_add_textile.setDisabled(False)
        self.pb_delete_textile.setDisabled(False)
        self.pb_save_textile.setDisabled(False)

    def _load_textile_clicked(self):

        if self._textile_data_base_name and self._textile_data_changed:
            rep = QMessageBox.warning(self, "Warning", "Current DataBase %s was changed but not saved, would you like to save it?" % self._textile_data_base_name,
                                QMessageBox.Yes | QMessageBox.No)

            if rep == QMessageBox.Yes:
                self._drop_data_base_clicked()

        _opt = QFileDialog.Options()
        _opt |= QFileDialog.DontUseNativeDialog

        _path, _ = QFileDialog.getOpenFileName(self, "Load Textile DataBase", "",
                                               "Binary (*.p, *.pickle);;All Files (*)", options=_opt)

        if _path:
            self._textile_data_base_path = _path
            self._textile_data_base_name = os.path.splitext(os.path.basename(_path))[0]

        self.__update_textile_tree()

    def __update_textile_tree(self):
        _tree_data = load_pickle_data(self._textile_data_base_path)
        #print(_tree_data)
        build_textile_data_tree_from_dict(tree_handle=self.treeView_textile, data_dict=_tree_data)
        self.treeView_textile.expandAll()

    def _new_dataset_clicked(self):
        d, is_ok = QInputDialog.getText(self, 'New Textile DataBase', 'Please type the name of DataBase:')

        if not is_ok or not d:
            self._echo(instance=self, msg="Invalid Name given!", type=InfoType.WARNING)
            return

        _db_path = QFileDialog.getExistingDirectory(self, "Path of new Textile DataBase")

        if not _db_path:
            self._echo(instance=self, msg="Invalid Path given!", type=InfoType.WARNING)
            return

        self._textile_data_base_name = d
        self._textile_data_base_path = _db_path + "/" + d + ".pickle"

        if os.path.isfile(self._textile_data_base_path):
            rep = QMessageBox.warning(self, "Warning",
                                      "Current DataBase %s exists, would you like to overwrite (y) or update (n) it?" % self._textile_data_base_name,
                                      QMessageBox.Yes | QMessageBox.No)

            if rep == QMessageBox.Yes:
                try:
                    os.remove(self._textile_data_base_path)
                except:
                    self._echo(instance=self, msg="Error while deleting file %s" % d, type=InfoType.ERROR)

        self._echo(instance=self, msg="New DataBase named as: %s" % d)
        self._echo(instance=self, msg=" New DataBase saved as: %s" % self._textile_data_base_path)
        self.__set_edit_enable()

    def _drop_data_base_clicked(self):
        pass

    def _textile_tree_clicked(self):
        self._textile_selected.clear()
        _last = self.treeView_textile.selectedIndexes()[0]
        self._textile_selected.append(_last.data())
        while _last.parent().data():
            _last = _last.parent()
            self._textile_selected.append(_last.data())
        self._textile_selected.reverse()

        if self._textile_selected:
            self.__set_edit_enable()

        _textile_database_dict = load_pickle_data(self._textile_data_base_path)

        # load info
        if self._textile_selected and _textile_database_dict:
            self._clean()
            self.edit_textile_name.setText(self._textile_selected[0])
            self.gb_model_raw.setDisabled(False)
            self.gb_add_model.setDisabled(False)

            _textile_data_dict = dict()

            if self._textile_selected[0] in _textile_database_dict.keys():
                _textile_data_dict = _textile_database_dict[self._textile_selected[0]]

            if "raw_data" in _textile_data_dict.keys():
                try:
                    self.lineEdit_x.setText(str(_textile_data_dict['raw_data']['cell'][0]))
                    self.lineEdit_y.setText(str(_textile_data_dict['raw_data']['cell'][1]))
                    _x_list = _textile_data_dict['raw_data']['x']
                    _y_list = _textile_data_dict['raw_data']['y']
                    for grp in [(_x_list, self.table_x), (_y_list, self.table_y)]:
                        for i in range(len(grp[0])):  # raw
                            try:
                                for j in range(10):
                                    _item = QTableWidgetItem(str(grp[0][i][j]))
                                    grp[1].setItem(i, j, _item)
                            except IndexError:
                                pass
                except:
                    pass

                try:
                    self.lineEdit_tension.setText(str(_textile_data_dict['property']['ctension']))
                    self.lineEdit_angle.setText(str(_textile_data_dict['property']['cangle']))
                    self.cBox_binding.setCurrentText(_textile_data_dict['property']['binding'])
                    self.cBox_art.setCurrentText(_textile_data_dict['property']['art'])
                    self.cBox_material.setCurrentText(_textile_data_dict['property']['material'])
                except:
                    pass

            try:
                if self._textile_selected[1] not in ["raw_data", "property"]:
                    self.edit_variant_name.setText(self._textile_selected[1])
                    self.edit_Ex.setText(str(_textile_data_dict[self._textile_selected[1]][0]))
                    self.edit_Ey.setText(str(_textile_data_dict[self._textile_selected[1]][1]))
                    self.edit_Cx.setText(str(_textile_data_dict[self._textile_selected[1]][2]))
                    self.edit_Cy.setText(str(_textile_data_dict[self._textile_selected[1]][3]))
            except:
                pass

    def _clean(self):
        self.edit_Ex.clear()
        self.edit_Ey.clear()
        self.edit_Cx.clear()
        self.edit_Cy.clear()
        self.edit_textile_name.clear()
        self.edit_variant_name.clear()
        self.lineEdit_x.clear()
        self.lineEdit_y.clear()
        self.table_x.clear()
        self.table_y.clear()
        self.table_x.setRowCount(20)
        self.table_x.setColumnCount(10)
        self.table_x.setHorizontalHeaderLabels(
            ['X [mm]', 'Ex [GPa]', 'Ey [GPa]', 'Cx [Nm²]', 'Cy [Nm²]', 'rx [mm]', 'ry [mm]', 'rz [mm]', 'cross [mm²]',
             'Qx [GPa]'])
        self.table_y.setRowCount(20)
        self.table_y.setColumnCount(10)
        self.table_y.setHorizontalHeaderLabels(
            ['Y [mm]', 'Ex [GPa]', 'Ey [GPa]', 'Cx [Nm²]', 'Cy [Nm²]', 'rx [mm]', 'ry [mm]', 'rz [mm]', 'cross [mm²]',
             'Qy [GPa]'])
        self.cBox_art.setCurrentIndex(0)
        self.cBox_material.setCurrentIndex(0)
        self.cBox_binding.setCurrentIndex(0)
        self.lineEdit_angle.clear()
        self.lineEdit_tension.clear()
        self.lineEdit_cross.clear()
        self.lineEdit_qx.clear()
        self.lineEdit_qy.clear()
        self.lineEdit_celly.clear()
        self.lineEdit_cellx.clear()
        self.lineEdit_cellz.clear()
        self.lineEdit_rx.clear()
        self.lineEdit_ry.clear()
        self.lineEdit_rz.clear()

    def _del_textile_clicked(self):
        _textile_database = load_pickle_data(self._textile_data_base_path)
        if self._textile_selected and _textile_database and self._textile_selected[0] in _textile_database.keys():
            del _textile_database[self._textile_selected[0]]

            update_pickled_data(path=self._textile_data_base_path, data_dict=_textile_database, without_check=True)
            self.__update_textile_tree()
            self._textile_selected.clear()

    def _add_textile_clicked(self):
        self.pb_save_textile.setDisabled(False)
        self.gb_add_model.setDisabled(False)
        self.gb_model_raw.setDisabled(False)
        self._clean()

    def _save_textile_clicked(self, is_new=True):
        if not self.edit_textile_name.text():
            QMessageBox.warning(self, "Warning", "No Textile Name defined!", QMessageBox.Ok)
            return

        if not self.lineEdit_x.text() or not self.lineEdit_y.text():
            QMessageBox.warning(self, "Warning", "Invalid Cell defined!", QMessageBox.Ok)
            return
        else:
            try:
                _cell_x = float(self.lineEdit_x.text())
                _cell_y = float(self.lineEdit_y.text())
            except ValueError:
                QMessageBox.warning(self, "Warning", "Cell Dimension should be float!", QMessageBox.Ok)
                return
        _name = str(self.edit_textile_name.text())
        _raw_data = dict()
        for table in [('x', self.table_x), ('y', self.table_y)]:
            _table = list()
            _data = list()
            for i in range(table[1].rowCount()):
                _data = list()
                for j in range(table[1].columnCount()):

                    try:
                        _data.append(float(table[1].item(i, j).text()))
                    except ValueError or AttributeError:
                        QMessageBox.warning(self, "Warning", "Invalid Input given!", QMessageBox.Ok)
                        return
                    except AttributeError:
                        pass
                if _data:
                    _table.append(_data)
            if _table:
                _raw_data.update({table[0]: _table})

        _reply = None

        try:
            if len(_raw_data['x']) != len(_raw_data['y']):
                _reply = QMessageBox.warning(self, "Warning", "Length of x and y is not the same, still save?",
                                             QMessageBox.Yes | QMessageBox.No)
        except KeyError:
            _reply = QMessageBox.warning(self, "Warning", "Length of x and y is not the same, still save?",
                                         QMessageBox.Yes | QMessageBox.No)

        if _reply == QMessageBox.No:
            return

        # feed properties

        if not all([self.cBox_art.currentIndex(), self.cBox_binding.currentIndex(), self.cBox_material.currentIndex()]):
            QMessageBox.warning(self, "Warning", "One of the properties is not specified!",
                                QMessageBox.Ok)

        _textile_art = self.cBox_art.currentText()
        _textile_material = self.cBox_material.currentText()
        _textile_binding = self.cBox_binding.currentText()
        _critical_angle = None
        _critical_tension = None

        try:
            if self.lineEdit_angle.text():
                _critical_angle = float(self.lineEdit_angle.text())
            else:
                QMessageBox.warning(self, "Warning", "Critical shear angle is not specified!",
                                    QMessageBox.Ok)

            if self.lineEdit_tension.text():
                _critical_tension = float(self.lineEdit_tension.text())
            else:
                QMessageBox.warning(self, "Warning", "Critical tension is not specified!",
                                    QMessageBox.Ok)
        except ValueError:
            QMessageBox.warning(self, "Warning", "One of the properties is not specified!",
                                QMessageBox.Ok)

        _raw_data.update({'cell': [_cell_x, _cell_y]})

        _property_data = {'material': _textile_material, 'binding': _textile_binding, 'art': _textile_art,
                          'cangle': _critical_angle, 'ctension': _critical_tension}

        _textile_dict = load_pickle_data(self._textile_data_base_path)
        _new_textile_dict = dict()
        if _textile_dict and _name in _textile_dict.keys():
            _textile_dict[_name].update({'raw_data': _raw_data,
                                        'property': _property_data})
            _new_textile_dict = _textile_dict
        else:
            _new_textile_dict.update({_name: {'raw_data': _raw_data,
                                              'property': _property_data}})

        update_pickled_data(self._textile_data_base_path, _new_textile_dict)

        self.__update_textile_tree()
        if is_new:
            self._echo(instance=self, msg="New Textile {} added.".format(self.edit_textile_name.text()))
        else:
            self._echo(instance=self, msg="Textile {} updated.".format(self.edit_textile_name.text()))
        self._clean()

    def _calc_querstress_clicked(self):

        if self.lineEdit_rx.text() and self.lineEdit_ry.text() and self.lineEdit_rz.text() and \
                self.lineEdit_cellx.text() and self.lineEdit_celly.text() and self.lineEdit_cross.text() and \
                self.lineEdit_angle.text():
            try:
                x = float(self.lineEdit_cellx.text())
                y = float(self.lineEdit_celly.text())

                rx = float(self.lineEdit_rx.text())
                ry = float(self.lineEdit_ry.text())
                rz = float(self.lineEdit_rz.text())

                c_angle = float(self.lineEdit_angle.text())
                qx, qy = calc_q(x, y, rx, ry, rz, c_angle)

                self.lineEdit_qx.setText(str(qx))
                self.lineEdit_qy.setText(str(qy))
            except ValueError:
                QMessageBox.warning(self, "Warning", "Data not be a number!", QMessageBox.Ok)
        else:

            QMessageBox.warning(self, "Warning", "Data not enough given!", QMessageBox.Ok)

    def _save_querstress_clicked(self):
        if not self.lineEdit_qx.text():
            QMessageBox.warning(self, "Warning", "qx unknown!", QMessageBox.Ok)
            return
        else:
            qx = self.lineEdit_qx.text()

        if not self.lineEdit_qy.text():
            QMessageBox.warning(self, "Warning", "qy unknown!", QMessageBox.Ok)
            return
        else:
            qy = self.lineEdit_qy.text()

        if not self.edit_textile_name.text():
            QMessageBox.warning(self, "Warning", "No Textile Name defined!", QMessageBox.Ok)
            return
        else:
            _textile_name = self.edit_textile_name.text()

        #try:

            _cell_x = []
            _cell_y = []

            for i in range(self.table_x.rowCount()):
                try:
                    _cell_x.append(self.table_x.item(i, 0).text())
                    _cell_y.append(self.table_y.item(i, 0).text())
                except AttributeError:
                    pass
            if self.lineEdit_cellx.text() in _cell_x:
                _row = _cell_x.index(self.lineEdit_cellx.text())
            else:
                QMessageBox.information(self, "Info", "The cell data %s does not exist, it will be fitted automatically" % _cell_x, QMessageBox.Ok)
                _row = self.__fitting_and_insert_data(float(self.lineEdit_cellx.text()), self.table_x)

            self.table_x.setItem(_row, 5, QTableWidgetItem(self.lineEdit_rx.text()))
            self.table_x.setItem(_row, 6, QTableWidgetItem(self.lineEdit_ry.text()))
            self.table_x.setItem(_row, 7, QTableWidgetItem(self.lineEdit_rz.text()))
            self.table_x.setItem(_row, 8, QTableWidgetItem(self.lineEdit_cross.text()))
            self.table_x.setItem(_row, 9, QTableWidgetItem(qx))

            if self.lineEdit_celly.text() in _cell_y:
                _row = _cell_y.index(self.lineEdit_celly.text())
            else:
                QMessageBox.information(self, "Info", "The cell data %s does not exist, it will be fitted automatically" % _cell_y, QMessageBox.Ok)
                _row = self.__fitting_and_insert_data(float(self.lineEdit_celly.text()), self.table_y)

            self.table_y.setItem(_row, 5, QTableWidgetItem(self.lineEdit_rx.text()))
            self.table_y.setItem(_row, 6, QTableWidgetItem(self.lineEdit_ry.text()))
            self.table_y.setItem(_row, 7, QTableWidgetItem(self.lineEdit_rz.text()))
            self.table_y.setItem(_row, 8, QTableWidgetItem(self.lineEdit_cross.text()))
            self.table_y.setItem(_row, 9, QTableWidgetItem(qy))

        #except AttributeError:
            pass

        self._save_textile_clicked(is_new=False)

    def _save_cell_clicked(self):
        QMessageBox.information(self, "Info", "Not implemented!", QMessageBox.Ok)

    def _del_cell_clicked(self):
        QMessageBox.information(self, "Info", "Not implemented!", QMessageBox.Ok)

    def _save_variant_clicked(self):
        if not self.edit_variant_name.text():
            QMessageBox.warning(self, "Warning", "No Variant Name defined!", QMessageBox.Ok)
            return
        else:
            _name = self.edit_variant_name.text()

        if not self.edit_Ex.text():
            QMessageBox.warning(self, "Warning", "No Ex given!", QMessageBox.Ok)
            return
        else:
            try:
                _ex = float(self.edit_Ex.text())
            except ValueError:
                QMessageBox.warning(self, "Warning", "Ex must be value!", QMessageBox.Ok)
                return

        if not self.edit_Ey.text():
            QMessageBox.warning(self, "Warning", "No Ey given!", QMessageBox.Ok)
            return
        else:
            try:
                _ey = float(self.edit_Ey.text())
            except ValueError:
                QMessageBox.warning(self, "Warning", "Ey must be value!", QMessageBox.Ok)
                return

        if not self.edit_Cx.text():
            QMessageBox.warning(self, "Warning", "No Cx given!", QMessageBox.Ok)
            return
        else:
            try:
                _cx = float(self.edit_Cx.text())
            except ValueError:
                QMessageBox.warning(self, "Warning", "Cx must be value!", QMessageBox.Ok)
                return

        if not self.edit_Cy.text():
            QMessageBox.warning(self, "Warning", "No Cy given!", QMessageBox.Ok)
            return
        else:
            try:
                _cy = float(self.edit_Cy.text())
            except ValueError:
                QMessageBox.warning(self, "Warning", "Cy must be value!", QMessageBox.Ok)
                return

        if not self.edit_textile_name.text():
            QMessageBox.warning(self, "Warning", "No Textile Name defined!", QMessageBox.Ok)
            return
        else:
            _textile_name = self.edit_textile_name.text()

        # here we must check whether the textile exists, if so, then first grasp the dict

        _textile_dict = load_pickle_data(self._textile_data_base_path)
        _new_textile_dict = dict()
        if _textile_dict and _textile_name in _textile_dict.keys():
            _textile_dict[_textile_name].update({_name: [_ex, _ey, _cx, _cy]})
            _new_textile_dict = _textile_dict

        else:
            _new_textile_dict.update({_textile_name: {_name: [_ex, _ey, _cx, _cy]}})

        update_pickled_data(path=self._textile_data_base_path, data_dict=_new_textile_dict)

        self.__update_textile_tree()
        self.edit_variant_name.clear()
        self.edit_Ex.clear()
        self.edit_Ey.clear()
        self.edit_Cx.clear()
        self.edit_Cy.clear()

    def _del_vaiant_cliecked(self):
        _name = self.edit_variant_name.text()
        if not self._textile_selected or not _name:
            QMessageBox.warning(self, "Warning", "No Variant selected!", QMessageBox.Ok)
            return

        if not self.edit_textile_name.text():
            QMessageBox.warning(self, "Warning", "No Textile Name defined!", QMessageBox.Ok)
            return

        _textile_name = self.edit_textile_name.text()

        _textile_data_dict = load_pickle_data(self._textile_data_base_path)

        if _textile_data_dict:
            if _textile_name in _textile_data_dict.keys():
                del _textile_data_dict[_textile_name][_name]
                update_pickled_data(self._textile_data_base_path, _textile_data_dict)

        self.__update_textile_tree()
        self.edit_variant_name.clear()
        self.edit_Ex.clear()
        self.edit_Ey.clear()
        self.edit_Cx.clear()
        self.edit_Cy.clear()

    @staticmethod
    def __get_fitting_data(y_name, tabel):
        _y_data_column = None
        _x_data = []
        _y_data = []
        for i in range(tabel.columnCount()):
            if y_name in tabel.horizontalHeaderItem(i).text():
                _y_data_column = i
                break
        for i in range(tabel.rowCount()):
            try:
                _x = float(tabel.item(i, 0).text())
                if _x:
                    _x_data.append(_x)
                if float(tabel.item(i, _y_data_column).text()):
                    _y_data.append(float(tabel.item(i, _y_data_column).text()))
            except ValueError:
                pass
            except AttributeError:
                pass
        return _x_data, _y_data

    def _fit_data_and_plot(self):
        if not self.comboBox_data_x.currentIndex() and not self.comboBox_data_y.currentIndex():
            QMessageBox.warning(self, "Warning", "No valid fitting condition chosen!", QMessageBox.Ok)
            return

        if not self.edit_textile_name.text():
            QMessageBox.warning(self, "Warning", "Textile not chosen!", QMessageBox.Ok)
            return

        # then we grasp the data from table

        if self.comboBox_data_x.currentText() == 'X':
            _x_data, _y_data = self.__get_fitting_data(self.comboBox_data_y.currentText(), self.table_x)
        else:
            _x_data, _y_data = self.__get_fitting_data(self.comboBox_data_y.currentText(), self.table_y)

        if not _y_data or not _y_data:
            QMessageBox.warning(self, "Warning", "There are no data to fit!", QMessageBox.Ok)
            return

        _func = fitted_data_func(fit_data(_x_data, _y_data, self.spinBox_deg.value()))
        _x_max = self.hSlider_plot.value()
        if _x_max < _x_data[len(_x_data) - 1]:
            _x_max = _x_data[len(_x_data) - 1]
        _plot_x = np.linspace(int(_x_data[0]), _x_max)
        self.plot_figure.clear()
        plot_ax = self.plot_figure.add_subplot(111)
        plot_ax.grid(True)
        plot_ax.plot(_x_data, _y_data, '.', _plot_x, _func(_plot_x), '-')
        self.plot_canvas.draw()

    def __fitting_and_insert_data(self, data, table):

        _func_list = []
        _x_data = []
        for i in range(1, self.comboBox_data_y.count()):
            _x_data, _y_data = self.__get_fitting_data(self.comboBox_data_y.itemText(i), table)
            _func_list.append(fitted_data_func(fit_data(_x_data, _y_data, self.spinBox_deg.value())))
        _row = 0
        for i in range(table.rowCount() - 1):
            try:
                if (float(table.item(i, 0).text()) < data < float(table.item(i + 1, 0).text())) or \
                        (float(table.item(i, 0).text()) != 0. and float(table.item(i + 1, 0).text()) == 0.):
                    _row = i + 1
                    break
            except AttributeError:
                _row = i + 1
        table.insertRow(_row)
        table.setItem(_row, 0, QTableWidgetItem(str(data)))

        for j in range(len(_func_list)):
            table.setItem(_row, j + 1, QTableWidgetItem(str(_func_list[j](data))))
        return _row

    def _pb_insert_data_clicked(self):

        if not self.lineEdit_new_data.text():
            QMessageBox.warning(self, "Warning", "No new Data given!", QMessageBox.Ok)
            return
        try:
            _data_to_fit = float(self.lineEdit_new_data.text())
            if self.comboBox_data_x.currentText() == 'X':
                self.__fitting_and_insert_data(_data_to_fit, self.table_x)
            else:
                self.__fitting_and_insert_data(_data_to_fit, self.table_y)

        except ValueError:
            QMessageBox.warning(self, "Warning", "Data must be a number!", QMessageBox.Ok)
            return
