class StyleManager:
    def __init__(self):
        self.current_mode = "dark"  # Default mode
        self.font_size = 10  # Default font size

        # Dark mode colors:
        self.dark_hover = "#4A4A4A"
        self.dark_pressed = "#5A5A5A"
        self.dark_font_color = "#FFFFFF"
        self.dark_navi_bgcolor = "#2b2d30"
        self.dark_navi_button_bg = "transparent"
        self.dark_window_bgcolor = "#344444"
        self.dark_content_bgcolor = "#1e1f22"

        # Bright mode colors:
        self.bright_hover = "gray" #"#D0D0D0"
        self.bright_pressed = "gray"#"#C0C0C0"
        self.bright_font_color = "#000000"
        self.bright_navi_bgcolor = "#F0F0F0"
        self.bright_navi_button_bg = "transparent"
        self.bright_window_bgcolor = "#FFFFFF"
        self.bright_content_bgcolor = "#D0D0D0"

    def get_stylesheet(self):
        """Return the combined stylesheet for the application based on the current mode."""
        return (
            self.get_navigation_stylesheet() +
            self.get_titlebar_stylesheet() +
            self.get_mainwindow_stylesheet() +
            self.get_svg_template_generator_stylesheet() +
            self.get_excel_processing_stylesheet()
        )

    def get_navigation_stylesheet(self):
        """Return the navigation pane stylesheet based on the current mode."""
        return self.dark_mode_navigation_stylesheet() if self.current_mode == "dark" else self.bright_mode_navigation_stylesheet()

    def get_titlebar_stylesheet(self):
        """Return the title bar stylesheet based on the current mode."""
        return self.dark_mode_titlebar_stylesheet() if self.current_mode == "dark" else self.bright_mode_titlebar_stylesheet()

    def get_mainwindow_stylesheet(self):
        """Return the main window stylesheet based on the current mode."""
        return self.dark_mode_mainwindow_stylesheet() if self.current_mode == "dark" else self.bright_mode_mainwindow_stylesheet()

    def get_svg_template_generator_stylesheet(self):
        """Return the SVG Template Generator stylesheet based on the current mode."""
        return self.dark_mode_svg_template_generator_stylesheet() if self.current_mode == "dark" else self.bright_mode_svg_template_generator_stylesheet()

    def get_excel_processing_stylesheet(self):
        """Return the Excel Processing widget stylesheet based on the current mode."""
        return self.dark_mode_excel_processing_stylesheet() if self.current_mode == "dark" else self.bright_mode_excel_processing_stylesheet()

    def common_button_styles(self, bg_color, font_color):
        return f"""
           QPushButton {{
               background-color: {bg_color};
               color: {font_color};
               border: none;
               padding: 10px;
               font-size: {self.font_size}px;
               border-radius: 6px;
           }}
           QPushButton:hover {{
               background-color: {self.dark_hover if bg_color == self.dark_navi_button_bg else self.bright_hover};
           }}
           QPushButton:pressed {{
               background-color: {self.dark_pressed if bg_color == self.dark_navi_button_bg else self.bright_pressed};
           }}
        """

    def common_label_styles(self, font_color):
        return f"""
           QLabel {{
               background-color: transparent;
               color: {font_color};
               font-size: {self.font_size}px;
               padding: 5px;
               border: none;
           }}
        """

    def common_input_styles(self, bg_color, font_color):
        return f"""
           QComboBox, QDateEdit {{
               background-color: {bg_color};
               color: {font_color};
               font-size: {self.font_size}px;
               border: 1px solid #ccc;
               border-radius: 6px;
               padding: 4px;
           }}
           QComboBox::drop-down, QDateEdit::drop-down {{
               border: none;
           }}
        """

    def common_table_view_styles(self, bg_color, font_color):
        return f"""
           QTableView {{
               background-color: {bg_color};
               color: {font_color};
               border: none;
               font-size: {self.font_size}px;
               border-radius: 6px;
           }}
           QHeaderView::section {{
               background-color: {bg_color};
               color: {font_color};
               font-size: {self.font_size}px;
           }}
           QTableCornerButton::section {{
               background-color: {bg_color};
           }}
           QTableView::verticalHeader {{
               background-color: {bg_color};
               color: {font_color};
               font-size: {self.font_size}px;
           }}
        """

    def dark_mode_navigation_stylesheet(self):
        return f"""
           QWidget {{ background-color: {self.dark_navi_bgcolor}; }}
           QListWidget {{ border: none; outline: 0; background-color: {self.dark_navi_bgcolor}; color: {self.dark_font_color}; font-size: {self.font_size}px;}}
           QListWidget::item {{ border: none; padding-left: 5px; padding-top: 5px; font-size: {self.font_size}px;}}
           QListWidget::item:hover {{ background-color: {self.dark_hover}; font-size: {self.font_size}px;}}
           QListWidget::item:selected {{ background-color: {self.dark_pressed}; color: {self.dark_font_color}; border-left: 1px solid #3058a4; font-size: {self.font_size}px;}}
           QStackedWidget {{ background-color: {self.dark_content_bgcolor}; font-size: {self.font_size}px;}}
           QSplitter::handle {{ background-color: {self.dark_hover}; }}
           {self.common_button_styles(self.dark_navi_button_bg, self.dark_font_color)}
           {self.common_label_styles(self.dark_font_color)}
           {self.common_input_styles(self.dark_navi_bgcolor, self.dark_font_color)}
       """

    def bright_mode_navigation_stylesheet(self):
        return f"""
           QWidget {{ background-color: {self.bright_navi_bgcolor}; }}
           QListWidget {{ border: none; outline: 0; background-color: {self.bright_navi_bgcolor}; color: {self.bright_font_color}; font-size: {self.font_size}px;}}
           QListWidget::item {{ border: none; padding-left: 5px; padding-top: 5px; font-size: {self.font_size}px;}}
           QListWidget::item:hover {{ background-color: {self.bright_hover}; font-size: {self.font_size}px;}}
           QListWidget::item:selected {{ background-color: {self.bright_pressed}; color: {self.bright_font_color}; border-left: 1px solid blue; font-size: {self.font_size}px;}}
           QStackedWidget {{ background-color: {self.bright_content_bgcolor}; font-size: {self.font_size}px;}}
           QSplitter::handle {{ background-color: #E0E0E0; }}
           {self.common_button_styles(self.bright_navi_button_bg, self.bright_font_color)}
           {self.common_label_styles(self.bright_font_color)}
           {self.common_input_styles(self.bright_navi_bgcolor, self.bright_font_color)}
       """

    def dark_mode_titlebar_stylesheet(self):
        return f"""
           QWidget {{
               background-color: transparent;
               color: {self.dark_font_color};
           }}
           QPushButton::icon {{
               alignment: center;
           }}
           {self.common_button_styles('transparent', self.dark_font_color)}
           {self.common_label_styles(self.dark_font_color)}
       """

    def bright_mode_titlebar_stylesheet(self):
        return f"""
           QWidget {{
               background-color: transparent;
               color: {self.bright_font_color};
           }}
           QPushButton::icon {{
               alignment: center;
           }}
           {self.common_button_styles('transparent', self.bright_font_color)}
           {self.common_label_styles(self.bright_font_color)}
       """

    def dark_mode_mainwindow_stylesheet(self):
        return f"""
           QMainWindow {{
               background-color: {self.dark_window_bgcolor};
           }}
       """

    def bright_mode_mainwindow_stylesheet(self):
        return f"""
           QMainWindow {{
               background-color: {self.bright_window_bgcolor};
           }}
       """

    def dark_mode_svg_template_generator_stylesheet(self):
        return f"""
            QWidget {{
                background-color: {self.dark_content_bgcolor};
                color: {self.dark_font_color};
                font-size: {self.font_size}px;
            }}
            QPushButton {{
                background-color: #3c3f41;
                color: {self.dark_font_color};
                border: 1px solid #555;
                padding: 5px;
                border-radius: 8px;
                font-size: {self.font_size}px;
            }}
            QPushButton:hover {{
                background-color: {self.dark_hover};
            }}
            QLineEdit, QTextEdit {{
                background-color: {self.dark_navi_bgcolor};
                color: {self.dark_font_color};
                border: 1px solid #555;
                border-radius: 8px;
                padding: 4px;
                font-size: {self.font_size}px;
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border: 1px solid #0078d7;
            }}
            QComboBox {{
                background-color: {self.dark_font_color};
                color: black;
                font-size: {self.font_size}px;
                border-radius: 6px;
            }}
            {self.common_label_styles(self.dark_font_color)}
        """

    def bright_mode_svg_template_generator_stylesheet(self):
        return f"""
            QWidget {{
                background-color: {self.bright_content_bgcolor};
                color: {self.bright_font_color};
                font-size: {self.font_size}px;
            }}
            QPushButton {{
                background-color: #e0e0e0;
                color: {self.bright_font_color};
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 8px;
                font-size: {self.font_size}px;
            }}
            QPushButton:hover {{
                background-color: {self.bright_hover};
            }}
            QPushButton:pressed {{
                background-color: {self.bright_pressed};
            }}
            QLineEdit, QTextEdit {{
                background-color: {self.bright_navi_bgcolor};
                color: {self.bright_font_color};
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 4px;
                font-size: {self.font_size}px;
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border: 1px solid #0078d7;
            }}
            QComboBox {{
                background-color: {self.dark_font_color};
                color: {self.bright_font_color};
                font-size: {self.font_size}px;
                border-radius: 6px;
            }}
            {self.common_label_styles(self.bright_font_color)}
        """

    def dark_mode_excel_processing_stylesheet(self):
        return f"""
            QWidget {{
                background-color: {self.dark_content_bgcolor};
                color: {self.dark_font_color};
                font-size: {self.font_size}px;
            }}
            QPushButton {{
                background-color: #3c3f41;
                color: {self.dark_font_color};
                border: 1px solid #555;
                padding: 5px;
                border-radius: 8px;
                font-size: {self.font_size}px;
            }}
            QPushButton:hover {{
                background-color: {self.dark_hover};
            }}
            {self.common_table_view_styles(self.dark_navi_bgcolor, self.dark_font_color)}
            QDateEdit {{
                background-color: {self.dark_navi_bgcolor};
                color: {self.dark_font_color};
                font-size: {self.font_size}px;
                border-radius: 6px;
            }}
            {self.common_label_styles(self.dark_font_color)}
        """

    def bright_mode_excel_processing_stylesheet(self):
        return f"""
            QWidget {{
                background-color: {self.bright_content_bgcolor};
                color: {self.bright_font_color};
                font-size: {self.font_size}px;
            }}
            QPushButton {{
                background-color: #e0e0e0;
                color: {self.bright_font_color};
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 8px;
                font-size: {self.font_size}px;
            }}
            QPushButton:hover {{
                background-color: {self.bright_hover};
            }}
            QPushButton:pressed {{
                background-color: {self.bright_pressed};
            }}
            {self.common_table_view_styles(self.bright_navi_bgcolor, self.bright_font_color)}
            QDateEdit {{
                background-color: {self.bright_navi_bgcolor};
                color: {self.bright_font_color};
                font-size: {self.font_size}px;
                border-radius: 6px;
            }}
            {self.common_label_styles(self.bright_font_color)}
        """

    def toggle_mode(self):
        """Toggle between dark and bright modes."""
        self.current_mode = "bright" if self.current_mode == "dark" else "dark"