from PySide2.QtCore import QSize, QLineF, QRect, Qt, QMargins
from PySide2.QtGui import QPen, QBrush, QColor, QTransform
from PySide2.QtWidgets import QGraphicsScene, QGraphicsItemGroup, QGraphicsItem, QMenu, QAction

from models.constants import MimeType, SelectConnect
from models.element import Process

GRID_WIDTH = 100
GRID_HEIGHT = 100
MIN_GRID_MARGIN = 10
DROP_INDICATOR_SIZE = 5

PROCESS_SIZE = 80


class SectionScene(QGraphicsScene):
    def __init__(self, section, model, process_cores):
        super().__init__()
        self._grid_size = QSize(GRID_WIDTH, GRID_HEIGHT)
        self._drop_indicator = self.init_drop_indicator()
        self._process_items = QGraphicsItemGroup()
        self._commodity_items = QGraphicsItemGroup()
        self._bounding_rect = BoundingRect(model.process_list, model.commodity_list)
        self._clicked_item = None
        self._item_mouse_offset = None
        self._items_border = QRect()
        self._grid_border = QRect()
        self._section = section
        self._model = model
        self._cores = process_cores

        self._edit_mode = SelectConnect.SELECT
        self._draft_mode = False

        self.init_scene()

    @property
    def edit_mode(self):
        return self._edit_mode

    @edit_mode.setter
    def edit_mode(self, value):
        if value in SelectConnect:
            self._edit_mode = value
            if value == SelectConnect.SELECT:
                self._process_items.setFlag(QGraphicsItem.ItemIsMovable)
            else:
                self._process_items.setFlag(QGraphicsItem.ItemIsMovable, False)
        else:
            raise TypeError

    @property
    def draft_mode(self):
        return self._draft_mode

    @draft_mode.setter
    def draft_mode(self, value):
        if value in [True, False]:
            self._draft_mode = value
            self._process_items.setFlag(QGraphicsItem.ItemIsMovable, value)
        else:
            raise TypeError

    def init_scene(self):
        """initialize content of scene based on list of elements"""
        for commodity in self._model.commodity_list:
            if commodity.section == self._section:
                self.draw_commodity(commodity)
        for process in self._model.process_list:
            if process.core.section == self._section:
                self.draw_process(process)
                self.draw_connections(process)

        self._bounding_rect.update()

    def draw_commodity(self, commodity):
        # todo implement draw commodity
        pass

    def draw_process(self, process):
        """create process item and add to scene & process items list"""
        process_item = ProcessItem(process.core.icon)
        process_item.setData(0, process)
        process_item.setPos(process.coordinate)
        process_item.setFlag(QGraphicsItem.ItemIsMovable)

        self._process_items.prepareGeometryChange()
        self._process_items.addToGroup(process_item)
        self.addItem(process_item)

    def delete_process(self, item):
        self._model.process_list.remove(item.data(0))
        # todo remove connections
        self._process_items.removeFromGroup(item)
        self.removeItem(item)

        self._bounding_rect.update()

    def draw_connections(self, process):
        # todo implement draw connections
        pass

    def init_drop_indicator(self):
        rect = QRect(-DROP_INDICATOR_SIZE/2, -DROP_INDICATOR_SIZE/2, DROP_INDICATOR_SIZE, DROP_INDICATOR_SIZE)
        brush = QBrush(Qt.darkBlue)
        pen = QPen(Qt.darkBlue, 1)
        ellipse = self.addEllipse(rect, pen, brush)
        ellipse.setVisible(False)
        return ellipse

    def disable_drop_indicator(self):
        self._drop_indicator.setX(-DROP_INDICATOR_SIZE / 2)
        self._drop_indicator.setY(-DROP_INDICATOR_SIZE / 2)
        self._drop_indicator.setVisible(False)
        self.update()

    def align_drop_indicator(self, point):
        """align the drop indicator to grid while mouse movement"""
        # move drop indicator only within grid boundaries
        if not self.get_grid_border(-MIN_GRID_MARGIN).contains(point.toPoint()):
            self._drop_indicator.setVisible(False)
            return

        # calculate the nearby position of grid interceptions
        grid_x = (round(point.x() / self._grid_size.width() / 2 - 1/2) * 2 + 1) * self._grid_size.width()
        grid_y = round(point.y() / self._grid_size.height()) * self._grid_size.height()

        # move drop indicator to grid interception
        self._drop_indicator.setX(grid_x)
        self._drop_indicator.setY(grid_y)
        self._drop_indicator.setVisible(True)
        self.update()

    def get_grid_border(self, margin=0):
        def get_raster_length(length, raster):
            return (int((length + MIN_GRID_MARGIN + raster/2) / raster) - 1/2) * raster

        left = get_raster_length(self.sceneRect().left(), self._grid_size.width())
        right = get_raster_length(self.sceneRect().right(), self._grid_size.width())
        top = get_raster_length(self.sceneRect().top(), self._grid_size.height())
        bottom = get_raster_length(self.sceneRect().bottom(), self._grid_size.height())

        return QRect(left, top, right-left, bottom-top).marginsAdded(QMargins(margin, margin, margin, margin))

    def drawBackground(self, painter, rect):
        if self.draft_mode:
            border_rect = self.get_grid_border()
            grid_rect = self.get_grid_border(-self._grid_size.width()/2)

            line_list = []
            # horizontal grid lines
            for line_coordinate in range(grid_rect.top(), border_rect.bottom(), self._grid_size.height()):
                line_list.append(QLineF(border_rect.left(), line_coordinate,
                                        border_rect.right(), line_coordinate))
            # vertical process lines
            left_border = int((grid_rect.left() + self._grid_size.width()) / (2 * self._grid_size.width())) * \
                self._grid_size.width() * 2 - self._grid_size.width()
            for line_coordinate in range(left_border, border_rect.right(), self._grid_size.width()*2):
                line_list.append(QLineF(line_coordinate, border_rect.top(),
                                        line_coordinate, border_rect.bottom()))

            # vertical commodity lines
            left_border = int(grid_rect.left() / (2 * self._grid_size.width())) * self._grid_size.width() * 2
            for line_coordinate in range(left_border, border_rect.right(), self._grid_size.width() * 2):
                line_list.append(QLineF(line_coordinate - 1, border_rect.top(),
                                        line_coordinate - 1, border_rect.bottom()))
                line_list.append(QLineF(line_coordinate + 1, border_rect.top(),
                                        line_coordinate + 1, border_rect.bottom()))

            painter.setPen(QPen(Qt.lightGray, 1))
            painter.drawLines(line_list)

        super().drawBackground(painter, rect)

    def mousePressEvent(self, event):
        # ignore right button click
        if event.button() == Qt.RightButton:
            return

        self._clicked_item = self.itemAt(event.scenePos(), QTransform())
        if self.draft_mode & (self.edit_mode == SelectConnect.SELECT):
            if isinstance(self._clicked_item, ProcessItem):
                self._clicked_item.setOpacity(0.5)
                self._drop_indicator.setPos(self._clicked_item.pos())
                self._drop_indicator.setVisible(True)
                # set offset between mouse and center of item for mouseMoveEvent
                self._item_mouse_offset = self._clicked_item.mapFromScene(event.scenePos())
            else:
                self._clicked_item = None

    def mouseMoveEvent(self, event):
        if self.draft_mode & (self.edit_mode == SelectConnect.SELECT):
            if self._clicked_item:
                # move drop indicator along grid and process item according to mouse position
                self.align_drop_indicator(event.scenePos() - self._item_mouse_offset)
                self._clicked_item.setPos(event.scenePos() - self._item_mouse_offset)

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.draft_mode & (self.edit_mode == SelectConnect.SELECT):
            if self._clicked_item:
                self._clicked_item.setOpacity(1.0)
                # remove clicked item from collision list with drop indicator
                collision_items = self.collidingItems(self._drop_indicator)
                if collision_items:
                    collision_items.remove(self._clicked_item)
                # avoid placement if colliding with other items
                if not collision_items:
                    self._clicked_item.setPos(self._drop_indicator.scenePos())
                    self._clicked_item.data(0).coordinate = self._drop_indicator.pos()
                    self._bounding_rect.update()
                self.disable_drop_indicator()
                self._clicked_item = None

        super().mouseReleaseEvent(event)

    def dragEnterEvent(self, event):
        pass

    def dragLeaveEvent(self, event):
        self.disable_drop_indicator()

    def dragMoveEvent(self, event):
        if self.draft_mode & (self.edit_mode == SelectConnect.SELECT):
            self.align_drop_indicator(event.scenePos())

    def dropEvent(self, event):
        """add new process to list and process item to scene"""
        # prevent process placement if item exists there
        if len(self.collidingItems(self._drop_indicator)) > 0:
            return

        core_name = event.mimeData().data(MimeType.PROCESS_CORE.value)
        process_core = list(filter(lambda element: element.name == core_name, self._cores))[0]

        # define name based on process core and existing names
        remainder_name = [process.name.split(process_core.name)[1].strip()
                          for process in self._model.process_list if process_core.name in process.name]
        if not remainder_name:
            process_name = process_core.name
        elif max(remainder_name).isdigit():
            process_name = process_core.name + " " + str(int(max(remainder_name)) + 1)
        else:
            process_name = process_core.name + " 1"

        # create new process based on process core and add to element list
        process = Process(process_name, self._drop_indicator.pos(), process_core)
        self._model.add_process(process)

        # create process item and connections
        self.draw_process(process)
        # todo draw connections

        self._bounding_rect.update()

        self.disable_drop_indicator()

    def contextMenuEvent(self, event):
        """context menu to interact with process items - delete item"""
        # prevent context menu of scene not in draft mode
        if not self.draft_mode:
            return

        # open context menu only for process items
        self._clicked_item = self.itemAt(event.scenePos(), QTransform())
        if self._clicked_item:
            if isinstance(self._clicked_item, ProcessItem):
                menu = QMenu()
                delete_action = QAction("Delete", None)
                delete_action.triggered.connect(
                    lambda: self.delete_process(self._clicked_item))
                menu.addAction(delete_action)
                menu.exec_(event.screenPos())
                self._clicked_item = None

    # todo extend/reduce sceneRect with position of elements
    def setSceneRect(self, rect):
        """set sceneRect to view boundaries if necessary space is less"""
        super().setSceneRect(self._bounding_rect.scene_rect(rect, 2*MIN_GRID_MARGIN))


class BoundingRect(QRect):
    """bounding rectangle including processes and commodities"""
    def __init__(self, process_list, commodity_list):
        super().__init__(0, 0, 0, 0)
        self._processes = process_list
        self._commodities = commodity_list

    def update(self):
        # todo add additional space for future expansion
        # set rect to initial value if no items exist
        if not self._processes:
            if not self._commodities:
                self.setRect(0, 0, 0, 0)
                return

        process_x_coordinates = list(map(lambda process: process.coordinate.x(), self._processes))
        process_y_coordinates = list(map(lambda process: process.coordinate.y(), self._processes))
        commodity_x_coordinates = list(map(lambda commodity: commodity.coordinate.x(), self._commodities))
        commodity_x_coordinates.extend([min(process_x_coordinates) - PROCESS_SIZE/2,
                                        max(process_x_coordinates) + PROCESS_SIZE/2])
        left_bound = min(commodity_x_coordinates)
        right_bound = max(commodity_x_coordinates)
        top_bound = min(process_y_coordinates) - PROCESS_SIZE/2
        bottom_bound = max(process_y_coordinates) + PROCESS_SIZE/2

        self.setRect(left_bound, top_bound, right_bound-left_bound, bottom_bound-top_bound)

    def scene_rect(self, other, margin):
        """define scene rectangle based on bounding rectangle with margin and other rectangle"""
        if not isinstance(other, QRect):
            raise TypeError

        scene_rect = self.marginsAdded(QMargins(margin, margin, margin, margin))
        # bounding rectangle of items within other rectangle
        if scene_rect.width() < other.width():
            # left border of items is within left border of other rectangle
            if other.left() < scene_rect.left():
                width_difference = other.width() - scene_rect.width()
                scene_rect.moveLeft(scene_rect.left() - width_difference/2)
            scene_rect.setWidth(other.width())
        if scene_rect.height() < other.height():
            if other.top() < scene_rect.top():
                height_difference = other.height() - scene_rect.height()
                scene_rect.moveTop(scene_rect.top() - height_difference/2)
            scene_rect.setHeight(other.height())

        return scene_rect


# todo create QGraphicsItem class for process
class ProcessItem(QGraphicsItem):
    """create rounded rectangle with icon"""

    def __init__(self, icon):
        super().__init__()
        self._icon = icon

    def boundingRect(self):
        return QRect(-PROCESS_SIZE/2, -PROCESS_SIZE/2, PROCESS_SIZE, PROCESS_SIZE)

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(QColor(0, 90, 158)))
        painter.setPen(QPen(QColor(0, 90, 158)))
        painter.drawRoundedRect(self.boundingRect(), 10, 10)
        painter.setBrush(QBrush())
        icon_rect = QRect(option.rect.top()/2, option.rect.left()/2, option.rect.width()/2, option.rect.height()/2)
        painter.drawPixmap(icon_rect, self._icon.pixmap(option.rect.size()/2))

# todo create QGraphicsItem class for commodity
