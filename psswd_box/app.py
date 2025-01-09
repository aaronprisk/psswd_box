import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QCheckBox,
    QLabel,
    QVBoxLayout,
    QComboBox,
    QHBoxLayout,
    QSpinBox,
)

from password_generator import PasswordGenerator
from file_handler import FileHandler


icon = FileHandler("images/psswd_box.png")

config_file = FileHandler("configs/config.yaml")
themes_file = FileHandler("configs/themes.yaml")

config = config_file.load_yaml_file()
themes = themes_file.load_yaml_file()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # * Set window default settings
        self.setWindowTitle(config["window_title"])
        self.setFixedSize(
            config["window_size"]["width"], config["window_size"]["height"]
        )
        self.setWindowIcon(QIcon(icon.get_file_path()))

        # *  Define normal variables
        self.theme_list = [theme for theme in list(themes)[:-1]]

        # * Create end user widgets and apply settings to them
        self.generate_password = QPushButton("Generate Password")

        self.password = QLabel(
            " ", alignment=Qt.AlignmentFlag.AlignCenter, wordWrap=False
        )
        self.password.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
            | Qt.TextInteractionFlag.TextSelectableByKeyboard
        )

        self.lowercase_letters = QCheckBox("Lowercase Letters")
        self.lowercase_letters.setCheckState(Qt.CheckState.Checked)

        self.uppercase_letters = QCheckBox("Uppercase Letters")
        self.uppercase_letters.setCheckState(Qt.CheckState.Checked)

        self.numbers = QCheckBox("Numbers")
        self.numbers.setCheckState(Qt.CheckState.Checked)

        self.symbols = QCheckBox("Symbols")
        self.symbols.setCheckState(Qt.CheckState.Checked)

        self.num_characters = QSpinBox(prefix="Number of Characters: ")
        self.num_characters.setRange(
            config["num_characters"]["min"], config["num_characters"]["max"]
        )
        self.num_characters.setValue(config["num_characters"]["default"])

        self.theme_toggle = QPushButton("Dark")

        # * Define button connections and/or actions
        self.generate_password.pressed.connect(self.get_password)
        self.theme_toggle.pressed.connect(self.toggle_theme)

        # * Create layouts
        self.page = QVBoxLayout()
        self.row_three = QHBoxLayout()
        self.row_four = QHBoxLayout()

        # * Add widgets to layouts
        self.row_three.addWidget(self.lowercase_letters)
        self.row_three.addWidget(self.uppercase_letters)
        self.row_three.addWidget(self.numbers)
        self.row_three.addWidget(self.symbols)

        self.row_four.addWidget(self.num_characters)
        self.row_four.addWidget(self.theme_toggle)

        # * Setup overall page layout and set default window theme
        self.page.addWidget(self.password)
        self.page.addWidget(self.generate_password)
        self.page.addLayout(self.row_three)
        self.page.addLayout(self.row_four)

        self.gui = QWidget()
        self.gui.setLayout(self.page)

        self.setCentralWidget(self.gui)

        self.apply_theme(self.theme_toggle.text().lower())

    def get_password(self):
        character_types = self.get_character_types()
        if character_types == ["n", "n", "n", "n"]:
            self.password.setText("You MUST select one of the character types below!")
        else:
            psswd = PasswordGenerator()
            self.password.setText(
                psswd.generate_password(character_types, self.num_characters.value())
            )

    def get_character_types(self):
        lowercase_letters_value = "y" if self.lowercase_letters.isChecked() else "n"
        uppercase_letters_value = "y" if self.uppercase_letters.isChecked() else "n"
        numbers_value = "y" if self.numbers.isChecked() else "n"
        symbols_value = "y" if self.symbols.isChecked() else "n"
        character_types = [
            lowercase_letters_value,
            uppercase_letters_value,
            numbers_value,
            symbols_value,
        ]

        return character_types

    def toggle_theme(self):
        if self.theme_toggle.text() == "Dark":
            self.theme_toggle.setText("Light")
            theme = self.theme_toggle.text()
        else:
            self.theme_toggle.setText("Dark")
            theme = self.theme_toggle.text()

        self.apply_theme(theme.lower())

    def apply_theme(self, theme):
        self.main_stylesheet = f"""
            background-color: {themes[theme]['background-color']};
            color: {themes[theme]['color']};
            border: {themes[theme]['border']};
            border-radius: {themes['general']['border-radius']};
            padding: {themes['general']['padding']};
            """
        self.widget_stylesheet = f"""
            background-color: {themes[theme]['widget-background-color']};
            """
        self.setStyleSheet(self.main_stylesheet)
        self.password.setStyleSheet(self.widget_stylesheet)
        self.generate_password.setStyleSheet(self.widget_stylesheet)
        self.lowercase_letters.setStyleSheet(self.widget_stylesheet)
        self.uppercase_letters.setStyleSheet(self.widget_stylesheet)
        self.numbers.setStyleSheet(self.widget_stylesheet)
        self.symbols.setStyleSheet(self.widget_stylesheet)
        self.theme_toggle.setStyleSheet(self.widget_stylesheet)
        self.num_characters.setStyleSheet(self.widget_stylesheet)

        (
            self.theme_toggle.setText("Dark")
            if theme == "dark"
            else self.theme_toggle.setText("Light")
        )


def main():
    app = QApplication(sys.argv)
    app.setStyle("Breeze")
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
