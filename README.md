

# ✍️ Inklet

**Inklet** is a minimal, modular text and code editor built with **Python + PyQt6**. Designed to be light on system resources, Inklet is perfect for low-end machines and easy to integrate into any PyQt6-based project.

---

## 🧩 Features

- ✅ **Modular Design** — Drop Inklet into any PyQt6 project with ease
- 🚀 **Lightweight** — Fast and responsive even on low-end hardware
- 🎨 **Theme Support** — Easily customize the look using external `.qss` stylesheets
- 🖋️ **Plain Text & Code Editing** — Clean interface for scripts, configs, or embedded tools
- 🔌 **Embed-Ready** — Just import and place wherever you need editing capabilities

---

## 💡 Use Cases

Inklet is ideal for:
- Game engines and dev tools (like Wronggine 🧪)
- Markdown or note editors
- Config panels and quick scripting consoles
- Any GUI app that needs a lightweight embedded editor

---

## 🚀 Quick Start
```python
from inklet import InkEditor
editor = InkEditor()
```

---

## ⌨️ Keyboard Shortcuts

### ⚙️ Main Shortcuts
> _These shortcuts are only active when Inklet is run directly (i.e. `__name__ == "__main__"`). They won't trigger when you import the editor or file manager into another application._

| ⌨️ Shortcut        | 🚀 Action            |
|-------------------|---------------------|
| `Ctrl + Q`        | Exit the application |

---

### ✍️ Editor Shortcuts

| ⌨️ Shortcut        | 📄 Action             |
|-------------------|----------------------|
| `Ctrl + S`        | Save current file     |
| `Ctrl + Shift + S`| Save As new file      |

---

### 📁 File Manager Shortcuts

| ⌨️ Shortcut        | 📂 Action               |
|-------------------|------------------------|
| `Ctrl + O`        | Open file dialog        |
| `Ctrl + Shift + O`| Open folder dialog      |
| *(Double-click)*  | Load selected file into editor |


---

For a full-featured demo and integration examples, check out `examples/` after setup.  
Need a branded logo or theme switcher? Inklet is ready to customize 🖋️🌒

