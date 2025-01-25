import sys
import os
import ast
import re
from typing import Dict, Optional
from PySide6.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton, QWidget, QMessageBox, QComboBox
)
from PySide6.QtGui import QColor, QPixmap, QPainter, QFontMetrics
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray
from dashboard_components.style import StyleManager
from PySide6.QtCore import Qt

class SVGIconManager:
    def __init__(self, file_path: str = "icons.txt"):
        self.file_path = file_path
        self.icon_fill = "#FFFFFF"  # Default dark mode color
        self.icons = self.load_icons()

    def load_icons(self) -> Dict[str, str]:
        """Load icons from the file."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as file:
                file.write("{}")
            return {}
        with open(self.file_path, "r", encoding="utf-8") as file:
            try:
                data = file.read()
                return ast.literal_eval(data)
            except (SyntaxError, ValueError):
                return {}

    def save_icons(self) -> None:
        """Save icons to the file."""
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write(str(self.icons))

    def add_icon(self, icon_name: str, svg_template: str) -> None:
        """Add a new icon to the manager."""
        self.icons[icon_name] = svg_template
        self.save_icons()

    def get_icon(self, icon_name: str) -> Optional[str]:
        """Retrieve an icon by its name."""
        return self.icons.get(icon_name)

    def delete_icon(self, icon_name: str) -> None:
        """Delete an icon from the manager."""
        if icon_name in self.icons:
            del self.icons[icon_name]
            self.save_icons()

    def set_icon_fill(self, color: str) -> None:
        """Set the fill color for icons."""
        self.icon_fill = color

    def render_icon(self, icon_name: str, size: int) -> Optional[QPixmap]:
        """Render an icon to a QPixmap."""
        svg_template = self.get_icon(icon_name)
        if not svg_template:
            return None

        svg_template = svg_template.replace("currentColor", self.icon_fill)
        renderer = QSvgRenderer(QByteArray(svg_template.encode("utf-8")))
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return pixmap

class SVGTemplateGenerator(QWidget):
    def __init__(self, icon_manager, style_manager, parent=None):
        super().__init__(parent)  # Pass the parent to the QWidget constructor
        self.icon_manager = icon_manager
        self.style_manager = style_manager
        self.setWindowTitle("SVG Template Generator")
        self.setGeometry(300, 300, 600, 600)

        self.initUI()
        self.applyStyles()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Icon selection and display section
        icon_selection_layout = QHBoxLayout()
        label = QLabel("Available Icons:")

        # Calculate the width of the label text
        font_metrics = QFontMetrics(label.font())
        text_width = font_metrics.horizontalAdvance(label.text())
        label.setFixedWidth(120)  # Add padding: text_width + 10

        self.icon_combobox = QComboBox()
        self.icon_combobox.setEditable(True)
        self.icon_combobox.addItems(self.icon_manager.icons.keys())

        self.delete_button = QPushButton("Delete Icon")
        icon_button_height = self.delete_button.sizeHint().height()
        self.icon_display = QLabel()
        self.icon_display.setFixedSize(icon_button_height, icon_button_height)  # Square display matching button height

        icon_selection_layout.addWidget(label)
        icon_selection_layout.addWidget(self.icon_combobox)
        icon_selection_layout.addWidget(self.icon_display)
        icon_selection_layout.addWidget(self.delete_button)
        main_layout.addLayout(icon_selection_layout)

        # Icon creation section
        self.name_label = QLabel("Icon Name:")
        self.name_input = QLineEdit()
        self.svg_label = QLabel("SVG Code:")
        self.svg_input = QTextEdit()

        main_layout.addWidget(self.name_label)
        main_layout.addWidget(self.name_input)
        main_layout.addWidget(self.svg_label)
        main_layout.addWidget(self.svg_input)

        self.output_label = QLabel("Generated Template:")
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)

        main_layout.addWidget(self.output_label)
        main_layout.addWidget(self.output_display)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Icon")
        self.close_button = QPushButton("Close")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.close_button)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.svg_input.textChanged.connect(self.generate_template)
        self.save_button.clicked.connect(self.add_icon_to_manager)
        self.delete_button.clicked.connect(self.delete_icon_from_manager)
        self.close_button.clicked.connect(self.close)
        self.icon_combobox.currentIndexChanged.connect(self.display_selected_icon)

    def applyStyles(self):
        """Apply styles using the style manager."""
        self.setStyleSheet(self.style_manager.get_svg_template_generator_stylesheet())

    def generate_template(self):
        icon_name = self.name_input.text().strip()
        svg_code = self.svg_input.toPlainText().strip()

        if not icon_name or not svg_code:
            self.output_display.setPlainText("")
            return

        template = re.sub(r'width="[^"]+"', 'width="{width}"', svg_code)
        template = re.sub(r'height="[^"]+"', 'height="{height}"', template)
        template = re.sub(r'fill="[^"]+"', 'fill="{fill}"', template)
        template = re.sub(r'class="[^"]+"', 'class="{class_name}"', template)

        formatted_output = f'"{icon_name}": """\n{template}\n""",'
        self.output_display.setPlainText(formatted_output)

    def add_icon_to_manager(self):
        icon_name = self.name_input.text().strip()
        svg_code = self.svg_input.toPlainText().strip()

        if not icon_name or not svg_code:
            QMessageBox.warning(self, "Error", "Icon name and SVG code cannot be empty!")
            return

        template = re.sub(r'width="[^"]+"', 'width="{width}"', svg_code)
        template = re.sub(r'height="[^"]+"', 'height="{height}"', template)
        template = re.sub(r'fill="[^"]+"', 'fill="{fill}"', template)
        template = re.sub(r'class="[^"]+"', 'class="{class_name}"', template)

        self.icon_manager.add_icon(icon_name, template)
        QMessageBox.information(self, "Success", f"Icon '{icon_name}' added/updated successfully!")
        self.output_display.setPlainText("")

        # Clear the inputs
        self.name_input.clear()
        self.svg_input.clear()
        self.refresh_icon_combobox()

    def delete_icon_from_manager(self):
        icon_name = self.icon_combobox.currentText().strip()

        if not icon_name:
            QMessageBox.warning(self, "Error", "Icon name cannot be empty!")
            return

        if icon_name not in self.icon_manager.icons:
            QMessageBox.warning(self, "Error", f"Icon '{icon_name}' does not exist!")
            return

        self.icon_manager.delete_icon(icon_name)
        QMessageBox.information(self, "Success", f"Icon '{icon_name}' deleted successfully!")
        self.refresh_icon_combobox()

    def display_selected_icon(self):
        icon_name = self.icon_combobox.currentText()
        svg_template = self.icon_manager.get_icon(icon_name)
        if svg_template:
            self.name_input.setText(icon_name)
            self.svg_input.setPlainText(svg_template.format(width="16", height="16", fill="gray", class_name="bi"))
            pixmap = self.icon_manager.render_icon(icon_name, size=16)
            self.icon_display.setPixmap(pixmap)

    def refresh_icon_combobox(self):
        self.icon_combobox.clear()
        self.icon_combobox.addItems(self.icon_manager.icons.keys())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon_file = "icons.txt"
    icon_manager = SVGIconManager(icon_file)
    style_manager = StyleManager()
    window = SVGTemplateGenerator(icon_manager, style_manager)
    window.show()
    sys.exit(app.exec())