import sys
from pathlib import Path


class LightThemeStylesheet:
    def __init__(self):
        gb_indicator_checked = "./cratonml_gui/Themes/images/light/check_mark.png"
        gb_indicator_checked_disabled = (
            "./cratonml_gui/Themes/images/light/check_mark_disable.png"
        )
        scroll_bar_add_line_vert = "./cratonml_gui/Themes/images/light/down_arrow.png"
        scroll_bar_sub_line_vert = "./cratonml_gui/Themes/images/light/up_arrow.png"
        scroll_bar_add_line_hor = "./cratonml_gui/Themes/images/light/right_arrow.png"
        scroll_bar_sub_line_hor = "./cratonml_gui/Themes/images/light/left_arrow.png"

        check_box_indicator_checked = (
            "./cratonml_gui/Themes/images/light/check_mark.png"
        )
        check_box_indicator_disabled = (
            "./cratonml_gui/Themes/images/light/check_mark_disable.png"
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
              background-color: #fff;
              border-color: #d0e3ff;
            }
            
            QLabel {
              color: #464d55;
              font-weight: 600;
            }
            QLabel::disabled {
                color: #999999;
            }
            
            QLineEdit {
              color: #464d55;
              font-weight: 600;
              border-radius: 8px;
              border: 1px solid #d0e3ff;
              padding: 5px 15px;
            }
            QLineEdit:focus {
              border: 1px solid #d0e3ff;
            }
            QLineEdit::placeholder {
              color: #464d55;
            }
            QLineEdit::disabled {
                color: #999999;
            }
            
            QPushButton {
              background-color: #8498d9;
              color: #fff;
              font-weight: 600;
              border-radius: 8px;
              border: 1px solid #5c76cc;
              padding: 5px 15px;
              outline: 0px;
            }
            QPushButton:hover, QPushButton:focus {
              background-color: #a8b6e3;
              border: 3px solid #8498d9;
            }
            QPushButton::disabled {
                background-color: #b5c1e8;
                border-color: #b5c1e8;
            }
            
            QSpinBox, QDoubleSpinBox {
              background-color: #fff;
              border-radius: 3px;
              border: 1px solid #d0e3ff;
              padding: 2px;
              color: #464d55;
              font-weight: 600;
            }
            QSpinBox::disabled, QDoubleSpinBox::disabled {
                color: #999999;
            }
            
            QGroupBox {
              color: #464d55;
              font-weight: 600;
              border-radius: 4px;
              border: 1px solid #d0e3ff;
              padding: 5px 7px;
              margin-top: 10px;
            }
            QGroupBox::title {
              padding: 0px 8px;
              subcontrol-origin: margin;
            }
            QGroupBox:indicator {
              border: 1px solid #5c6570;
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
            QGroupBox::indicator::disabled {
              border-color: #999999;
            }
            
            QScrollArea {
              border: 0px;
            }
            QScrollBar:vertical {
              background-color: #fff;
              border-radius: 4px;
              border: 1px solid #8ca9cf;
              margin: 15px 1px 15px 1px;
            }
            QScrollBar:horizontal {
              background-color: #fff;
              border-radius: 4px;
              border: 1px solid #8ca9cf;
              margin: 1px 15px 1px 15px;
            }
            QScrollBar::handle:vertical{
                background: #b0c4de;
                border-radius: 4px;
                border: 1px solid #8ca9cf;
                min-height: 5px;
            }
            QScrollBar::handle:horizontal{
                background: #b0c4de;
                border-radius: 4px;
                border: 1px solid #8ca9cf;
                min-width: 5px;
            }
            QScrollBar::add-line:vertical {
                background-color: #fff;
                margin: 1px 0px 1px 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
                height: 10px;
                width: 10px;
                background-image: url(scroll_bar_add_line_vert);
            }
            QScrollBar::sub-line:vertical {
                background-color: #fff;
                margin: 1px 0px 1px 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
                height: 10px;
                width: 10px;
                background-image: url(scroll_bar_sub_line_vert);
            }
            QScrollBar::add-line:horizontal {
                background-color: #fff;
                margin: 0px 1px 0px 1px;
                subcontrol-position: right;
                subcontrol-origin: margin;
                height: 10px;
                width: 10px;
                background-image: url(scroll_bar_add_line_hor);
            }
            QScrollBar::sub-line:horizontal {
                background-color: #fff;
                margin: 0px 1px 0px 1px;
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
              background-color: #d3dfed;
              color: #464d55;
              padding: 6px;
              border-radius: 3px;
              border: 1px solid #d0e3ff;
              font-weight: 600;
             }
            QTabBar::tab:selected {
              background-color: #f7fafc;
              border: 1px solid #d0e3ff;
            }
            QTabWidget::pane{
              background-color: #fff;
              border-radius: 4px;
              border: 1px solid #d0e3ff;
            }
            
            QCheckBox {
              color: #464d55;
              font-weight: 600;
            }
            QCheckBox::indicator {
              border: 1px solid #5c6570;
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
            QCheckBox::indicator::disabled {
              border-color: #999999;
            }
            
            QListWidget {
              color: #464d55;
              font-weight: 600;
              border-radius: 2px;
              border: 1px solid #d0e3ff;
            }
            QListWidget::disabled {
                color: #999999;
            }
            QListWidget:indicator {
              border: 1px solid #5c6570;
            }
            QListWidget:indicator:checked {
              background-image: url(gb_indicator_checked);
            }
            QListWidget::indicator::checked::disabled {
              background-image: url(check_box_indicator_disabled);
            }
            
            QComboBox {
              color: #464d55;
              font-weight: 600;
              border-radius: 2px;
              border: 1px solid #d0e3ff;
            }
            QComboBox QAbstractItemView{
                color: #464d55;
            }
            QComboBox::disabled {
                color: #999999;
            }
            
            QPlainTextEdit {
              border-radius: 3px;
              border: 1px solid #d0e3ff;
            }
            QPlainTextEdit::disabled {
                color: #999999;
            }
            
            QProgressBar {
              color: #464d55;
              font-weight: 700;
              border: 1px solid #3574e8;
              border-radius: 4px;
              text-align: center;
            }
            QProgressBar:chunk {
              background-color: #5d76cb;
            }
            
            QTableWidget {
                background-color: #fff;
                color: black;
                font: 14px;
            }
            QHeaderView::section {
                background-color: #fff;
                border-color: #3574e8;
                color: black;
                height: 50px;
                width: 100px; 
                font: 14px;
            }  
            QTableView QTableCornerButton::section {
                background-color: #fff;
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
