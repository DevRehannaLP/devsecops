# LazyVim / Neovim Cheat Sheet

## Files / Explorer

| Action | Shortcut / Command |
|---|---|
| Open file by name | `<leader><space>` |
| Find files | `<leader>ff` |
| Recent files | `<leader>fr` |
| Search text in project | `<leader>fg` |
| Open explorer | `<leader>e` |
| Open explorer at current folder | `:Neotree .` |
| Open specific file | `:e main.go` |
| Open file in vertical split | `:vs main.go` / `:vsplit main.go` |
| From explorer open vertical split | `s` |
| Create folder in explorer | `a` then type `folder-name/` |

---

## Buffers / Tabs / Splits

LazyVim "tabs" are usually **buffers**.

| Action | Shortcut |
|---|---|
| Previous buffer | `Shift+h` |
| Next buffer | `Shift+l` |
| Switch buffer picker | `<leader>bb` |
| Close buffer | `<leader>bd` |
| Last file / previous buffer | `Ctrl+^` |

Real Vim tabs:

| Action | Shortcut |
|---|---|
| Next tab | `gt` |
| Previous tab | `gT` |
| New tab | `:tabnew` |
| Close tab | `:tabclose` |

Splits:

| Action | Shortcut / Command |
|---|---|
| Vertical split | `:vsplit` / `:vs` |
| Horizontal split | `:split` / `:sp` |
| Move left split | `Ctrl+h` |
| Move down split | `Ctrl+j` |
| Move up split | `Ctrl+k` |
| Move right split | `Ctrl+l` |
| Close split | `:q` |

---

## Navigation

| Action | Shortcut |
|---|---|
| Go to line 25 | `:25` or `25G` |
| First line | `gg` |
| Last line | `G` |
| Jump back | `Ctrl+o` |
| Jump forward | `Ctrl+i` |
| Previous cursor line | `''` |
| Previous exact cursor position | `` ` `` |
| Last edited location | `` `. `` |
| Last cursor position when file closed | `` `" `` |
| Go to definition | `gd` |
| Next function | `]m` |
| Previous function | `[m` |
| Search current file symbols/functions | `<leader>ss` |
| Next diagnostic/error | `]d` |
| Previous diagnostic/error | `[d` |
| Open diagnostic under cursor | `<leader>cd` |
| Show all diagnostics/Trouble | `<leader>xx` |

---

## Marks

| Action | Command |
|---|---|
| Set mark `a` | `ma` |
| Jump to mark line | `'a` |
| Jump to exact mark position | `` `a `` |
| List marks | `:marks` |
| Delete mark `a` | `:delmarks a` |
| Delete marks `a`, `b`, `c` | `:delmarks abc` |
| Delete all lowercase marks | `:delmarks!` |

Rule:

```text
' = jump to line
` = jump to exact position
```

---

## Editing Basics

| Action | Shortcut |
|---|---|
| Insert before cursor | `i` |
| Insert after cursor | `a` |
| Insert at start of line | `I` |
| Insert at end of line | `A` |
| Toggle case of current char | `~` |
| Uppercase current char | `gUl` |
| Uppercase word | `gUw` |
| Lowercase word | `guw` |

Example: add one char before cursor:

```vim
iX<Esc>
```

---

## Search Match Editing

After searching with `/foo`:

| Action | Shortcut |
|---|---|
| Delete current/next search match | `dgn` |
| Change current/next search match | `cgn` |
| Yank current/next search match | `ygn` |
| Repeat last change/delete | `.` |

Delete all matches:

```vim
:%s/foo//g
```

---

## Text Objects

Quotes example:

| Action | Shortcut |
|---|---|
| Change inside quotes | `ci"` |
| Change around quotes, including quotes | `ca"` |
| Delete inside quotes | `di"` |
| Delete around quotes | `da"` |
| Yank inside quotes | `yi"` |
| Yank around quotes | `ya"` |

Example:

```text
"hello"
```

`ci"` changes only `hello`.

`ca"` changes `"hello"`, including the quotes.

---

## mini-surround

Used for adding/removing/replacing surrounding chars like `"`, `'`, `{}`, `[]`, `()`.

| Action | Shortcut |
|---|---|
| Add surround | `gsa` |
| Delete surround | `gsd` |
| Replace surround | `gsr` |
| Find right surround | `gsf` |
| Find left surround | `gsF` |
| Highlight surround | `gsh` |

Examples:

| Goal | Shortcut |
|---|---|
| Add quotes around word | `gsaiw"` |
| Delete quotes | `gsd"` |
| Delete backticks | `` gsd` `` |
| Replace `"` with `'` | `gsr"'` |
| Replace `{}` with `[]` | `gsr{[` |
| Replace `()` with `[]` | `gsr([` |

Enable if missing:

```vim
:LazyExtras
```

Enable:

```text
coding.mini-surround
```

Then:

```vim
:Lazy sync
```

---

## Rename / LSP

| Action | Shortcut |
|---|---|
| Rename variable/function | `<leader>cr` |
| Manual LSP rename | `:lua vim.lsp.buf.rename()` |
| LSP info/check attached server | `:LspInfo` |

For Go completion, make sure LazyVim Go extra is enabled:

```vim
:LazyExtras
```

Enable:

```text
lang.go
```

Then check/install:

```vim
:Mason
```

Needed:

```text
gopls
goimports
gofumpt
delve
```

---

## Comments

| Action | Shortcut |
|---|---|
| Comment current line | `gcc` |
| Comment selected lines | Visual select, then `gc` |
| Comment paragraph | `gcip` |

---

## File Refresh

| Action | Command |
|---|---|
| Refresh current file from disk | `:e` |
| Refresh and discard unsaved changes | `:e!` |
| Check all buffers for outside changes | `:checktime` |
| Enable auto-read | `:set autoread` |

Good combo:

```vim
:set autoread
:checktime
```

---

## Terminal

LazyVim terminal:

| Action | Shortcut |
|---|---|
| Open terminal | `<leader>ft` |
| Open floating terminal | `<leader>fT` |
| Open Vim terminal | `:terminal` |
| Exit terminal insert mode | `Ctrl+\ Ctrl+n` |
| Close terminal | `exit` |

Tmux terminal management:

| Action | Shortcut |
|---|---|
| New tmux window | `Ctrl+b c` |
| Next window | `Ctrl+b n` |
| Previous window | `Ctrl+b p` |
| Vertical pane | `Ctrl+b %` |
| Horizontal pane | `Ctrl+b "` |
| Toggle pane zoom | `Ctrl+b z` |
| Resize pane | `Ctrl+b` then arrow |

Nice tmux resize config:

```tmux
bind -r H resize-pane -L 5
bind -r J resize-pane -D 5
bind -r K resize-pane -U 5
bind -r L resize-pane -R 5
```

Reload:

```bash
tmux source-file ~/.tmux.conf
```

---

## Reset Neovim / LazyVim

Full reset:

```bash
rm -rf ~/.config/nvim
rm -rf ~/.local/share/nvim
rm -rf ~/.local/state/nvim
rm -rf ~/.cache/nvim
```

Safer backup:

```bash
mv ~/.config/nvim ~/.config/nvim.bak
mv ~/.local/share/nvim ~/.local/share/nvim.bak
mv ~/.local/state/nvim ~/.local/state/nvim.bak
mv ~/.cache/nvim ~/.cache/nvim.bak
```

Only reset plugins/cache but keep config:

```bash
rm -rf ~/.local/share/nvim ~/.local/state/nvim ~/.cache/nvim
```
