
import sys, os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class DrapeImageLabel(QLabel):
    def __init__(self, parent=None):
        super(DrapeImageLabel, self).__init__(parent)
        self._raw_image = None
        self._pixel_map = None

    def set_image(self, q_image):
        self._raw_image = q_image
        self._pixel_map = QPixmap.fromImage(q_image)
        self.update_image()

    def update_image(self):
        if self._pixel_map:
            self.setPixmap(self._pixel_map.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))

    def resizeEvent(self, QResizeEvent):
        self.update_image()


class DrapeInteractScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(DrapeInteractScene, self).__init__(parent)
        self._start = QPointF()
        self._current_rect_item = None

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            if type(self.itemAt(event.scenePos(), QTransform())) is QGraphicsRectItem:
                self.removeItem(self.itemAt(event.scenePos(), QTransform()))

        else:
            if type(self.itemAt(event.scenePos(), QTransform())) is not QGraphicsRectItem:
                self._current_rect_item = QGraphicsRectItem()
                self._current_rect_item.setBrush(QColor(200, 10, 10, 100))
                self._current_rect_item.setFlag(QGraphicsItem.ItemIsMovable, True)

                self.addItem(self._current_rect_item)
                self._start = event.scenePos()
                r = QRectF(self._start, self._start)
                self._current_rect_item.setRect(r)
        super(DrapeInteractScene, self).mousePressEvent(event)


    def mouseMoveEvent(self, event):
        if self._current_rect_item is not None:
            #if event.scenePos().x() <= self.sceneRect().width() and event.scenePos().y() <= self.sceneRect().height():
            r = QRectF(self._start, event.scenePos()).normalized()
            self._current_rect_item.setRect(r)

        super(DrapeInteractScene, self).mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        self._current_rect_item = None
        super(DrapeInteractScene, self).mouseReleaseEvent(event)


class DrapeInteractiveView(QGraphicsView):
    def __init__(self, parent=None, bg_image=None):
        super(DrapeInteractiveView, self).__init__(parent)
        self._raw_image = None
        self._pixel_map = None
        self._pixelmapitem = None
        self.setScene(DrapeInteractScene(parent=self))

        if bg_image:
            self.set_background_image(q_image=bg_image)

    def set_background_image(self, q_image):
        self._raw_image = q_image
        self._pixel_map = QPixmap.fromImage(q_image)
        self._pixelmapitem = QGraphicsPixmapItem(self._pixel_map)
        if self.scene():
            self.scene().addItem(self._pixelmapitem)

    def resizeEvent(self, QResizeEvent):
        self.scene().setSceneRect(self.x(), self.y(), int(self.width() * 0.95), int(self.height() * 0.95))
        self._pixel_map = self._pixel_map.scaled(self.size() * 0.95, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self._pixelmapitem.setPixmap(self._pixel_map)
        super(DrapeInteractiveView, self).resizeEvent(QResizeEvent)

    def clean_all_rects(self):
        _scene = self.scene()
        for item in _scene.items():
            if type(item) == QGraphicsRectItem:
                _scene.removeItem(item)

    def get_all_rects(self):
        _scene = self.scene()
        _rects = []
        for item in _scene.items():
            if type(item) == QGraphicsRectItem:
                _rects.append(item.rect())
        return _rects, _scene.sceneRect(), self._raw_image.size()






























