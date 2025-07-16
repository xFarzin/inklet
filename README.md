

# ✍️ Inklet

**Inklet** is a minimal, modular text and code editor built with **Python + PyQt6**. Designed to be light on system resources, Inklet is perfect for low-end machines and easy to integrate into any PyQt6-based project.

---


## 🧩 Features

- ✅ **Modular Design** — Drop Inklet into any PyQt6 project with ease  
- 🚀 **Lightweight** — Fast and responsive even on low-end hardware  
- 🎨 **Theme Support** — Easily customize the look using external `.qss` stylesheets  
- 🔍 **Floating Find & Replace** — Summonable via `Ctrl + F`, unobtrusive and focused  
- 🧮 **Line Number Support** — Elegant and scroll-synced alongside the editor  
- 🖋️ **Python Syntax Highlighting** — Highlight keywords, strings, comments, and numbers  
- 📄 **Current Line Highlighting** — Optional focus feature for active line  
- 💾 **File Load/Save with Shortcuts** — Includes fallback Save As  
- 🎨 **QSS-Powered Syntax Styling** — Highlight colors defined in `syntax.qss`  
- 🧘 **Zen Mode (F11)** — Toggle fullscreen distraction-free view  
- 📂 **Drag & Drop File Loading** — Drop files directly into the editor to open  
- 🔄 **Session Restore** — Automatically reloads last opened file + scroll position  
- 🔌 **Plugin System** — Load external Python modules to add features dynamically  
- 🔮 **Command Palette (Ctrl+Shift+P)** — Search and trigger commands with fuzzy matching  
- ❔ **Shortcut Help Overlay (Ctrl+?)** — View all available keyboard shortcuts in one place  


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
> _Active only when run directly — not imported into other applications._

| ⌨️ Shortcut        | 🚀 Action               |
|-------------------|------------------------|
| `Ctrl + Q`        | Exit the application    |
| `F11`             | Toggle Zen Mode         |
| `Ctrl + ?`             | Show Help         |
---

### ✍️ Editor Shortcuts

| ⌨️ Shortcut        | 📄 Action               |
|-------------------|------------------------|
| `Ctrl + S`        | Save current file       |
| `Ctrl + Shift + S`| Save as new file        |
| `Ctrl + F`        | Open Find & Replace dialog |

---

### 📁 File Manager Shortcuts

| ⌨️ Shortcut        | 📂 Action                     |
|-------------------|------------------------------|
| `Ctrl + O`        | Open file dialog              |
| `Ctrl + Shift + O`| Open folder dialog            |
| *(Double-click)*  | Load selected file into editor |
| *(Drag file)*     | Drop file directly into editor |

---

## 🎨 Theme Configuration

Inklet uses `.qss` stylesheets for UI theming and syntax color definition:

```css
/* syntax.qss */
syntax-keyword: #ff79c6;
syntax-string:  #f1fa8c;
syntax-comment: #6272a4;
syntax-number:  #bd93f9;
```

Simply update the values to recolor highlights dynamically.

---

Explore `examples/` for full demos, or dive into extending Inklet with split views, Markdown preview, and more. Whether embedded in Wronggine or customized for your own app, Inklet is the aesthetic and functional core you’ve always wanted 💡🖋️
