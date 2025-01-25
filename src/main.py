#!/Users/huongnguyen105/Desktop/Tu-Anh/my-pyside6-dashboard/venv/bin/python
import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QSizeGrip
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QIcon, QFont, QFontDatabase
from dashboard_components.style import StyleManager
from dashboard_components.navbar import CustomNavigationContentWidget
from dashboard_components.titlebar import CustomTitleBar
from dashboard_components.sidegrip import SideGrip
from dashboard_components.icon import SVGIconManager, SVGTemplateGenerator

class MainWindow(QMainWindow):
    _gripSize = 8

    def __init__(self):
        super().__init__()
        self.icon_manager = SVGIconManager()
        self.initUI()

    def initUI(self) -> None:
        """Initialize the user interface."""
        self.setWindowTitle("Custom Navigation Interface")
        self.setMinimumSize(800, 600)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)  # Remove the default title bar

        centralWidget = QWidget(self)
        mainLayout = QVBoxLayout(centralWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        self.style_manager = StyleManager()
        self.setupTitleBar(mainLayout)
        self.setupNavigationContent(mainLayout)

        self.setCentralWidget(centralWidget)
        self.navigationContentWidget.switchToPage(0)  # Show "Home Page"
        self.applyStyles()
        self.addGrips()

    def setupTitleBar(self, layout: QVBoxLayout) -> None:
        """Set up the custom title bar."""
        self.titleBar = CustomTitleBar(self.style_manager, self.icon_manager, self)
        layout.addWidget(self.titleBar)

    def setupNavigationContent(self, layout: QVBoxLayout) -> None:
        """Set up the custom navigation and content widget."""
        self.navigationContentWidget = CustomNavigationContentWidget(self.style_manager, self.icon_manager, self)
        self.navigationContentWidget.addPageWithNavigationItem(QLabel("Home Page"),
                                                               QIcon(self.icon_manager.render_icon("Home")), "Home",
                                                               "Home")
        self.navigationContentWidget.addPageWithNavigationItem(QLabel("Processes Page"),
                                                               QIcon(self.icon_manager.render_icon("Folder")),
                                                               "Processes", "Folder")
        self.iconEditorWidget = SVGTemplateGenerator(self.icon_manager, self.style_manager, self)
        self.navigationContentWidget.addPageWithNavigationItem(self.iconEditorWidget,
                                                               QIcon(self.icon_manager.render_icon("Setting")),
                                                               "Settings", "Setting", align_bottom=True)
        self.navigationContentWidget.addPageWithNavigationItem(QLabel("Info Page"),
                                                               QIcon(self.icon_manager.render_icon("Info")), "Info",
                                                               "Info", align_bottom=True)
        layout.addWidget(self.navigationContentWidget)

    def applyStyles(self) -> None:
        """Apply styles using the style manager."""
        self.setStyleSheet(self.style_manager.get_mainwindow_stylesheet())

    def addGrips(self) -> None:
        """Add side and corner grips for resizing."""
        self.sideGrips = [
            SideGrip(self, Qt.LeftEdge),
            SideGrip(self, Qt.TopEdge),
            SideGrip(self, Qt.RightEdge),
            SideGrip(self, Qt.BottomEdge),
        ]
        self.cornerGrips = [QSizeGrip(self) for _ in range(4)]
        for grip in self.cornerGrips + self.sideGrips:
            grip.setStyleSheet("background-color: transparent;")

    def toggle_mode(self) -> None:
        """Toggle the mode and update all components."""
        self.style_manager.toggle_mode()
        self.icon_manager.set_icon_fill("#FFFFFF" if self.style_manager.current_mode == "dark" else "#000000")
        self.navigationContentWidget.refresh_icons()
        self.titleBar.refresh_icons()
        self.iconEditorWidget.display_selected_icon()
        self.titleBar.applyStyles()
        self.navigationContentWidget.applyStyles()
        self.iconEditorWidget.applyStyles()
        self.applyStyles()

    def resizeEvent(self, event) -> None:
        QMainWindow.resizeEvent(self, event)
        self.updateGrips()

    def updateGrips(self) -> None:
        outRect = self.rect()
        inRect = outRect.adjusted(self._gripSize, self._gripSize, -self._gripSize, -self._gripSize)
        self.cornerGrips[0].setGeometry(QRect(outRect.topLeft(), inRect.topLeft()))
        self.cornerGrips[1].setGeometry(QRect(outRect.topRight(), inRect.topRight()).normalized())
        self.cornerGrips[2].setGeometry(QRect(inRect.bottomRight(), outRect.bottomRight()))
        self.cornerGrips[3].setGeometry(QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())
        self.sideGrips[0].setGeometry(0, inRect.top(), self._gripSize, inRect.height())
        self.sideGrips[1].setGeometry(inRect.left(), 0, inRect.width(), self._gripSize)
        self.sideGrips[2].setGeometry(inRect.left() + inRect.width(), inRect.top(), self._gripSize, inRect.height())
        self.sideGrips[3].setGeometry(self._gripSize, inRect.top() + inRect.height(), inRect.width(), self._gripSize)
        [grip.raise_() for grip in self.sideGrips + self.cornerGrips]

    def mousePressEvent(self, event) -> None:
        """Capture the mouse press event to enable window dragging."""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event) -> None:
        """Capture the mouse move event to enable window dragging."""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font_id = QFontDatabase.addApplicationFont("fonts/ttf/JetBrainsMono-Regular.ttf")
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(font_family))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())