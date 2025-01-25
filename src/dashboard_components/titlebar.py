from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from dashboard_components.icon import SVGIconManager
from dashboard_components.style import StyleManager

class CustomTitleBar(QWidget):
    def __init__(self, style_manager, icon_manager=None, parent=None, button_size=30):
        super().__init__(parent)
        self.style_manager = style_manager
        self.icon_manager = icon_manager  # Pass the icon manager to manage icons
        self.setFixedHeight(30)
        self.button_size = button_size

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)  # Remove spacing between buttons

        # Title label
        self.title_label = QLabel("  Dashboard")
        layout.addWidget(self.title_label, stretch=1)

        # Spacer to push buttons to the right
        # layout.addStretch()

        # Minimize button with SVG icon
        self.minimize_button = QPushButton(QIcon(self.icon_manager.render_icon("Minimize", size=10)),"", self)
        self.minimize_button.setFixedSize(self.button_size, self.button_size)
        self.minimize_button.clicked.connect(self.minimize_window)
        layout.addWidget(self.minimize_button)

        # Maximize/Restore button with SVG icon
        self.maximize_button = QPushButton(QIcon(self.icon_manager.render_icon("Maximize", size = 10)), "", self)
        self.maximize_button.setFixedSize(self.button_size, self.button_size)
        self.maximize_button.clicked.connect(self.maximize_restore_window)
        layout.addWidget(self.maximize_button)

        # Close button with SVG icon
        self.close_button = QPushButton(QIcon(self.icon_manager.render_icon("Close", size=10)), "", self)
        self.close_button.setFixedSize(self.button_size, self.button_size)
        self.close_button.clicked.connect(self.close_window)
        layout.addWidget(self.close_button)

        self.parent = parent
        self.is_maximized = False

        self.applyStyles()

    def applyStyles(self):
        """Apply styles using the style manager."""
        self.setStyleSheet(self.style_manager.get_titlebar_stylesheet())

    def refresh_icons(self):
        """Refresh the icons with the current fill color."""
        self.minimize_button.setIcon(QIcon(self.icon_manager.render_icon("Minimize", size=10)))
        self.maximize_button.setIcon(QIcon(self.icon_manager.render_icon("Maximize", size=10)))
        self.close_button.setIcon(QIcon(self.icon_manager.render_icon("Close", size=10)))

    def minimize_window(self):
        self.parent.showMinimized()

    def maximize_restore_window(self):
        if self.is_maximized:
            self.parent.showNormal()
            self.is_maximized = False
        else:
            self.parent.showMaximized()
            self.is_maximized = True

    def close_window(self):
        self.parent.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.drag_position = event.globalPosition().toPoint() - self.parent.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent.move(event.globalPosition().toPoint() - self.parent.drag_position)
            event.accept()