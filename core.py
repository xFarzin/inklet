from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QLabel
from PyQt6.QtCore import Qt, QSettings, QTimer
from PyQt6.QtGui import QKeySequence, QShortcut


class CommandPalette(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Command Palette")
        self.setFixedSize(400, 300)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Type a command...")
        self.list = QListWidget()

        layout = QVBoxLayout(self)
        layout.addWidget(self.input)
        layout.addWidget(self.list)

        self.commands = {
            "Help": parent.showHelpOverlay,
            "Save": parent.editor.saveFile,
            "Save As": parent.editor.saveFileAs,
            "Open File": parent.editor.loadFile,
            "Zen Mode": parent.toggleZenMode
        }

        if hasattr(self.parent().editor, "externalCommands"):
            self.commands.update(self.parent().editor.externalCommands)

        self.input.textChanged.connect(self.filterCommands)
        self.list.itemActivated.connect(self.executeCommand)
        self.populate()
    


    def populate(self):
        self.list.clear()
        for cmd in self.commands:
            self.list.addItem(cmd)

    def filterCommands(self, text):
        self.list.clear()
        for cmd in self.commands:
            if text.lower() in cmd.lower():
                self.list.addItem(cmd)

    def executeCommand(self, item):
        cmd = item.text()
        if cmd in self.commands:
            self.commands[cmd]()
            self.accept()


class ShortcutHelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Shortcut Help")
        self.setFixedSize(500, 400)

        layout = QVBoxLayout(self)
        shortcuts = [
            ("Ctrl + S", "Save"),
            ("Ctrl + Shift + S", "Save As"),
            ("Ctrl + O", "Open File"),
            ("F11", "Toggle Zen Mode"),
            ("Ctrl + Shift + P", "Command Palette"),
            ("Ctrl + F", "Find & Replace")
        ]

        for keys, action in shortcuts:
            label = QLabel(f"<b>{keys}</b> — {action}")
            layout.addWidget(label)
