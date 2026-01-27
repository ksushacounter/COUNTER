import sys
from pathlib import Path


class DarkThemeStylesheet:
    def __init__(self):
        gb_indicator_checked = "./cratonml_gui/Themes/images/dark/check_mark.png"
        gb_indicator_checked_disabled = (
            "./cratonml_gui/Themes/images/dark/check_mark_disable.png"
        )
        scroll_bar_add_line_vert = "./cratonml_gui/Themes/images/dark/down_arrow.png"
        scroll_bar_sub_line_vert = "./cratonml_gui/Themes/images/dark/up_arrow.png"
        scroll_bar_add_line_hor = "./cratonml_gui/Themes/images/dark/right_arrow.png"
        scroll_bar_sub_line_hor = "./cratonml_gui/Themes/images/dark/left_arrow.png"

        check_box_indicator_checked = "./cratonml_gui/Themes/images/dark/check_mark.png"
        check_box_indicator_disabled = (
            "./cratonml_gui/Themes/images/dark/check_mark_disable.png"
        )

        if getattr(sys, "frozen", False):
            gb_indicator_checked = Path(sys._MEIPASS, gb_indicator_checked).as_posix()
            gb_indicator_checked_disabled = Path(
                sys._MEIPASS, gb_indicator_checked_disabled
            ).as_posix()
            scroll_bar_add_line_vert = Path(
                sys._MEIPASS, scroll_bar_add_line_vert
            ).as_posix()
            scroll_bar_sub_line_vert = Path(
                sys._MEIPASS, scroll_bar_sub_line_vert
            ).as_posix()
            scroll_bar_add_line_hor = Path(
                sys._MEIPASS, scroll_bar_add_line_hor
            ).as_posix()
            scroll_bar_sub_line_hor = Path(
                sys._MEIPASS, scroll_bar_sub_line_hor
            ).as_posix()
            check_box_indicator_checked = Path(
                sys._MEIPASS, check_box_indicator_checked
            ).as_posix()
            check_box_indicator_disabled = Path(
                sys._MEIPASS, check_box_indicator_disabled
            ).as_posix()

        self.stylesheet = self.get_stylesheet(
            gb_indicator_checked,
            gb_indicator_checked_disabled,
            scroll_bar_add_line_vert,
            scroll_bar_sub_line_vert,
            scroll_bar_add_line_hor,
            scroll_bar_sub_line_hor,
            check_box_indicator_checked,
            check_box_indicator_disabled,
        )

    @staticmethod
    def get_stylesheet(
        gb_indicator_checked,
        gb_indicator_checked_disabled,
        scroll_bar_add_line_vert,
        scroll_bar_sub_line_vert,
        scroll_bar_add_line_hor,
        scroll_bar_sub_line_hor,
        check_box_indicator_checked,
        check_box_indicator_disabled,
    ):
        stylesheet = """
            QWidget {
              background-color: #19232d;
              border-color: #455364;
            }
            QMenuBar{
                background-color: #19232d;
                color: #fff;
                border-color: #051a39;
            }
            QLabel {
              color: #e0e1e3;
              font-weight: 600;
            }
            QLabel::disabled {
                color: #999999;
            }
            
            QLineEdit {
              color: #e0e1e3;
              font-weight: 600;
              border-radius: 8px;
              border: 1px solid #455364;
              padding: 5px 15px;
            }
            QLineEdit:focus {
              border: 1px solid #455364;
            }
            QLineEdit::placeholder {
              color: #e0e1e3;
            }
            QLineEdit::disabled {
                color: #999999;
            }
            
            QPushButton {
              background-color: #2c3e4f;
              color: #e0e1e3;
              font-weight: 600;
              border-radius: 8px;
              border: 1px solid #455364;
              padding: 5px 15px;
              outline: 0px;
            }
            QPushButton:hover, QPushButton:focus {
              background-color: #3f5870;
              border: 3px solid #2c3e4f;
            }
            QPushButton::disabled {
              color: #19232d;
              background-color: #23313f;
              border-color: #23313f;
            }
            
            QSpinBox, QDoubleSpinBox {
              background-color: #19232d;
              border-radius: 3px;
              border: 1px solid #455364;
              padding: 2px;
              color: #e0e1e3;
              font-weight: 600;
            }
            QSpinBox::disabled, QDoubleSpinBox::disabled {
                color: #999999;
            }
            
            QGroupBox {
              color: #e0e1e3;
              font-weight: 600;
              border-radius: 4px;
              border: 1px solid #455364;
              padding: 5px 7px;
              margin-top: 10px;
            }
            QGroupBox::title{
              padding: 0px 8px;
              subcontrol-origin: margin;
            }
            QGroupBox:indicator {
              border: 1px solid #455364;
            }
            QGroupBox:indicator:checked {
              background-image: url(gb_indicator_checked);
            }
            QGroupBox::title::disabled {
                color: #999999;
            }
            QGroupBox::indicator::checked::disabled {
              background-image: url(check_box_indicator_disabled);
            }
            
            QScrollArea {
              border: 0px;
            }
            QScrollBar:vertical {
              background-color: #19232d;
              border-radius: 4px;
              border: 1px solid #37414f;
              margin: 15px 1px 15px 1px;
            }
            QScrollBar:horizontal {
              background-color: #19232d;
              border-radius: 4px;
              border: 1px solid #37414f;
              margin: 1px 15px 1px 15px;
            }
            QScrollBar::handle:vertical{
                background: #3f5870;
                border-radius: 4px;
                border: 1px solid #37414f;
                min-height: 5px;
            }
            QScrollBar::handle:horizontal{
                background: #3f5870;
                border-radius: 4px;
                border: 1px solid #37414f;
                min-width: 5px;
            }
            QScrollBar::add-line:vertical {
                background-color: #19232d;
                margin: 1px 0px 1px 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
                height: 10px;
                width: 10px;
                background-image: url(scroll_bar_add_line_vert);
            }
            QScrollBar::sub-line:vertical {
                background-color: #19232d;
                margin: 1px 0px 1px 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
                height: 10px;
                width: 10px;
                background-image: url(scroll_bar_sub_line_vert);
            }
            QScrollBar::add-line:horizontal {
                background-color: #19232d;
                margin: 1px 0px 1px 0px;
                subcontrol-position: right;
                subcontrol-origin: margin;
                height: 10px;
                width: 10px;
                background-image: url(scroll_bar_add_line_hor);
            }
            QScrollBar::sub-line:horizontal {
                background-color: #19232d;
                margin: 1px 0px 1px 0px;
                subcontrol-position: left;
                subcontrol-origin: margin;
                height: 10px;
                width: 10px;
                background-image: url(scroll_bar_sub_line_hor);
            }
            QScrollBar::sub-line:vertical:hover, QScrollBar::sub-line:vertical:on {
                height: 10px;
                width: 10px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
            QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {
                height: 10px;
                width: 10px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:horizontal:hover, QScrollBar::sub-line:horizontal:on {
                height: 10px;
                width: 10px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }
            QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:on {
                height: 10px;
                width: 10px;
                subcontrol-position: right;
                subcontrol-origin: margin;
            }
            QScrollBar::add-page, QScrollBar::sub-page {
                background: none;
            }
            
            QTabBar::tab {
              background-color: #37414f;
              color: #e0e1e3;
              padding: 6px;
              border-radius: 3px;
              border: 1px solid #455364;
              font-weight: 600;
            }
            QTabBar::tab:selected {
              background-color: #455364;
              border: 1px solid #455364;
            }
            QTabWidget::pane{
              background-color: #19232d;
              border-radius: 4px;
              border: 1px solid #455364;
            }
            
            QCheckBox {
              color: #e0e1e3;
              font-weight: 600;
            }
            QCheckBox::indicator {
              border: 1px solid #455364;
            }
            QCheckBox::indicator:checked {
              background-image: url(check_box_indicator_checked);
            }
            QCheckBox::indicator::checked::disabled {
              background-image: url(check_box_indicator_disabled);
            }
            QCheckBox::disabled {
                color: #999999;
            }
            
            QListWidget {
              color: #e0e1e3;
              font-weight: 600;
              border-radius: 2px;
              border: 1px solid #455364;
            }
            QListWidget::disabled {
                color: #999999;
            }
            QListWidget:indicator {
              border: 1px solid #455364;
            }
            QListWidget:indicator:checked {
              background-image: url(gb_indicator_checked);
            }
            QListWidget::indicator::checked::disabled {
              background-image: url(check_box_indicator_disabled);
            }
            
            QComboBox {
              color: #e0e1e3;
              font-weight: 600;
              border-radius: 2px;
              border: 1px solid #455364;
            }
            QComboBox QAbstractItemView{
                color: #e0e1e3;
            }
            QComboBox::disabled {
                color: #999999;
            }
            
            QPlainTextEdit {
              border-radius: 3px;
              border: 1px solid #455364;
            }
            QPlainTextEdit::disabled {
                color: #999999;
            }
            
            QProgressBar {
              color: #e0e1e3;
              font-weight: 700;
              border: 1px solid #455364;
              border-radius: 4px;
              text-align: center;
            }
            QProgressBar:chunk {
             background-color: #26486b;
            }
            
            QTableWidget {
                background-color: #19232d;
                color: #e0e1e3;
                font: 14px;
            }
            QHeaderView::section {
                background-color: #19232d;
                color: #e0e1e3;
                height: 50px;
                width: 100px; 
                font: 14px;
            }  
            QTableView QTableCornerButton::section {
                background-color: #19232d;
            } 
            
            QHBoxLayout {
                background-color: #19232d;
            }
        """
        stylesheet = stylesheet.replace("gb_indicator_checked", gb_indicator_checked)
        stylesheet = stylesheet.replace(
            "scroll_bar_add_line_vert", scroll_bar_add_line_vert
        )
        stylesheet = stylesheet.replace(
            "scroll_bar_sub_line_vert", scroll_bar_sub_line_vert
        )
        stylesheet = stylesheet.replace(
            "scroll_bar_add_line_hor", scroll_bar_add_line_hor
        )
        stylesheet = stylesheet.replace(
            "scroll_bar_sub_line_hor", scroll_bar_sub_line_hor
        )
        stylesheet = stylesheet.replace(
            "check_box_indicator_checked", check_box_indicator_checked
        )
        stylesheet = stylesheet.replace(
            "check_box_indicator_disabled", check_box_indicator_disabled
        )
        return stylesheet
