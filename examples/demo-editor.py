import sys,os
from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QSplitter, QWidget
from PyQt6.QtGui import QKeySequence, QShortcut

# Just because its in examples dir...
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from InkEditor import InkEditor
from InkFileManager import InkFileManager

class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inklet Demo — Dark Mode")
        self.resize(1200, 700)

        self.theme_path = "themes/dark.qss"
        self.apply_theme(self.theme_path)

        # Initialize components
        self.editor = InkEditor()
        self.fileManager = InkFileManager(Editor=self.editor,)

        # Layout
        splitter = QSplitter()
        splitter.addWidget(self.fileManager)
        splitter.addWidget(self.editor)
        splitter.setSizes([240, 960])

        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter)
        self.setCentralWidget(container)

        # Setup main shortcuts
        self.setup_shortcuts()

    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+Q"), self).activated.connect(self.close)
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(self.editor.saveFile)
        QShortcut(QKeySequence("Ctrl+Shift+S"), self).activated.connect(self.editor.saveFileAs)

    def apply_theme(self, theme_path):
        try:
            with open(theme_path, "r") as f:
                self.setStyleSheet(f.read())
            print(f"🎨 Theme loaded: {theme_path}")
        except Exception as e:
            print(f"⚠️ Failed to load theme: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DemoWindow()
    window.show()
    sys.exit(app.exec())
