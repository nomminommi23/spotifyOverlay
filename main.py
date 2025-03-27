import sys

import requests
from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui
from secondwindow import SettingsWindow
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import art
import http.server
import httpserver


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint |
            QtCore.Qt.WindowTransparentForInput
            )
        self.setGeometry(QtWidgets.QStyle.alignedRect(
            QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter,
            QtCore.QSize(1120, 320),
            QtWidgets.QApplication.desktop().availableGeometry()))
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.move(50, 50)

        # Create a QLabel
        self.label = QtWidgets.QLabel("Hello World", self)
        self.label.setStyleSheet("color: white")  # Set the text color to black
        font = QtGui.QFont("Arial", 16, QtGui.QFont.Bold)
        self.label.setFont(font)

        self.label.setWordWrap(True)
        self.label.adjustSize()
        self.text = "Hello World"

        # Position the label at the center of the window
        self.label.move(0, 0)

    # Create a QTimer
        self.update_label()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.timer.start(30000)  # Update every 30 seconds
        self.open_settings()

    def open_settings(self): # Open the settings window
        self.settings_window = SettingsWindow() # Create an instance of the SettingsWindow class
        self.settings_window.settings_applied.connect(self.apply_settings) # Connect the signal to the slot
        self.settings_window.show()

    def apply_settings(self, color, position): # Apply the settings
        if color:
            self.label.setStyleSheet(f"color: {color}")
        if position:
            try:
                x, y = map(int, position.split(','))
                self.move(x, y)
            except ValueError:
                pass  # Ungültige Positionseingabe ignorieren
    def update_label(self):
        with open("config.json", "r") as f:
            data = f.read()
            f.close()
        data = json.loads(data)
        client_id = data["client_id"]
        client_secret = data["client_secret"]
        redirect_uri = "https://discord.gg/Dan8jF3Q3q"
        scope = "user-read-currently-playing"
        username = data["username"]
        try:
            token = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                                scope=scope, username=username)
            spotify = spotipy.Spotify(auth_manager=token)
            current_song = spotify.current_user_playing_track()
        except Exception as e:
            print(e)
            current_song = None
        # Update the text of the QLabel
        if current_song is None:
            self.text = "No song is currently playing"
        else:
            self.text = (f"song: {current_song['item']['name']} \nartist: "
                         f"{current_song['item']['artists'][0]['name']} "
                         f"\nalbum: {current_song['item']['album']['name']}")
        self.label.setText(self.text)  # Replace "New Text" with the text you want to display
        self.label.adjustSize()
        self.label.setWordWrap(True)



app = QtWidgets.QApplication(sys.argv)
myWindow = MyMainWindow()
myWindow.show()
app.exec_()