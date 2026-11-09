# Linux System Administration · Unit 1: Linux Fundamentals & Command Line Basics

## 💻 The Admin's True Workspace
Before graphical interfaces, before menus and mice, there was the command line. For a Linux system administrator, the command line is not a relic—it is the most powerful and flexible tool at your disposal. This unit is your first step into that world.

> 💡 **Catch Wisdom**  
> Your first step into the command line is understanding Linux itself, its file system, and the commands that let you control it. Everything else (user management, networking, security, scripting) builds on this foundation.

### 🎯 This Unit Will Give You 3 Things:
1. Recognize the Linux architecture and the kernel's role in managing hardware and system calls.
2. Learn to navigate the File System Hierarchy (FHS) using essential command-line tools.
3. Understand how to use `man` pages for self-guided learning and troubleshooting.

> 🛑 **Myth vs. Fact**  
> **Myth:** "There is only one command-line shell on Linux (Bash)."  
> **Fact:** False. There are many shells available (`sh`, `ksh`, `zsh`, `csh`, `fish`), though Bash is the most common default.

---

## 🧠 What is Linux? Architecture and the Kernel
Linux is a Unix-like operating system built around a **kernel**. The kernel is the core component that manages hardware resources, system calls, and process scheduling. 

When you run a program, the kernel allocates memory, schedules CPU time, and handles input/output requests. Without the kernel, the hardware would be just a collection of inert components.

### 🔑 Kernel Versions Matter
Kernel version numbering follows a pattern: `major.minor.patch`. 
- **Major releases**: Introduce new features or change system behavior.
- **Minor/Patch releases**: Typically bring bug fixes and security updates.

> 💡 **Pro Tip**  
> Always check your current kernel version with:  
> `uname -r`  
> *(Bonus: Live patching technology allows critical security fixes to be applied to the running kernel with zero downtime, keeping systems secure without interrupting services!)*

---

## 🐧 Choosing Your Distribution
Linux is a family of distributions. The three major families used in enterprise and server environments are **Red Hat**, **Debian**, and **SUSE**. 

| Distribution Family | Package Format | Package Manager | Common Use Case |
| :--- | :--- | :--- | :--- |
| **Red Hat** (RHEL, CentOS, Rocky, Alma) | `.rpm` | `yum` / `dnf` | Corporate data centers, enterprise servers |
| **Debian** (Debian, Ubuntu, Mint) | `.deb` | `apt` / `apt-get` | Servers, desktops, cloud environments (like your WSL!) |
| **SUSE** (SLES, openSUSE) | `.rpm` | `zypper` | European enterprise, specific SAP environments |

> 💡 **Pro Tip**  
> To quickly identify which Linux distribution you are on, run:  
> `cat /etc/os-release`

---

## 📂 The File System Hierarchy (FHS)
The FHS standardizes directory locations across all Linux distributions. Knowing where things live is half the battle.

- `/` : The root of the entire file system.
- `/bin` & `/usr/bin` : Essential user command binaries.
- `/etc` : System-wide configuration files. *(Your home away from home for tweaking things).*
- `/home` : User home directories (e.g., `/home/rehanna`).
- `/var` : Variable data, like log files (`/var/log`) and spools.
- `/tmp` : Temporary files (cleared on reboot).
- `/root` : The home directory for the root user (not `/home/root`).
- `/dev` : Device files (hardware interfaces).
- `/proc` : Virtual filesystem providing process and kernel information.

---

## 🐚 Shell Basics: Your Command Interpreter
The shell is the command-line interpreter. Bash (Bourne Again SHell) is the default on most systems (including your WSL Ubuntu). 

Mastering these shell mechanics is **non-negotiable** for a SysAdmin:

| Concept | Syntax / Example | Purpose |
| :--- | :--- | :--- |
| **Output Redirect** | `command > file.txt` | Overwrites file with command output. |
| **Append Redirect** | `command >> file.txt` | Adds command output to the end of the file. |
| **Input Redirect** | `command < file.txt` | Feeds file contents as input to the command. |
| **Pipe** | `command1 \| command2` | Sends output of `command1` as input to `command2`. |
| **Wildcards (Globbing)** | `*.conf`, `?.txt` | `*` matches any chars, `?` matches single char. |
| **Command Substitution**| `$(command)` or `` `command` `` | Embeds the output of one command into another. |

---

## 🛠️ Essential Command-Line Tools

### 1. Search for Files: `find`
Searches the file system for files matching criteria (name, size, time).
```bash
# Find all .log files in /var
find /var -name "*.log"

# Find all .conf files in /etc, suppressing "Permission denied" errors
find /etc -name "*.conf" 2>/dev/null
```

### 2. Search Within Files: `grep`
Searches file contents for specific patterns or strings.
```bash
# Search for 'error' in syslog
grep 'error' /var/log/syslog

# Recursive search with extended regex
grep -r "error" /var/log/
```

### 3. View File Beginnings and Endings: `head` & `tail`
Crucial for reading logs without opening massive files in an editor.
```bash
# View the first 20 lines of a file
head -20 /var/log/syslog

# Monitor a log file in real-time as new lines are added
tail -f /var/log/syslog
```

### 4. Extract and Combine: `cut` & `paste`
```bash
# Extract the 1st field (username) from /etc/passwd, using ':' as delimiter
cut -d ':' -f1 /etc/passwd
```

> 🎯 **Practice Scenario: Daily Logging Script**  
> A junior admin needs to record system uptime daily.  
> 1. `date > /var/log/uptime.log` *(Writes current date, overwriting if it exists)*  
> 2. `uptime >> /var/log/uptime.log` *(Appends uptime info without erasing the date)*

---

## 📚 Online Documentation: The Man Pages
Every command has a built-in manual. This is your first stop for troubleshooting, fostering independence from Google.

```bash
# Open the manual for the 'tar' command
man tar

# Open the manual for a specific section (e.g., Section 5 for file formats like crontab)
man 5 crontab
```
**Common Man Page Sections:**
- **Section 1**: User commands (e.g., `ls`, `cd`)
- **Section 5**: File formats and conventions (e.g., `passwd`, `crontab`)
- **Section 8**: System administration commands (e.g., `useradd`, `fdisk`)

*(Pro tip: Press `q` to quit the man page, and `/` followed by a word to search within it).*

---

## ⚡ Command Quick Reference

| Command | Primary Use |
| :--- | :--- |
| `find` | Search for files by name, size, or time |
| `grep` | Search for text patterns within file contents |
| `head` / `tail` | View the beginning or end of a file (`tail -f` for live monitoring) |
| `cut` | Extract specific columns/fields from text |
| `paste` | Combine lines from multiple files side-by-side |
| `man` | Access built-in system documentation |
| `tar` / `gzip` | Archive and compress files |
| `vi` / `vim` / `nvim` | Terminal-based text editor *(Your LazyVim setup lives here!)* |

---

## 📌 Key Takeaways
- Linux is built around a **kernel** that manages hardware, system calls, and process scheduling.
- The three major distro families are **Red Hat** (`dnf`/`yum`), **Debian** (`apt`), and **SUSE** (`zypper`).
- The **File System Hierarchy (FHS)** standardizes directories (`/etc` for configs, `/var` for logs, `/home` for users).
- The **Bash shell** provides I/O redirection, pipes, wildcards, and command substitution—essential for chaining commands.
- **Man pages** (`man`) are your built-in, offline documentation system. Learn to read them.

***

How’s that look, Rehanna? 🛡️ 

Since you're already using WSL Ubuntu and LazyVim, you're living in this environment every day. If you want to build that muscle memory right now, try opening your terminal and typing `cat /etc/os-release` followed by `man cut`. 

Let me know if you want to break down any of these commands step-by-step, or if you're ready to tackle the next concept! You're building a rock-solid foundation. ☬
