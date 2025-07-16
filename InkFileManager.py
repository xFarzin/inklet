from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTreeView,
    QFileDialog
)
from PyQt6.QtGui import QKeySequence, QFileSystemModel, QShortcut
from PyQt6.QtCore import QModelIndex, pyqtSignal
import os


class InkFileManager(QWidget):
    file_selected = pyqtSignal(str)

    def __init__(self, Editor, root_path=None):
        self.IsItWindows = os.name == 'nt'
        super().__init__()
        layout = QVBoxLayout(self)

        # ✅ Default Root
        if root_path is None:
            root_path = os.path.expanduser("~") if not self.IsItWindows else os.path.join(os.environ.get("USERPROFILE", ""), "Documents")

        root_path = os.path.abspath(root_path)
        self.root_path = root_path  # Save for later folder switch

        # 🌲 File System Model
        self.model = QFileSystemModel()
        self.model.setRootPath(self.root_path)

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.root_path))
        self.tree.setHeaderHidden(True)
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)
        self.tree.doubleClicked.connect(lambda index: self.open_file(self.model, index))

        layout.addWidget(self.tree)

        self.file_selected.connect(Editor.loadFile)

        # ⌨️ Shortcuts
        self.setup_shortcuts()

    def setup_shortcuts(self):
        # 📂 Open File: Ctrl+O
        open_file_shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        open_file_shortcut.activated.connect(self.open_file_dialog)

        # 📁 Open Folder: Ctrl+K, O
        open_folder_shortcut = QShortcut(QKeySequence("Ctrl+Shift+O"), self)
        open_folder_shortcut.activated.connect(self.open_folder_dialog)


    def open_file(self, model: QFileSystemModel, index: QModelIndex):
        file_path = model.filePath(index)
        if os.path.isfile(file_path):
            print(f"📂 File opened: {file_path}")
            self.file_selected.emit(file_path)

    def loadPath(self, path):
        print(f"📁 Loading path: {path}")
        path = os.path.abspath(path)
        if os.path.isdir(path):
            self.tree.setRootIndex(self.model.index(path))
        else:
            self.file_selected.emit(path)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open File", self.root_path,
            "All Files (*);;Python Files (*.py);;Text Files (*.txt)"
        )
        if file_path:
            print(f"📄 File chosen via dialog: {file_path}")
            self.file_selected.emit(file_path)

    def open_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, "Open Folder", self.root_path
        )
        if folder_path:
            print(f"📁 Folder chosen via dialog: {folder_path}")
            self.tree.setRootIndex(self.model.index(folder_path))
            self.root_path = folder_path
