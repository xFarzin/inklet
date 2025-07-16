from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFileDialog,
    QPlainTextEdit, QTextEdit, QDialog, QHBoxLayout,
    QLineEdit, QPushButton
)
from PyQt6.QtGui import (
    QPainter, QTextFormat, QFont, QKeySequence, QShortcut,
    QSyntaxHighlighter, QTextCharFormat, QColor
)
from PyQt6.QtCore import Qt, QRect, QSize, QTimer
import os, re, importlib.util


# 🔧 Settings
highlight_cl = False  # Highlight current line toggle


# 🧮 Line Number Area
class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self._editor = editor

    def sizeHint(self):
        return QSize(self._editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self._editor.line_number_area_paint_event(event)


# ✍️ Code Editor
class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Consolas", 12))
        self.setPlaceholderText("Type your code here...")
        self.line_number_area = LineNumberArea(self)
        
        # 🖌️ Syntax highlighter
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        
        self.update_line_number_area_width(0)
        syntax_theme_colors = load_syntax_colors("themes/syntax.qss")
        self.highlighter = PythonSyntaxHighlighter(self.document(), syntax_theme_colors)

        self.highlighter = PythonSyntaxHighlighter(self.document())
        
        self.setAcceptDrops(True) # Enable drag & drop

        
    def line_number_area_width(self):
        digits = len(str(max(1, self.blockCount())))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(
                0, rect.y(), self.line_number_area.width(), rect.height()
            )
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height())
        )

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), Qt.GlobalColor.transparent)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.GlobalColor.white)
                font_height = self.fontMetrics().height()
                painter.drawText(
                    0, top, self.line_number_area.width() - 5, font_height,
                    Qt.AlignmentFlag.AlignRight, number
                )
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1

    def highlight_current_line(self):
        if not highlight_cl or self.isReadOnly():
            return
        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(Qt.GlobalColor.darkMagenta)
        selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        self.setExtraSelections([selection])

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            filepath = url.toLocalFile()
            if filepath:
                # Call loadFile from InkEditor
                if hasattr(self.parent(), 'loadFile'):
                    self.parent().loadFile(filepath)

                





class PythonSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document, colors=None):
        super().__init__(document)
        self.highlight_rules = []

        def fmt(color_str, bold=False):
            format = QTextCharFormat()
            format.setForeground(QColor(color_str))
            if bold:
                format.setFontWeight(QFont.Weight.Bold)
            return format

        # Fallbacks if no theme provided
        default_colors = {
            "syntax-keyword": "#ff79c6",
            "syntax-string": "#f1fa8c",
            "syntax-comment": "#6272a4",
            "syntax-number": "#bd93f9"
        }
        if colors is None:
            colors = default_colors
        else:
            # Fill missing keys with defaults
            for key in default_colors:
                colors.setdefault(key, default_colors[key])

        # Highlight formats
        keyword_format = fmt(colors["syntax-keyword"], bold=True)
        string_format  = fmt(colors["syntax-string"])
        comment_format = fmt(colors["syntax-comment"])
        number_format  = fmt(colors["syntax-number"])

        # Keyword patterns
        keywords = [
            r"\bdef\b", r"\bclass\b", r"\breturn\b", r"\bif\b", r"\belse\b",
            r"\bwhile\b", r"\bfor\b", r"\bimport\b", r"\bfrom\b", r"\btry\b",
            r"\bexcept\b", r"\bwith\b", r"\bas\b", r"\blambda\b", r"\bNone\b",
            r"\bTrue\b", r"\bFalse\b", r"\bself\b"
        ]
        for kw in keywords:
            self.highlight_rules.append((re.compile(kw), keyword_format))

        # Other rules
        self.highlight_rules.append((re.compile(r"(\".*?\"|\'.*?\')"), string_format))
        self.highlight_rules.append((re.compile(r"#.*"), comment_format))
        self.highlight_rules.append((re.compile(r"\b\d+(\.\d+)?\b"), number_format))

    def highlightBlock(self, text):
        for pattern, style in self.highlight_rules:
            for match in pattern.finditer(text):
                start, length = match.start(), match.end() - match.start()
                self.setFormat(start, length, style)




# 🔍 Floating Find & Replace Dialog
class FindReplaceDialog(QDialog):
    def __init__(self, parent_editor):
        super().__init__(parent_editor)
        self.setWindowTitle("Find & Replace")
        self.setFixedSize(400, 120)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.Tool)
        self.editor = parent_editor.editor

        layout = QVBoxLayout(self)

        self.find_input = QLineEdit()
        self.find_input.setPlaceholderText("Find...")
        self.replace_input = QLineEdit()
        self.replace_input.setPlaceholderText("Replace with...")

        button_layout = QHBoxLayout()
        find_btn = QPushButton("Find")
        replace_btn = QPushButton("Replace")
        replace_all_btn = QPushButton("Replace All")
        close_btn = QPushButton("Close")

        find_btn.clicked.connect(self.find_text)
        replace_btn.clicked.connect(self.replace_text)
        replace_all_btn.clicked.connect(self.replace_all)
        close_btn.clicked.connect(self.close)

        button_layout.addWidget(find_btn)
        button_layout.addWidget(replace_btn)
        button_layout.addWidget(replace_all_btn)
        button_layout.addWidget(close_btn)

        layout.addWidget(self.find_input)
        layout.addWidget(self.replace_input)
        layout.addLayout(button_layout)

    def find_text(self):
        query = self.find_input.text()
        cursor = self.editor.textCursor()
        new_cursor = self.editor.document().find(query, cursor)
        if new_cursor.isNull():
            new_cursor = self.editor.document().find(query)
        if not new_cursor.isNull():
            self.editor.setTextCursor(new_cursor)

    def replace_text(self):
        query = self.find_input.text()
        replacement = self.replace_input.text()
        cursor = self.editor.textCursor()
        if cursor.hasSelection() and cursor.selectedText() == query:
            cursor.insertText(replacement)

    def replace_all(self):
        query = self.find_input.text()
        replacement = self.replace_input.text()
        text = self.editor.toPlainText().replace(query, replacement)
        self.editor.setPlainText(text)


# 🖋️ InkEditor Container
class InkEditor(QWidget):
    def __init__(self):
        
        

        # Initialize idle timer to save if dirty
        self.idle_timer = QTimer()
        self.idle_timer.setInterval(10000)  # 10 seconds
        self.idle_timer.timeout.connect(self.save_if_dirty)
        self.idle_timer.start() # Start the timer

        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.editor = CodeEditor()
        layout.addWidget(self.editor)

        self.search_dialog = FindReplaceDialog(self)

        self.current_path = None
        self.setup_shortcuts()

    def loadFile(self, file_path):
        print(f"📂 Loading file: {file_path}")
        self.filepath = file_path
        if not os.path.exists(file_path):
            self.editor.setPlainText(f"⚠️ File not found: {file_path}")
            return
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                contents = f.read()
                self.editor.setPlainText(contents)
            self.current_path = file_path
            print(f"✅ File loaded")
        except Exception as e:
            self.editor.setPlainText(f"⚠️ Failed to load: {e}")
            print(f"❌ Load error: {e}")

    def saveFile(self):
        if not self.current_path:
            print("🕳️ No file loaded — using Save As")
            self.saveFileAs()
            return
        try:
            with open(self.current_path, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            print(f"💾 File saved to: {self.current_path}")
        except Exception as e:
            print(f"❌ Save failed: {e}")

    def saveFileAs(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File As", "", "All Files (*);;Python Files (*.py);;Text Files (*.txt)"
        )
        if not file_path:
            print("🚫 Save cancelled")
            return
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            self.current_path = file_path
            print(f"✅ File saved as: {file_path}")
        except Exception as e:
            print(f"❌ Save As failed: {e}")

    def setup_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+S"), self).activated.connect(self.saveFile)
        QShortcut(QKeySequence("Ctrl+Shift+S"), self).activated.connect(self.saveFileAs)
        QShortcut(QKeySequence("Ctrl+F"), self).activated.connect(self.show_search_dialog)

    def show_search_dialog(self):
        self.search_dialog.show()
        self.search_dialog.raise_()
        self.search_dialog.activateWindow()

    def save_if_dirty(self):
        print("📝 Checking if its dirty")
        if self.editor.document().isModified():
            self.saveFile()
            print("📝 Its dirty, saving sir...")
            self.editor.document().setModified(False)



    def loadPlugins(self):
        plugin_dir = os.path.join(os.getcwd(), "plugins")
        for fname in os.listdir(plugin_dir):
            if fname.endswith(".py"):
                path = os.path.join(plugin_dir, fname)
                spec = importlib.util.spec_from_file_location(fname[:-3], path)
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                    if hasattr(module, "register"):
                        module.register(self)
                        print(f"✅ Loaded plugin: {fname}")
                except Exception as e:
                    print(f"❌ Failed to load {fname}: {e}")


    def addCommand(self, name, callback):
        if not hasattr(self, "externalCommands"):
            self.externalCommands = {}
        self.externalCommands[name] = callback







def load_syntax_colors(qss_path):
    colors = {}
    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("syntax-") and ":" in line:
                    key, value = line.split(":")
                    colors[key.strip()] = value.strip().rstrip(";")
    except Exception as e:
        print(f"⚠️ Failed to load syntax colors: {e}")
    return colors