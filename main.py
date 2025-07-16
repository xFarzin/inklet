import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplitter, QWidget, QHBoxLayout
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtCore import Qt, QSettings, QTimer
from InkEditor import InkEditor
from InkFileManager import InkFileManager
import os
import core  

class MainWindow(QMainWindow,):
    def __init__(self,theme):
        super().__init__()
        
        self.setWindowTitle("Inklet")
        self.resize(1000, 600)
        
        self.apply_theme(theme_path)
        
        # 🖥️ Initialize InkEditor And InkFileManager
        self.editor = InkEditor()
        self.fileManager = InkFileManager(Editor = self.editor)
        self.editor.loadPlugins() # Load plugins after initializing InkEditor
        
        # 🪄 Create splitter layout
        splitter = QSplitter()
        splitter.setChildrenCollapsible(False)

        # 📂 Left: File Manager
        splitter.addWidget(self.fileManager)

        # 🖋️ Right: Editor
        splitter.addWidget(self.editor)
        
        # 📏 Set stretch factors 
        splitter.setSizes([200, 800])
        
        # 🌟 Set splitter as central layout
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter)
        self.setCentralWidget(container)

        # ⌨️ Ctrl+Q to exit
        shortcut_exit = QShortcut(QKeySequence("Ctrl+Q"), self)
        shortcut_exit.activated.connect(self.close)
        
        QShortcut(QKeySequence("F11"), self, activated=self.toggleZenMode)
        
        # 🖱  Load Last Session️
        settings = QSettings("Inklet", "Session")
        filepath = settings.value("lastFilePath", "")
        scroll = int(settings.value("scrollValue", 0))

        if filepath and os.path.exists(filepath):
            self.editor.loadFile(filepath)
            QTimer.singleShot(100, lambda: self.editor.editor.verticalScrollBar().setValue(scroll))
        
        # Command Palette Shortcut
        QShortcut(QKeySequence("Ctrl+Shift+P"), self, activated=self.showCommandPalette)
        
        # Help Overlay Shortcut
        QShortcut(QKeySequence("Ctrl+?"), self, activated=self.showHelpOverlay)


    def apply_theme(self, theme_path):
        if theme_path:
            try:
                with open(theme_path, "r") as f:
                    self.setStyleSheet(f.read())
                print(f"🎨 Theme applied to MainWindow from: {theme_path}")
            except Exception as e:
                print(f"⚠️ Failed to apply theme: {e}")

    def toggleZenMode(self):
        is_fullscreen = self.windowState() == Qt.WindowState.WindowFullScreen

        if is_fullscreen:
            self.showNormal()
            if self.menuBar():
                self.menuBar().show()
            print("🎯 Exited Zen Mode")
        else:
            self.showFullScreen()
            if self.menuBar():
                self.menuBar().hide()
            print("🧘 Entered Zen Mode")

    def closeEvent(self, event):
        settings = QSettings("Inklet", "Session")
        settings.setValue("lastFilePath", self.editor.filepath)
        settings.setValue("scrollValue", self.editor.editor.verticalScrollBar().value())
        event.accept()

    def showCommandPalette(self):
        dialog = core.CommandPalette(self)
        dialog.exec()
    
    def showHelpOverlay(self):
        dialog = core.ShortcutHelpDialog(self)
        dialog.exec()




if __name__ == "__main__":
    
    theme_path = "themes/dark.qss"
    
    app = QApplication(sys.argv)
    window = MainWindow(theme = theme_path)
    window.show()
    sys.exit(app.exec())
