from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QStackedWidget, QPushButton, QSizePolicy, QSplitter
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from .icon import SVGIconManager

class CustomNavigationContentWidget(QWidget):
    def __init__(self, style_manager, icon_manager, parent=None, button_size=35, expanded_width=100, collapsed_width=35,
                 item_height=30, padding=0):
        super().__init__(parent)
        self.style_manager = style_manager
        self.icon_manager = icon_manager
        self.button_size = button_size
        self.expanded_width = expanded_width
        self.collapsed_width = collapsed_width
        self.item_height = item_height
        self.padding = padding
        self.sidebar_expanded = True  # Start with the sidebar expanded
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.splitter = QSplitter(Qt.Horizontal, self)
        self.splitter.setHandleWidth(2)  # Set the handle width to make the splitter thinner

        # Navigation pane setup
        self.navigation_widget = QWidget(self)  # Store as instance variable for access in toggle_sidebar
        navigation_layout = QVBoxLayout(self.navigation_widget)
        navigation_layout.setContentsMargins(0, 0, 0, 0)
        navigation_layout.setSpacing(0)

        # Menu button
        self.menuButton = QPushButton(QIcon(self.icon_manager.render_icon("Menu")), "", self)
        self.menuButton.setFixedSize(self.button_size, self.button_size)
        self.menuButton.setObjectName("menuButton")
        self.menuButton.clicked.connect(self.toggle_sidebar)
        navigation_layout.addWidget(self.menuButton)

        self.nav_list_top = QListWidget(self)
        self.nav_list_top.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.nav_list_top.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        navigation_layout.addWidget(self.nav_list_top)

        self.nav_list_bottom = QListWidget(self)
        self.nav_list_bottom.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.nav_list_bottom.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.nav_list_bottom.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        navigation_layout.addWidget(self.nav_list_bottom)

        # Toggle mode button
        self.toggleButton = QPushButton(QIcon(self.icon_manager.render_icon("Toggle-off")), "", self)
        self.toggleButton.setFixedSize(self.button_size, self.button_size)
        self.toggleButton.setObjectName("toggleButton")
        self.toggleButton.clicked.connect(self.parent().toggle_mode)
        navigation_layout.addWidget(self.toggleButton)

        self.splitter.addWidget(self.navigation_widget)

        # Content stack on the right
        self.contentStack = QStackedWidget(self)
        self.splitter.addWidget(self.contentStack)
        self.splitter.setStretchFactor(1, 1)

        main_layout.addWidget(self.splitter)

        # Set initial sizes for the splitter
        self.splitter.setSizes([self.expanded_width, self.width() - self.expanded_width])

        self.nav_list_top.itemClicked.connect(self.handleTopItemClick)
        self.nav_list_bottom.itemClicked.connect(self.handleBottomItemClick)

        self.applyStyles()

    def refresh_icons(self):
        """Refresh the icons with the current fill color."""
        self.menuButton.setIcon(QIcon(self.icon_manager.render_icon("Menu")))
        self.toggleButton.setIcon(QIcon(
            self.icon_manager.render_icon("Toggle-off" if self.style_manager.current_mode == "bright" else "Toggle-on")))

        for i in range(self.nav_list_top.count()):
            item = self.nav_list_top.item(i)
            icon_name = item.data(Qt.UserRole + 2)  # Retrieve the stored icon name
            if icon_name:  # Ensure the icon name is not None
                item.setIcon(QIcon(self.icon_manager.render_icon(icon_name)))

        for i in range(self.nav_list_bottom.count()):
            item = self.nav_list_bottom.item(i)
            icon_name = item.data(Qt.UserRole + 2)  # Retrieve the stored icon name
            if icon_name:  # Ensure the icon name is not None
                item.setIcon(QIcon(self.icon_manager.render_icon(icon_name)))

    def handleTopItemClick(self, item):
        """Handle item click events for the top list."""
        # Clear selection in the bottom list
        self.nav_list_bottom.clearSelection()
        # Highlight only the clicked item
        self.nav_list_top.setCurrentItem(item)
        page_index = self.nav_list_top.row(item)
        self.switchToPage(page_index)

    def handleBottomItemClick(self, item):
        """Handle item click events for the bottom list."""
        # Clear selection in the top list
        self.nav_list_top.clearSelection()
        # Highlight only the clicked item
        self.nav_list_bottom.setCurrentItem(item)
        page_index = item.data(Qt.UserRole)
        if isinstance(page_index, int):  # Ensure the page index is an integer
            self.switchToPage(page_index)

    def applyStyles(self):
        """Apply styles using the style manager."""
        self.setStyleSheet(self.style_manager.get_navigation_stylesheet())

    def toggle_sidebar(self):
        """Toggle the visibility of the sidebar."""
        self.sidebar_expanded = not self.sidebar_expanded
        width = self.expanded_width if self.sidebar_expanded else self.collapsed_width

        # Set the fixed width of the navigation widget
        self.navigation_widget.setFixedWidth(width)

        # Update the splitter sizes to respect the new width
        self.splitter.setSizes([width, self.splitter.width() - width])

        # Update text visibility for all items in the top list
        for i in range(self.nav_list_top.count()):
            item = self.nav_list_top.item(i)
            original_text = item.data(Qt.UserRole + 1)  # Retrieve the original text
            item.setText(original_text if self.sidebar_expanded else "")

        # Update text visibility for all items in the bottom list
        for i in range(self.nav_list_bottom.count()):
            item = self.nav_list_bottom.item(i)
            original_text = item.data(Qt.UserRole + 1)  # Retrieve the original text
            item.setText(original_text if self.sidebar_expanded else "")

    def addPageWithNavigationItem(self, page_widget, icon, text, icon_name, align_bottom=False):
        """Add a new page to the content stack and a corresponding item to the navigation pane."""
        # Add page to content stack
        index = self.contentStack.addWidget(page_widget)

        # Create and add corresponding navigation item
        nav_item = QListWidgetItem(icon, text if self.sidebar_expanded else "")
        nav_item.setData(Qt.UserRole, index)  # Store the page index
        nav_item.setData(Qt.UserRole + 1, text)  # Store the original text separately
        nav_item.setData(Qt.UserRole + 2, icon_name)  # Store the icon name

        if align_bottom:
            self.nav_list_bottom.addItem(nav_item)
            self.adjustBottomListHeight()
        else:
            self.nav_list_top.addItem(nav_item)

    def adjustBottomListHeight(self):
        """Adjust the height of the bottom navigation list based on its contents."""
        num_items = self.nav_list_bottom.count()
        new_height = num_items * self.item_height + self.padding
        self.nav_list_bottom.setFixedHeight(new_height)

    def switchToPage(self, index):
        """Switch to a specific page."""
        if 0 <= index < self.contentStack.count():
            self.contentStack.setCurrentIndex(index)