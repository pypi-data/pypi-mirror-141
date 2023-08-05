from __future__ import annotations
from functools import partial

from qtpy import QtWidgets, QtGui, QtCore
import qtawesome

from ...enums import _EnumMixin
from ...default.schema import DefaultSchema
from ...models import ParamsModel
from ...models.root_schema import RootSchema


COMPONENT_ICON = "fa5s.cube"
SCHEMA_ICON = "fa5s.cubes"
FAV_ICON = "fa5s.star"
MATCH_ICON = "fa5s.search"
PARAM_GROUP_ICON = "fa.list-ul"
PARAM_SET_ICON = "fa.dot-circle-o"
PARAM_DEFAULT_ICON = "fa.circle-o"


class _BaseItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, tree: "ComponentTree", parent):
        super().__init__(parent)
        self._tree = tree
        self._hide_defaults = True

    def _build(self):
        raise NotImplementedError

    def _update(self):
        raise NotImplementedError

    def sort_children(self):
        pass

    def get_component_item(self):
        raise NotImplementedError()

    def get_component_type(self):
        return self.get_component_item().get_component_type()

    def apply_edit(self, column):
        # Default is to do nothing bc non editable items
        # dont have the flag which let the user edit them...
        pass

    def get_ui(self):
        return None

    def as_params(self):
        raise NotImplementedError()

    def get_menu(self):
        raise NotImplementedError()

    def set_hide_defaults(self, b):
        self._hide_defaults = b
        self._apply_hide_defaults()

    def _apply_hide_defaults(self):
        self._update()
        for i in range(self.childCount()):
            child = self.child(i)
            if child.get_component_item() is self.get_component_item():
                child.set_hide_defaults(self._hide_defaults)

    def _get_param_group_menu(self):
        menu = QtWidgets.QMenu()

        #
        #   PARAMS
        #
        params_menu = menu.addMenu("Params")
        params_menu.setIcon(qtawesome.icon("fa.dot-circle-o"))

        a = params_menu.addAction("Show All")
        a.triggered.connect(partial(self.set_hide_defaults, False))
        a = params_menu.addAction("Hide Defaults")
        a.triggered.connect(partial(self.set_hide_defaults, True))

        params_menu.addSeparator()
        for path_items, item in self.collect_param_items():
            name = ".".join([item.text(0) for item in path_items[1:]])
            a = params_menu.addAction(name)
            if not item.isHidden():
                a.setEnabled(False)
                a.setIcon(qtawesome.icon(PARAM_SET_ICON))
            else:
                a.setIcon(qtawesome.icon(PARAM_DEFAULT_ICON))

                def ensure_visible(items):
                    for item in items:
                        item.setHidden(False)

                a.triggered.connect(partial(ensure_visible, path_items))

        #
        #   COMPONENTS
        #
        menu.addSeparator()
        menu.addMenu(self._tree._add_component_menu)
        return menu


class ParamGroupItem(_BaseItem):
    def __init__(self, tree: "ComponentTree", parent, name, params, defaults):
        super().__init__(tree, parent)
        self.setFlags(
            QtCore.Qt.ItemIsEnabled
            | QtCore.Qt.ItemIsSelectable
            # | QtCore.Qt.ItemIsEditable
        )

        self._name = name
        self._params = params
        self._defaults = defaults

        self._build()
        self._update()
        self.setIcon(0, qtawesome.icon(PARAM_GROUP_ICON))

    def _build(self):
        for name, value in self._params:
            if name in ("TYPE", "ID", "children"):
                continue
            self._tree.add_param(self, name, value, getattr(self._defaults, name))
        self.setExpanded(True)

    def _update(self):
        self.setText(0, self._name)
        is_default = self.is_default()
        if self._hide_defaults and is_default:
            self.setHidden(True)
        else:
            self.setHidden(False)

    def is_default(self):
        for i in range(self.childCount()):
            child = self.child(i)
            if not child.is_default():
                return False
        return True

    def get_component_item(self):
        if self.parent() is None:
            return None
        return self.parent().get_component_item()

    def collect_param_items(self, parents=[]):
        collected = []
        parents = parents + [self]
        my_component_item = self.get_component_item()
        for i in range(self.childCount()):
            child = self.child(i)
            if child.get_component_item() is my_component_item:
                collected.extend(child.collect_param_items(parents))
        return collected

    def get_menu(self):
        return self._get_param_group_menu()
        # menu = QtWidgets.QMenu()
        # if not self._hide_defaults:
        #     a = menu.addAction("Hide Defaults")
        #     a.triggered.connect(partial(self.set_hide_defaults, True))
        # else:
        #     a = menu.addAction("Show All")
        #     a.triggered.connect(partial(self.set_hide_defaults, False))
        # return menu

    def as_params(self):
        new_params = self._params.__class__()
        for i in range(self.childCount()):
            child = self.child(i)
            for name, value in child.as_params().items():
                setattr(new_params, name, value)
        return {self._name: new_params}


class ParamItem(_BaseItem):
    def __init__(self, tree: "ComponentTree", parent, name, value, default):
        self._skip_edits = True
        super().__init__(tree, parent)
        self.setFlags(
            QtCore.Qt.ItemIsEnabled
            | QtCore.Qt.ItemIsSelectable
            | QtCore.Qt.ItemIsEditable
        )

        self._name = name
        self._value = value
        self._default = default

        self._build()
        self._skip_edits = False
        self._update()

    def _build(self):
        pass

    def _update(self):
        self._skip_edits = True
        try:
            self.setText(0, self._name)
            self.setText(1, str(self._value))
            is_default = self.is_default()
            if not is_default:
                self.setIcon(0, qtawesome.icon(PARAM_SET_ICON))
            else:
                self.setIcon(0, qtawesome.icon(PARAM_DEFAULT_ICON))

            if self._hide_defaults and is_default:
                self.setHidden(True)
            else:
                self.setHidden(False)
        finally:
            self._skip_edits = False

    def is_default(self):
        return self._value == self._default

    def get_component_item(self):
        if self.parent() is None:
            return None
        return self.parent().get_component_item()

    def collect_param_items(self, parents=[]):
        return [(parents + [self], self)]

    def get_menu(self):
        menu = QtWidgets.QMenu()
        if self._default in (True, False):
            a = menu.addAction("Toggle")
            a.triggered.connect(self.toggle_value)
        if isinstance(self._default, _EnumMixin):
            for v in type(self._default):
                a = menu.addAction(str(v))
                a.triggered.connect(partial(self.set_value, v))

        return menu

    def set_value(self, value):
        self._value = value
        self._update()

    def toggle_value(self):
        self.set_value(not self._value)

    def apply_edit(self, column):
        if self._skip_edits:
            return
        if column == 1:
            text = self.text(1)
            try:
                value = eval(text)
            except Exception:
                value = text
            self.set_value(value)
        self._update()

    def as_params(self):
        if self.is_default():
            return {}
        return {self._name: self._value}


class ComponentItem(_BaseItem):
    def __init__(self, tree: "ComponentTree", parent, ui, defaults):
        super().__init__(tree, parent)
        self._ui = ui
        self._defaults = defaults
        self._build()
        self._update()

    def _build(self):
        ID = self._ui.ID
        if ID is not None:
            self._tree.add_param(self, "ID", ID, None)
        for name, value in self._ui:
            if name in ("TYPE", "ID", "children"):
                continue
            self._tree.add_param(self, name, value, getattr(self._defaults, name))

        for child in getattr(self._ui, "children", []):
            self._tree.add_component(self, child)

        self.setIcon(0, qtawesome.icon(COMPONENT_ICON))
        self.setExpanded(True)

    def _update(self):
        self.setText(0, self._ui.TYPE)

    def sort_children(self):
        components = []
        params = []
        while self.childCount():
            c = self.takeChild(0)
            try:
                ci = c.get_component_item()
            except AttributeError:
                ci = None
            if ci == c:
                components.append(c)
            else:
                params.append(c)

        for c in params:
            self.addChild(c)
        for c in components:
            self.addChild(c)

    def get_component_item(self):
        return self

    def get_component_type(self):
        return self._ui.TYPE

    def collect_param_items(self, parents=[]):
        collected = []
        for i in range(self.childCount()):
            child = self.child(i)
            if child.get_component_item() is not self:
                continue
            collected.extend(child.collect_param_items([self]))
        return collected

    def get_menu(self):
        return self._get_param_group_menu()

    def as_params(self):
        return dict()

    def get_ui(self):
        schema = self._tree.get_schema()
        ui = getattr(schema, self._ui.TYPE)()
        for i in range(self.childCount()):
            child = self.child(i)
            for name, value in child.as_params().items():
                setattr(ui, name, value)
            child_ui = child.get_ui()
            if child_ui is not None:
                ui.children.append(child.get_ui())
        return ui


class ComponentTree(QtWidgets.QTreeWidget):
    _NO_ICON = None

    def _on_rows_inserted(self, parent_index, first, last):
        # There probably a better way to do this (ensuring params
        # children are before component children), but I must admit
        # I dont care -___-
        if first != 0:
            return
        if not self._sort_on_insert:
            return
        parent_item = self.itemFromIndex(parent_index)
        if parent_item is not None:
            self._sort_on_insert = False
            parent_item.sort_children()
            self._sort_on_insert = True
        self.expandRecursively(parent_index)

    def __init__(self, parent, view: ComponentsView):
        super().__init__(parent)
        self._view = view
        self._fav_components = ["VBox", "HBox", "Button", "Frame", "Handle"]

        self.setHeaderLabels(("Name", "Value"))
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.setRootIsDecorated(True)
        self.setHeaderHidden(True)

        self.setDragEnabled(True)
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(self.InternalMove)

        self.itemChanged.connect(self._on_item_changed)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._popup_request)
        self.currentItemChanged.connect(self._on_current_item_changed)

        self._sort_on_insert = True
        self.model().rowsInserted.connect(self._on_rows_inserted)

        self._item_menu = None
        self._add_component_menu = None

    def no_icon(self):
        if self._NO_ICON is None:
            self._NO_ICON = QtGui.QIcon()
        return self._NO_ICON

    def get_schema(self):
        return self._view.get_schema()

    def load_ui(self, ui):
        self.clear()
        self.add_component(self, ui)

    def get_ui(self):
        root = self.invisibleRootItem()
        if not root.childCount():
            return None
        return root.child(0).get_ui()

    def add_component(self, parent, ui):
        ComponentItem(
            self,
            parent,
            ui,
            ui.__class__(),
        )

    def add_param(self, parent, name, value, default):
        if isinstance(value, ParamsModel):
            ParamGroupItem(self, parent, name, value, default)
        else:
            ParamItem(self, parent, name, value, default)

    def add_component_to_current(self, TYPE):
        current_item = self.currentItem()
        current_component = current_item.get_component_item()
        ui = getattr(self.get_schema(), TYPE)()
        self.add_component(current_component, ui)
        current_component.sort_children()

    def _build_add_component_menu(self):
        if self._add_component_menu is not None:
            self._add_component_menu.clear()

        menu = QtWidgets.QMenu(self)
        menu.setIcon(qtawesome.icon(COMPONENT_ICON))
        menu.setTitle("Add Component")

        #
        #   Add Favorite Components
        #
        fav_actions = []
        for fav in self._fav_components:
            action = menu.addAction(fav)
            action.setIcon(qtawesome.icon(FAV_ICON))
            action.triggered.connect(partial(self.add_component_to_current, fav))
            fav_actions.append(action)

        grouped_component_actions = []
        all_component_actions = []

        #
        #   Add Components in their schema submenu
        #
        schema = self._view.get_schema()
        schema_classes = schema.__mro__
        components = schema.params_models()
        grouped_components = []
        for name, model in components:
            for c in schema_classes:
                if name in c.__dict__:
                    grouped_components.append((c.__name__, name))
        before_groups_action = menu.addSeparator()
        schema_menus = {}
        for schema_name, component_name in grouped_components:
            try:
                schema_menu = schema_menus[schema_name]
            except KeyError:
                schema_menu = menu.addMenu(qtawesome.icon(SCHEMA_ICON), schema_name)
                schema_menus[schema_name] = schema_menu
            a = schema_menu.addAction(qtawesome.icon(COMPONENT_ICON), component_name)
            a.triggered.connect(partial(self.add_component_to_current, component_name))
            grouped_component_actions.append(a)

            a = QtWidgets.QAction(qtawesome.icon(MATCH_ICON), component_name)
            a.triggered.connect(partial(self.add_component_to_current, component_name))
            all_component_actions.append(a)

        #
        # Add all component action. Those are shown only as result
        # of search
        #
        for action in all_component_actions:
            menu.insertAction(before_groups_action, action)

        #
        # Add the search thingy
        #
        filter_action = QtWidgets.QWidgetAction(menu)
        w = QtWidgets.QWidget()
        w.setLayout(QtWidgets.QHBoxLayout())
        w.layout().setContentsMargins(0, 0, 0, 0)
        w.layout().setSpacing(0)
        le = QtWidgets.QLineEdit()
        le.setToolTip("Enter text to filter components")
        b = QtWidgets.QToolButton()
        b.setToolTip("Clear filter text")
        b.setIcon(qtawesome.icon("fa5s.eraser"))
        b.clicked.connect(le.clear)
        w.layout().addWidget(le)
        w.layout().addWidget(b)
        filter_action.setDefaultWidget(w)
        before = menu.actions()[0]
        menu.insertAction(before, filter_action)

        def show_unfiltered_action():
            for action in fav_actions:
                action.setVisible(True)
            for action in grouped_component_actions:
                action.setVisible(True)
            for action in all_component_actions:
                action.setVisible(False)

        def apply_menu_filter(filter_text):
            if not filter_text:
                show_unfiltered_action()
                return
            for action in fav_actions:
                action.setVisible(False)
            for action in grouped_component_actions + all_component_actions:
                action.setVisible(filter_text.lower() in action.text().lower())

        apply_menu_filter("")
        le.textChanged.connect(apply_menu_filter)

        self._add_component_menu = menu

    def _popup_request(self, pos):
        item = self.itemAt(pos)
        if self._add_component_menu is None:
            self._build_add_component_menu()
        if item is not None:
            # NB: we store the menu in self._item_menu
            # to prevent it from being deleted by Qt before
            # showing up (since it has no parent)
            self._item_menu = item.get_menu()
            self._item_menu.popup(QtGui.QCursor.pos())
        else:
            self._add_component_menu.popup(QtGui.QCursor.pos())

    def _on_item_changed(self, item, column):
        item.apply_edit(column)

    def _on_current_item_changed(self, current, previous):
        prev_component_type = None
        if previous is not None:
            prev_component_type = previous.get_component_type()
        component_type = current.get_component_type()
        if prev_component_type != component_type:
            self._view.current_component_type_changed.emit(component_type)


class ComponentsView(QtWidgets.QWidget):

    current_component_type_changed = QtCore.Signal(str)

    def __init__(self, parent, editor):
        super().__init__(parent)
        self.editor = editor

        lo = QtWidgets.QVBoxLayout()
        lo.setContentsMargins(0, 0, 0, 0)
        lo.setSpacing(0)
        self.setLayout(lo)

        top_lo = QtWidgets.QHBoxLayout()
        lo.addLayout(top_lo)

        top_lo.addStretch()

        b = QtWidgets.QPushButton(self)
        b.setText(">")
        b.clicked.connect(self.send_to_text_view)
        top_lo.addWidget(b)

        b = QtWidgets.QPushButton(self)
        b.setText(">>")
        b.clicked.connect(self.send_to_render_view)
        top_lo.addWidget(b)

        self._tree = ComponentTree(self, self)
        lo.addWidget(self._tree)

    def get_renderer(self):
        return self.editor.get_renderer()

    def get_schema(self):
        return self.get_renderer().schema

    def load_ui(self, ui):
        self._tree.load_ui(ui)

    def get_ui(self):
        return self._tree.get_ui()

    def send_to_text_view(self):
        self.editor._text_view.load_ui(self.get_ui())

    def send_to_render_view(self):
        ui = self.get_ui()
        self.editor._text_view.load_ui(ui)
        self.editor._render_view.render(ui)
