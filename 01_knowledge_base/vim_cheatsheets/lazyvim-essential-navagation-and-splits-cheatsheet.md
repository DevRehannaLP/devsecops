# LazyVim Essential Navigation & Splits Cheat Sheet

A comprehensive summary of the essential keyboard shortcuts for managing files, splits, and terminals within LazyVim.

## 1. Window Navigation (Moving Between Splits)
Move your cursor between active splits using `Ctrl` and a directional key.
* **`Ctrl + h`** or **`Ctrl + Left Arrow`** – Move to the left split
* **`Ctrl + l`** or **`Ctrl + Right Arrow`** – Move to the right split
* **`Ctrl + k`** or **`Ctrl + Up Arrow`** – Move to the upper split
* **`Ctrl + j`** or **`Ctrl + Down Arrow`** – Move to the lower split

## 2. Split Window Management
Commands and shortcuts to create, resize, and close workspace windows.
* **`leader + |`** – Split window vertically
* **`leader + -`** – Split window horizontally
* **`leader + w + d`** or **`:q`** – Close the current split
* **`Ctrl + w` followed by `=`** – Equalize the size of all open splits
* **`Ctrl + w` followed by `r`** – Rotate/swap the positions of your splits

## 3. Opening Files in Splits
### Via Telescope (File Finder)
Press **`leader + f + f`** to open the file search, highlight your target file, and press:
* **`Ctrl + v`** – Open file in a **vertical** split
* **`Ctrl + x`** – Open file in a **horizontal** split

### Via Neo-tree (Sidebar Explorer)
Press **`leader + e`** to toggle the file tree sidebar, highlight a file, and press:
* **`v`** – Open file in a **vertical** split
* **`s`** – Open file in a **horizontal** split

### Via Command-Line Mode
Press **`:`** to enter command mode, then type:
* **`:vsp path/to/file`** – Open file in a **vertical** split
* **`:sp path/to/file`** – Open file in a **horizontal** split

## 4. Integrated Terminal Windows
### Spawning Terminals
* **`leader + f + T`** – Open a **vertical** terminal split
* **`leader + f + t`** – Open a **horizontal** terminal split
* **`leader + t`** – Toggle a **floating** terminal window

### Terminal Mode Navigation
When typing inside a terminal, Neovim locks input into Terminal Mode. 
* **`Esc`** (or **`Ctrl + \` then `Ctrl + n`**) – Exit Terminal Mode (returns to Normal Mode so you can navigate out of the split)
* **`i`** or **`a`** – Re-enter Terminal Mode to start typing shell commands again

---
*Tip: In Neovim, the **`leader`** key in LazyVim defaults to the **Spacebar**.*
