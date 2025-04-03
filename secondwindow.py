from PyQt5 import QtWidgets, QtCore


class SettingsWindow(QtWidgets.QWidget):
    # Erstellen Sie ein benutzerdefiniertes Signal
    settings_applied = QtCore.pyqtSignal(str, str)
    quit_signal = QtCore.pyqtSignal(bool)
    visible_signal = QtCore.pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.WindowMinimizeButtonHint
        )

        self.setWindowTitle("Einstellungen")

        # Layout erstellen
        layout = QtWidgets.QVBoxLayout()
        self.isVisible = True

        # Widgets erstellen
        self.color_input = QtWidgets.QLineEdit()
        self.position_input = QtWidgets.QLineEdit()

        # Widgets zum Layout hinzufügen
        layout.addWidget(QtWidgets.QLabel("Textfarbe:"))
        layout.addWidget(self.color_input)
        layout.addWidget(QtWidgets.QLabel("Position:"))
        layout.addWidget(self.position_input)

        # Schaltflächen erstellen
        self.visibile_switch = QtWidgets.QCheckBox("Sichtbarkeit umschalten")
        self.ok_button = QtWidgets.QPushButton("OK")
        self.cancel_button = QtWidgets.QPushButton("Abbrechen")
        self.quit_button = QtWidgets.QPushButton("Beenden")

        # Schaltflächen verbinden
        self.visibile_switch.clicked.connect(self.switch_visibility)
        self.ok_button.clicked.connect(self.emit_settings)
        self.cancel_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(self.quit_event)

        # Schaltflächen zum Layout hinzufügen
        layout.addWidget(self.visibile_switch)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)
        layout.addWidget(self.quit_button)

        self.visibile_switch.setChecked(True)

        # Dialog-Layout festlegen
        self.setLayout(layout)

    def emit_settings(self):
        color, position = self.get_inputs()
        self.settings_applied.emit(color, position)

    def get_inputs(self):
        return self.color_input.text(), self.position_input.text()

    def quit_event(self):
        self.quit_signal.emit(True)

    def switch_visibility(self):
        self.isVisible = self.visibile_switch.isChecked()
        self.visible_signal.emit(self.isVisible)
