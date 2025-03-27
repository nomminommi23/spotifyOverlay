from PyQt5 import QtWidgets, QtCore


class SettingsWindow(QtWidgets.QWidget):
    # Erstellen Sie ein benutzerdefiniertes Signal
    settings_applied = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.WindowMinimizeButtonHint
        )

        self.setWindowTitle("Einstellungen")

        # Layout erstellen
        layout = QtWidgets.QVBoxLayout()

        # Widgets erstellen
        self.color_input = QtWidgets.QLineEdit()
        self.position_input = QtWidgets.QLineEdit()

        # Widgets zum Layout hinzufügen
        layout.addWidget(QtWidgets.QLabel("Textfarbe:"))
        layout.addWidget(self.color_input)
        layout.addWidget(QtWidgets.QLabel("Position:"))
        layout.addWidget(self.position_input)

        # Schaltflächen erstellen
        self.ok_button = QtWidgets.QPushButton("OK")
        self.cancel_button = QtWidgets.QPushButton("Abbrechen")

        # Schaltflächen verbinden
        self.ok_button.clicked.connect(self.emit_settings)
        self.cancel_button.clicked.connect(self.close)

        # Schaltflächen zum Layout hinzufügen
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

        # Dialog-Layout festlegen
        self.setLayout(layout)

    def emit_settings(self):
        color, position = self.get_inputs()
        self.settings_applied.emit(color, position)

    def get_inputs(self):
        return self.color_input.text(), self.position_input.text()
