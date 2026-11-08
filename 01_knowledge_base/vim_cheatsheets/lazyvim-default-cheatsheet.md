**LazyVim Default Cheat Sheet**

**(Leader Key: Space) (Local Leader: `\`)**

---

**I. General Navigation & Editing**

| Key        | Description                  | Mode |
| :--------- | :--------------------------- | :--- |
| `j`        | Move cursor down.            | n, x |
| `<Down>`    | Move cursor down.            | n, x |
| `k`        | Move cursor up.              | n, x |
| `<Up>`      | Move cursor up.              | n, x |
| `<C-h>`     | Go to Left Window.          | n   |
| `<C-j>`     | Go to Lower Window.         | n   |
| `<C-k>`     | Go to Upper Window.         | n   |
| `<C-l>`     | Go to Right Window.         | n   |
| `<C-Up>`    | Increase window height.     | n   |
| `<C-Down>`  | Decrease window height.     | n   |
| `<C-Left>`  | Decrease window width.      | n   |
| `<C-Right>` | Increase window width.      | n   |
| `<A-j>`     | Move Down                    | n, i, v |
| `<A-k>`     | Move Up                      | n, i, v |
| `<S-h>`     | **Prev Buffer**              | n   |
| `<S-l>`     | **Next Buffer**              | n   |
| `[b`       | Previous buffer.            | n   |
| `]b`       | Next buffer.                | n   |
| `<leader>bb` | Switch to Other Buffer.     | n   |
| `<leader>\` | Switch to Other Buffer.     | n   |
| `<leader>bd` | Delete Buffer.             | n   |
| `<leader>bo` | Delete Other Buffers.      | n   |
| `<leader>bD` | Delete Buffer and Window.   | n   |
| `<esc>`     | Exit insert mode/clear search/cancel operation. | \*   |
| `<leader>ur` | Redraw / Clear hlsearch / Diff Update | n |
| `n`        | Next Search Result.         | n, x, o |
| `N`        | Previous Search Result.     | n, x, o |
| `<C-s>`     | Save File.                  | i, x, n, s |
| `<leader>K` | Keywordprg                  | n   |
| `gco`       | Add comment below.          | n   |
| `gcO`       | Add comment above.          | n   |
| `<leader>l` | Open lazy.nvim              | n   |
| `<leader>fn` | New File                    | n   |
| `<leader>xl` | Location List               | n   |
| `<leader>xq` | Quickfix List               | n   |
| `[q`       | Previous Quickfix.          | n   |
| `]q`       | Next Quickfix.              | n   |
| `<leader>cf` | Format                      | n, v |
| `<leader>cd` | Line Diagnostics            | n   |
| `]d`        | Next Diagnostic.            | n   |
| `[d`        | Previous Diagnostic.        | n   |
| `]e`        | Next Error.                 | n   |
| `[e`        | Previous Error.             | n   |
| `]w`        | Next Warning.               | n   |
| `[w`        | Previous Warning.           | n   |
| `<leader>uf` | Toggle Auto Format (Global) | n |
| `<leader>uF` | Toggle Auto Format (Buffer) | n |
| `<leader>us` | Toggle Spelling             | n |
| `<leader>uw` | Toggle Wrap                 | n |
| `<leader>uL` | Toggle Relative Number      | n |
| `<leader>ud` | Toggle Diagnostics          | n |
| `<leader>ul` | Toggle Line Numbers         | n |
| `<leader>uc` | Toggle Conceal Level        | n |
| `<leader>uA` | Toggle Tabline              | n |
| `<leader>uT` | Toggle Treesitter Highlight | n |
| `<leader>ub` | Toggle Dark Background      | n |
| `<leader>uD` | Toggle Dimming              | n |
| `<leader>ua` | Toggle Animations           | n |
| `<leader>ug` | Toggle Indent Guides        | n |
| `<leader>uS` | Toggle Smooth Scroll        | n |
| `<leader>dpp` | Toggle Profiler | n |
| `<leader>dph` | Toggle Profiler Highlights | n |
| `<leader>uh` | Toggle Inlay Hints | n |
| `<leader>gb` | Git Blame Line              | n   |
| `<leader>gB` | Git Browse (open)           | n, x |
| `<leader>gY` | Git Browse (copy)           | n, x |
| `<leader>qq` | Quit All                    | n   |
| `<leader>ui` | Inspect Pos                 | n   |
| `<leader>uI` | Inspect Tree                | n   |
| `<leader>L` | LazyVim Changelog           | n   |
| `<leader>fT` | Terminal (cwd)              | n   |
| `<leader>ft` | Terminal (Root Dir)         | n   |
| `<c-_>` / `<c-/>`| Terminal (Root Dir)       | n, t |
| `<c-/>`     | Hide Terminal              | t   |
| `<leader>-`  | Split Window Below          | n   |
| `<leader>|`  | Split Window Right         | n   |
| `<leader>wd` | Delete Window               | n   |
| `<leader>wm` / `<leader>uZ` | Toggle Zoom Mode       | n   |
| `<leader>uz` | Toggle Zen Mode             | n   |
| `<leader><tab>l` | Last Tab                  | n   |
| `<leader><tab>o` | Close Other Tabs          | n   |
| `<leader><tab>f` | First Tab                 | n   |
| `<leader><tab><tab>` | New Tab                 | n   |
| `<leader><tab>]` | Next Tab                  | n   |
| `<leader><tab>d` | Close Tab                 | n   |
| `<leader><tab>[` | Previous Tab              | n   |

---

**II. LSP (Language Server Protocol)**

| Key         | Description                    | Mode |
| :---------- | :----------------------------- | :--- |
| `<leader>cl` | Lsp Info                      | n   |
| `gd`        | Go to Definition.            | n   |
| `gr`        | References.                  | n   |
| `gI`        | Goto Implementation.         | n   |
| `gy`        | Goto T\[y]pe Definition.      | n   |
| `gD`        | Goto Declaration             | n   |
| `K`         | Hover (Show documentation)   | n   |
| `gK`        | Signature Help               | n   |
| `<c-k>`     | Signature Help (in insert mode) | i   |
| `<leader>ca` | Code Action                  | n, v |
| `<leader>cc` | Run Codelens                 | n, v |
| `<leader>cC` | Refresh & Display Codelens    | n  |
| `<leader>cR` | Rename File                  | n  |
| `<leader>cr` | Rename                       | n  |
| `<leader>cA` | Source Action                | n  |
| `<leader>co` | Organize Imports             | n  |
| `<leader>cM` | Add missing imports          | n  |
| `<leader>cu` | Remove unused imports        | n  |
| `<leader>cD` | Fix all diagnostics          | n  |
| `<leader>cV` | Select TS workspace version  | n  |

---

**III. Diagnostics (Errors/Warnings)**

| Key         | Description                    | Mode |
| :---------- | :----------------------------- | :--- |
| `[q`    | Previous Trouble/Quickfix Item.  | n   |
| `]q`    | Next Trouble/Quickfix Item.      | n   |
| `<leader>cd` | Show line diagnostics.        | n   |
| `]d`    | Next Diagnostic.                | n   |
| `[d`    | Previous Diagnostic.            | n   |
| `]e`    | Next Error.                     | n   |
| `[e`    | Previous Error.                 | n   |
| `]w`    | Next Warning.                   | n   |
| `[w`    | Previous Warning.               | n   |
| `<leader>xx` | Toggle diagnostics (Trouble).| n   |
| `<leader>xX` | Toggle buffer diagnostics (Trouble).| n   |

---

**IV. Which-Key (Keybinding Helper)**

| Key           | Description                      | Mode |
| :------------ | :------------------------------- | :--- |
| `<leader>?`   | Show all keymaps for the current buffer. | n |
| `<c-w><space>` | Window Hydra Mode (which-key)     | n |

---

**V. Bufferline**

| Key         | Description                    | Mode |
| :---------- | :----------------------------- | :--- |
| `<leader>bp` | Toggle Pin                     | n   |
| `<leader>bP` | Delete Non-Pinned Buffers.     | n   |
| `<leader>br` | Delete Buffers to the Right.   | n   |
| `<leader>bl` | Delete Buffers to the Left.    | n   |
| `[b`        | Prev Buffer                   | n   |
| `]b`        | Next Buffer                   | n   |
| `[B`         | Move buffer prev               | n |
| `]B`         | Move buffer next               | n |
| `<S-h>`     | **Prev Buffer**               | n |
| `<S-l>`     | **Next Buffer**               | n |

---

**VI. Conform (Formatting)**

| Key         | Description                        | Mode |
| :---------- | :--------------------------------- | :--- |
| `<leader>cF` | Format Injected Langs (Format selection or buffer) | n, v |

---

**VII. Telescope (Fuzzy Finder)**

| Key         | Description                    | Mode |
| :---------- | :----------------------------- | :--- |
| `<leader>/` | Live Grep (grep in the current directory).| n |
| `<leader>:` | Command History.             | n |
| `<leader><space>` | Find Files (Root Dir).    | n |
| `<leader>fp` | Projects.                    | n |
| `<leader>fb` | Buffers                      | n |
| `<leader>fB` | Buffers (all)                | n |
| `<leader>fc` | Find Config File             | n |
| `<leader>ff` | Find Files (Root Dir).        | n |
| `<leader>fF` | Find Files (cwd).            | n |
| `<leader>fg` | Find Files (git-files).      | n |
| `<leader>fr` | Recent Files.                | n |
| `<leader>fR` | Recent Files (cwd).           | n |
| `<leader>gc` | Commits                      | n |
| `<leader>gs` | Git Status                   | n |
| `<leader>s"` | Registers.                   | n |
| `<leader>s/` | Search History               | n |
| `<leader>sa` | Autocmds                     | n |
| `<leader>sb` | Buffer Lines                 | n |
| `<leader>sB` | Grep Open Buffers            | n |
| `<leader>sc` | Command History              | n |
| `<leader>sC` | Commands                     | n |
| `<leader>sd` | Diagnostics                  | n |
| `<leader>sD` | Buffer Diagnostics           | n |
| `<leader>sg` | Grep (Root Dir)             | n |
| `<leader>sG` | Grep (cwd)                   | n |
| `<leader>sh` | Help Pages                   | n |
| `<leader>sH` | Highlights                   | n |
| `<leader>si` | Icons                        | n |
| `<leader>sj` | Jumps                        | n |
| `<leader>sk` | Keymaps                      | n |
| `<leader>sl` | Location List                | n |
| `<leader>sm` | Marks                        | n |
| `<leader>sM` | Man Pages                    | n |
| `<leader>so` | Options                      | n |
| `<leader>sR` | Resume                       | n |
| `<leader>sq` | Quickfix List                | n |
| `<leader>sw` | Visual selection or word (Root Dir) | n, x |
| `<leader>sW` | Visual selection or word (cwd)  | n, x |
| `<leader>sS` | Goto Symbol (Workspace)      | n |

---

**VIII. Git Integration (Gitsigns)**

| Key         | Description                    | Mode |
| :---------- | :----------------------------- | :--- |
| `[h`        | Go to previous hunk.          | n   |
| `]h`        | Go to next hunk.              | n   |
| `[H`        | Go to the first hunk.         | n   |
| `]H`        | Go to the last hunk.          | n   |
| `<leader>ghs` | Stage Hunk.                   | n, v |
| `<leader>ghr` | Reset Hunk.                   | n, v |
| `<leader>ghS` | Stage Buffer.                  | n   |
| `<leader>ghu` | Undo Stage Hunk.              | n   |
| `<leader>ghR` | Reset Buffer.                  | n   |
| `<leader>ghp` | Preview Hunk Inline.         | n   |
| `<leader>ghb` | Blame Line.                   | n   |
| `<leader>ghB` | Blame Buffer.                 | n   |
| `<leader>ghd` | Diff This.                    | n   |
| `<leader>ghD` | Diff This (compare to the head of the branch). | n |
| `ih`        | GitSigns Select Hunk            | o, x |

---

**IX. Trouble (Diagnostics/Quickfix)**

| Key         | Description                            | Mode |
| :---------- | :------------------------------------- | :--- |
| `<leader>xt` | Todo (Trouble)                         | n  |
| `<leader>xT` | Todo/Fix/Fixme (Trouble)             | n  |
| `[q`        | Previous Trouble/Quickfix Item.         | n  |
| `]q`        | Next Trouble/Quickfix Item.             | n  |

---

**X. Mini-Surround**

| Key   | Description            | Mode |
| :---- | :--------------------- | :--- |
| `gsa` | Add Surrounding        | n, v |
| `gsd` | Delete Surrounding     | n    |
| `gzf` | Find Right Surrounding | n    |
| `gzF` | Find Left Surrounding  | n    |
| `gzh` | Highlight Surrounding  | n    |
| `gzn` | Update `MiniSurround.config.n_lines` | n |
| `gzr` | Replace Surrounding    | n    |

---

**XI. Neo-Tree (File Explorer)**

| Key         | Description                      | Mode |
| :---------- | :------------------------------- | :--- |
| `<leader>fe` | Open Neo-tree (Root Dir)       | n   |
| `<leader>fE` | Open Neo-tree (cwd)            | n   |

---

**XII. Project (project.nvim)**

| Key         | Description              | Mode |
| :---------- | :----------------------- | :--- |
| `<leader>fp` | Projects                 | n    |

---

**XIII. Notifications (Snacks.nvim)**

| Key         | Description                 | Mode |
| :---------- | :-------------------------- | :--- |
| `<leader>n` | Notification History       | n    |
| `<leader>un` | Dismiss All Notifications | n    |

---

**XIV. Code Completion (blink.cmp)**

| Key         | Description                                  | Mode |
| :---------- | :-------------------------------------------- | :--- |
| `<tab>`     | Cycle through completion suggestions/accept snippet | i, s |
| `<s-tab>`   | Cycle backwards through completion suggestions | i, s |
| `<c-y>`     | Accept completion                              | i |
| `<c-space>` | Show completion menu                          | i |

---

**XV. File/Code Navigation (Flash.nvim)**

| Key     | Description                    | Mode |
| :------ | :----------------------------- | :--- |
| `s`     | Flash (jump to any location)   | n, x, o |
| `S`     | Flash Treesitter              | n, x, o |
| `r`     | Remote Flash                   | o |
| `R`     | Treesitter Search              | o, x |

---

**XVI. Misc/Utils**

| Key         | Description                   | Mode |
| :---------- | :---------------------------- | :--- |
| `<leader>.` | Toggle scratch buffer         | n   |
| `<leader>S` | Select scratch buffer         | n   |
| `<leader>dps` | Profiler Scratch Buffer     | n   |

---

**XVII. Terminal (Snacks Terminal)**

| Key          | Description                | Mode |
| :----------- | :------------------------- | :--- |
| `<leader>fT` | Terminal (cwd)             | n   |
| `<leader>ft` | Terminal (Root Dir)        | n   |
| `<c-_>` / `<c-/>` | Terminal (Root Dir)      | n, t |
| `<c-/>`      | Hide Terminal               | t   |
| `<C-h>`      | Go to Left Window          | t   |
| `<C-j>`      | Go to Lower Window         | t   |
| `<C-k>`      | Go to Upper Window         | t   |
| `<C-l>`      | Go to Right Window         | t   |

---

**XVIII. Test (Neotest)**

| Key         | Description                                | Mode |
| :---------- | :------------------------------------------ | :--- |
| `<leader>t` | +test                                      | n    |
| `<leader>tl` | Run Last (Neotest)                          | n    |
| `<leader>to` | Show Output (Neotest)                       | n    |
| `<leader>tO` | Toggle Output Panel (Neotest)               | n    |
| `<leader>tr` | Run Nearest (Neotest)                      | n    |
| `<leader>ts` | Toggle Summary (Neotest)                   | n    |
| `<leader>tS` | Stop (Neotest)                             | n    |
| `<leader>tt` | Run File (Neotest)                          | n    |
| `<leader>tT` | Run All Test Files (Neotest)               | n    |
| `<leader>tw` | Toggle Watch (Neotest)                      | n    |
| `<leader>td` | Debug Nearest (Run test with debugger)     | n    |

---

**XIX. Chezmoi (chezmoi.nvim and chezmoi.vim)**

| Key         | Description | Mode |
| :---------- | :---------- | :--- |
| `<leader>sz` | Chezmoi     | n    |

---
