from qtpy import QtWidgets, QtGui, QtCore

from ._qt_utils import make_widget_property
from ..renderer import QtRenderer
from ...render_context import RenderContext

import qtawesome


class GroupItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, tree, group_name, group_column_name):
        super().__init__(parent)

        self._tree = tree
        self._group_column_name = group_column_name

        manager = self._tree._table_manager

        if manager.get_auto_expand_groups(None):
            self.setExpanded(True)
        self.setFirstColumnSpanned(True)

        self.setText(0, group_name)

        self._NO_ICON = QtGui.QIcon()
        self._column_icon_name = self._tree._table_manager.get_column_icon_name(
            group_column_name
        )
        self._group_icon_name = self._tree._table_manager.get_column_group_icon_name(
            group_column_name, fallback_to_icon=False
        )
        icon_name = None
        if self._group_icon_name is not None:
            icon_name = self._group_icon_name
        elif self._column_icon_name is not None:
            icon_name = self._column_icon_name
        if icon_name is not None:
            self.setIcon(0, qtawesome.icon(icon_name))

    def get_item(self):
        return None

    def use_group_icon(self, b):
        if b:
            if self._group_icon_name is not None:
                self.setIcon(0, qtawesome.icon(self._group_icon_name))
            else:
                self.setIcon(0, self._NO_ICON)
        else:
            if self._column_icon_name is not None:
                self.setIcon(0, qtawesome.icon(self._column_icon_name))
            else:
                self.setIcon(0, self._NO_ICON)

    def apply_filter(self, filter, use_filter):
        hide_me = True
        for i in range(self.childCount()):
            item = self.child(i)
            visible = item.apply_filter(filter, use_filter)
            if visible:
                hide_me = False
        self.setHidden(hide_me)
        return not hide_me


class TableItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent, tree, item):
        super().__init__(parent)

        self._NO_ICON = QtGui.QIcon()

        self._tree = tree
        self._column_labels = self._tree._table_manager._column_labels
        self._item = item

        self._cell_texts = []
        self._cell_icons = []
        self._cell_bg_brushes = []
        self._cell_fg_brushes = []

        self._update_cells()
        self._update_display()

    def get_item(self):
        return self._item

    def _update_cells(self):
        self._cell_texts = []
        self._cell_icons = []
        self._cell_bg_brushes = []
        self._cell_fg_brushes = []

        for column in self._column_labels:
            cell = self._item.get(column, None)
            if not isinstance(cell, dict):
                if cell is None:
                    self._cell_texts.append("Missing Cell !")
                else:
                    self._cell_texts.append(str(cell))
                self._cell_icons.append(self._NO_ICON)
                self._cell_bg_brushes.append(None)
                self._cell_fg_brushes.append(None)
                continue

            text = cell.get("display")
            if text is None:
                try:
                    text = str(cell["value"])
                except KeyError:
                    text = "! NO VALUE !"

            try:
                icon_name = cell["icon"]
            except KeyError:
                icon = self._NO_ICON
            else:
                try:
                    icon = qtawesome.icon(icon_name)
                except Exception:
                    print(f"Warning: could not create icon with name {icon_name} !")
                    icon = self._NO_ICON

            bg_color = None
            bg_brush = None
            try:
                bg_color = cell["background_color"]
            except KeyError:
                try:
                    bg_color = cell["background-color"]
                except KeyError:
                    bg_color = None
            if bg_color is not None:
                bg_brush = QtGui.QBrush(QtGui.QColor(bg_color))

            fg_color = None
            fg_brush = None
            try:
                fg_color = cell["foreground_color"]
            except KeyError:
                try:
                    fg_color = cell["foreground-color"]
                except KeyError:
                    fg_color = None
            if fg_color is not None:
                fg_brush = QtGui.QBrush(QtGui.QColor(fg_color))

            self._cell_texts.append(text)
            self._cell_icons.append(icon)
            self._cell_bg_brushes.append(bg_brush)
            self._cell_fg_brushes.append(fg_brush)

    def _update_display(self):
        for i in range(len(self._column_labels)):
            self.setText(i, self._cell_texts[i])

            icon = self._cell_icons[i]
            self.setIcon(i, icon)

            bg_brush = self._cell_bg_brushes[i]
            if bg_brush is not None:
                self.setBackground(i, bg_brush)

            fg_brush = self._cell_fg_brushes[i]
            if fg_brush is not None:
                self.setForeground(i, fg_brush)

    def match_filter(self, filter):
        for i in range(len(self._column_labels)):
            if filter and filter.lower() in self.text(i).lower():
                return True
        return False

    def apply_filter(self, filter, use_filter):
        if not filter or not use_filter:
            self.setHidden(False)
            return True
        visible = self.match_filter(str(filter))
        self.setHidden(not visible)
        return visible


class ViewManager(object):
    """
    A class to manage item view properties and applying them.

    Note that all property getters and setters have a context
    argument we dont use. This is needed by the property system
    that will call them with a context.
    Dont fool you into thinking this is not intentionnal ;)
    """

    def __init__(self, context, current_item_state, selected_items_state):
        super().__init__()
        self._context = context

        # We can't set the tree in the constructor bc
        # we need to register property before building
        # the actual widget.
        # When the widget is ready, `set_tree()` will be
        # called, which will call `update_all()`...
        self._tree = None

        self._icon_size = 32

        self._columns = []
        self._column_labels = []

        self._multiple_selection = False
        self._current_item_state = current_item_state
        self._selected_items_state = selected_items_state

        self._items = []
        self._group_by = []
        self._auto_group_separator = None
        self._auto_expand_groups = True

        self._filter = None
        self._use_filter = False

        # Register properties before doing anything else:
        self.register_properties(context)

    def register_properties(self, context):
        context.register_property("icon_size", self.get_icon_size, self.set_icon_size)
        context.register_property("columns", self.get_columns, self.set_columns)
        context.register_property("items", self.get_items, self.set_items)
        context.register_property(
            "multiple_selection",
            self.get_multiple_selection,
            self.set_multiple_selection,
        )
        context.register_property("group_by", self.get_group_by, self.set_group_by)
        context.register_property(
            "auto_group_separator",
            self.get_auto_group_separator,
            self.set_auto_group_separator,
        )
        context.register_property(
            "auto_expand_groups",
            self.get_auto_expand_groups,
            self.set_auto_expand_groups,
        )
        context.register_property(
            "use_filter", self.get_use_filter, self.set_use_filter
        )
        context.register_property("filter", self.get_filter, self.set_filter)

    def set_tree(self, tree):
        tree._table_manager = self
        self._tree = tree

        self._tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._tree.customContextMenuRequested.connect(self._on_popup_request)
        if self._current_item_state is not None:
            self._tree.currentItemChanged.connect(self._on_curernt_item_changed)
        if self._selected_items_state is not None:
            self._tree.itemSelectionChanged.connect(self._on_selection_changed)
        self.apply_all()

    def _on_popup_request(self, pos):
        ti = self._tree.itemAt(pos)
        item = ti.get_item()
        if item is None:
            return
        col_index = self._tree.header().logicalIndexAt(pos.x())
        column = self._get_column_at(col_index)
        try:
            menu_trigger_state = column.get("menu_trigger_state")
        except AttributeError:  # when column is just a string
            menu_trigger_state = None
        if menu_trigger_state is not None:
            # this will show the popup:
            self._context.set_state(menu_trigger_state, True)

    def _on_selection_changed(self):
        items = [ti.get_item() for ti in self._tree.selectedItems()]
        # remove group items:
        items = [i for i in items if i is not None]
        self._context.set_state(self._selected_items_state, items)

    def _on_curernt_item_changed(self, new, old):
        item = new.get_item()
        self._context.set_state(self._current_item_state, item)

    def apply_all(self):
        self.apply_icon_size()
        self.apply_columns()
        self.apply_multiple_selection()
        self.apply_items()
        self.apply_filter()

    # ICON SIZE

    def apply_icon_size(self):
        if self._tree is None:
            # not ready yet
            return
        self._tree.setIconSize(QtCore.QSize(self._icon_size, self._icon_size))

    def get_icon_size(self, context):
        return self._icon_size

    def set_icon_size(self, context, size):
        self._icon_size = size
        self.apply_icon_size()

    # COLUMNS

    def apply_columns(self):
        if self._tree is None:
            # not yet ready...
            return
        labels = []
        hiddens = []
        for column in self._columns:
            try:
                labels.append(column["label"])
            except TypeError:
                labels.append(str(column))
                hiddens.append(False)
            except KeyError:
                labels.append("! missing 'label' !")
            else:
                hiddens.append(column.get("hidden", False))
        self._tree.setHeaderLabels(labels)

        header = self._tree.header()
        for i, hidden in enumerate(hiddens):
            header.setSectionHidden(i, hidden)

        # store it, TableItem will use it:
        self._column_labels = labels

    def set_columns(self, context, columns):
        self._columns = columns
        self.apply_columns()

    def get_columns(self, context):
        return self._columns

    def _get_column_at(self, index):
        return self._columns[index]

    def _get_column_info(self, column_name, info_name):
        for column in self._columns:
            try:
                label = column["label"]
            except TypeError:
                label = column
            if label == column_name:
                try:
                    return column[info_name]
                except (TypeError, KeyError):
                    return None
        return None

    def get_column_icon_name(self, column_name):
        return self._get_column_info(column_name, "icon")

    def get_column_group_icon_name(self, column_name, fallback_to_icon=True):
        icon_name = self._get_column_info(column_name, "group_icon")
        if icon_name is None and fallback_to_icon:
            icon_name = self._get_column_info(column_name, "icon")
        return icon_name

    # ITEMS

    def apply_items(self):
        """
        (re)Create all items in the table using `items` and `group_by`.
        """
        if self._tree is None:
            # not ready yet
            return
        self._tree.clear()

        group_items = {}
        gi = None
        auto_group_sep = self.get_auto_group_separator(context=None)
        for item in self._items or []:
            parent = self._tree
            if self._group_by:
                group_namespace = ""
                for column in self._group_by:
                    try:
                        cell = item[column]
                    except KeyError:
                        parent = self._tree
                    else:
                        if isinstance(cell, dict):
                            group_name = cell.get("display")
                            if group_name is None:
                                group_name = str(cell["value"])
                        else:
                            group_name = cell
                        if auto_group_sep:
                            # This is to avoid an first empy group when
                            # the value starts with the separator (like first
                            # slash in a path...)
                            # We could skip all empty group names, but I'm not
                            # sure someone won't ever want to have empty group
                            # names on purpose. So for now let's assume the item
                            # will be cleaned up if empty group name needs to be
                            # avoided...
                            group_name = group_name.lstrip(auto_group_sep)
                            # now we can split into group names:
                            group_name_parts = group_name.split(auto_group_sep)
                        else:
                            group_name_parts = [group_name]
                        for group_name_part in group_name_parts:
                            namespaced_group = group_namespace + "/" + group_name_part
                            try:
                                gi = group_items[namespaced_group]
                            except KeyError:
                                gi = GroupItem(
                                    parent, self._tree, group_name_part, column
                                )
                                group_items[namespaced_group] = gi
                            parent = gi
                            group_namespace = namespaced_group
                        # last group for each column uses the column icon:
                        gi.use_group_icon(False)
            item = TableItem(parent, self._tree, item)

    def get_items(self, context):
        return self._items

    def set_items(self, context, items):
        self._items = items
        self.apply_items()

    # MULTIPLE SELECTION

    def apply_multiple_selection(self):
        if self._tree is None:
            # not ready yet
            return
        if self._multiple_selection:
            self._tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        else:
            self._tree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    def get_multiple_selection(self, context):
        return self._multiple_selection

    def set_multiple_selection(self, context, b):
        self._multiple_selection = b
        self.apply_multiple_selection()

    # GROUP BY

    def get_group_by(self, context):
        return self._group_by

    def set_group_by(self, context, group_by):
        self._group_by = group_by
        self.apply_items()

    # AUTO GROUP SEPARATOR

    def get_auto_group_separator(self, context):
        return self._auto_group_separator

    def set_auto_group_separator(self, context, separator):
        self._auto_group_separator = separator
        self.apply_items()

    # AUTO EXPAND GROUPS

    def get_auto_expand_groups(self, context):
        return self._auto_expand_groups

    def set_auto_expand_groups(self, context, b):
        self._auto_expand_groups = bool(b)
        # There's no apply here, this only affects the default
        # state of the table...

    # FILTER

    def apply_filter(self):
        if self._tree is None:
            # not yet ready
            return
        root = self._tree.invisibleRootItem()
        for i in range(root.childCount()):
            item = root.child(i)
            item.apply_filter(self._filter, self._use_filter)

    def get_filter(self, context):
        return self._filter

    def set_filter(self, context, filter):
        self._filter = str(filter)
        self.apply_filter()

    # USE FILTER

    def get_use_filter(self, context):
        return self._use_filter

    def set_use_filter(self, context, use_filter):
        self._use_filter = bool(use_filter)
        self.apply_filter()


@QtRenderer.register
def ItemView(context: RenderContext, params: QtRenderer.schema.ItemView):
    schema = QtRenderer.schema

    current_item_state = schema._namespaces.get_state_key(
        context, params.current_item_state
    )
    selected_items_state = schema._namespaces.get_state_key(
        context, params.selected_items_state
    )
    view_manager = ViewManager(
        context,
        current_item_state,
        selected_items_state,
    )

    # simple qt properties:
    make_widget_property(
        "decorated_root", bool, context, qproperty_name="rootIsDecorated"
    )
    make_widget_property("header_hidden", bool, context, qproperty_name="headerHidden")
    make_widget_property("sortable", bool, context, qproperty_name="sortingEnabled")

    #
    # Content
    #
    with params.widget as view:
        view.widget_class = "QTreeWidget"
        schema.set_or_bind(context, "decorated_root", params.decorated_root, False)
        schema.set_or_bind(context, "header_hidden", params.header_hidden, False)
        schema.set_or_bind(context, "icon_size", params.icon_size, 24)
        schema.set_or_bind(context, "columns", params.columns, [])
        schema.set_or_bind(context, "sortable", params.sortable, None)
        schema.set_or_bind(context, "filter", params.filter, None)
        schema.set_or_bind(context, "use_filter", params.use_filter, False)
        schema.set_or_bind(context, "group_by", params.group_by, [])
        schema.set_or_bind(
            context, "auto_group_separator", params.auto_group_separator, "/"
        )
        schema.set_or_bind(
            context, "auto_expand_groups", params.auto_expand_groups, True
        )
        schema.set_or_bind(context, "items", params.items, [])
        schema.set_or_bind(
            context, "multiple_selection", params.multiple_selection, False
        )

    tree = context.render(view)["widget"]
    view_manager.set_tree(tree)
