# 📋 Linux+ Week 4: Automation, Orchestration, & Scripting

## 🎯 Domain Overview

This week focuses on automating repetitive tasks, parsing data efficiently, managing code versions, and understanding how systems talk to each other.

---

## ✅ 1. Shell Scripting Essentials

_The foundation of Linux automation._

- **Shebang:** Always start scripts with `#!/bin/bash`
- **Variables:** `MY_VAR="hello"` (access with `$MY_VAR`)
- **Conditionals:**
  ```bash
  if [ "$USER" == "root" ]; then
      echo "You are root"
  else
      echo "You are not root"
  fi
  ```
- **Loops:**
  - `for i in {1..5}; do echo $i; done`
  - `while [ condition ]; do ... done`
- **Exit Codes:** `$?` holds the exit status of the last command (`0` = success, `1-255` = error). Use `exit 0` or `exit 1` in scripts.
- **Pipelines:** `|` passes the output (stdout) of one command as the input (stdin) to the next.

---

## ✅ 2. Text Processing Tools (The Log-Parsing Trinity)

_Essential for filtering, editing, and analyzing log files and data._

**`grep` (Find text)**

- `grep "text" file.log` → Find exact match (case-sensitive).
- `grep -i "text" file.log` → Ignore case.
- `grep -c "text" file.log` → Count matching lines.
- `grep -v "text" file.log` → Invert match (show everything _except_ this).
- `grep -n "text" file.log` → Show line numbers.
- `grep -C 1 "text" file.log` → Show 1 line of context (Before & After). `-B` (Before) and `-A` (After) also work.

**`sed` (Stream Editor / Find & Replace)**

- `sed 's/old/new/g' file.log` → Substitute (dry run, prints to screen).
- `sed -i 's/old/new/g' file.log` → Substitute **in-place** (saves to file).
- `sed '/pattern/d' file.log` → Delete entire lines matching pattern.
- `sed -n '2,4p' file.log` → Print _only_ lines 2 through 4.
- `sed '2s/old/new/' file.log` → Substitute _only_ on line 2.

**`awk` (Column Extraction)**

- `awk '{print $3, $4}' file.log` → Print specific columns (space-delimited by default).
- `awk '$5 == "sshd:"' file.log` → Filter rows where column 5 exactly matches "sshd:".

**`sort` & `uniq` (The Golden Combo)**

- _Rule:_ Always `sort` before `uniq`, because `uniq` only removes _adjacent_ duplicates.
- `sort file.txt | uniq` → Sort and remove duplicates.
- `sort file.txt | uniq -c` → Sort, remove duplicates, and **count** occurrences.

---

## ⏳ 3. Task Automation (Upcoming)

_Scheduling tasks to run automatically._

- **`cron`**: The classic scheduler. Edited via `crontab -e`.
  - Format: `* * * * * /path/to/script.sh` (Minute, Hour, Day of Month, Month, Day of Week)
  - Example: `0 2 * * * /home/rlpor/backup.sh` (Runs daily at 2:00 AM)
- **`systemd` timers**: The modern, more robust alternative to cron. Uses `.timer` and `.service` files.
- **Logging & Error Handling**:
  - Redirect output: `./script.sh >> /var/log/myscript.log 2>&1` (Appends both standard output and standard error to a log file).

---

## ⏳ 4. Version Control: Git Fundamentals (Upcoming)

_Tracking changes and collaborating on code._

- `git clone <url>` → Copy a remote repo locally.
- `git status` → Check current state of working directory.
- `git add <file>` → Stage changes.
- `git commit -m "message"` → Save staged changes to local history.
- `git branch <name>` → Create a new branch.
- `git checkout -b <name>` → Create and switch to a new branch.
- `git merge <branch>` → Merge a branch into your current branch.
- `git revert <commit-hash>` → Safely undo a commit by creating a new "undo" commit.
- **`.gitignore`**: A file listing patterns of files/directories Git should ignore (e.g., `*.log`, `.env`, `__pycache__/`).

---

## ⏳ 5. API Awareness & Basic IaC (Upcoming)

_How systems talk to each other and the future of infrastructure._

- **`curl`**: Command-line tool for transferring data with URLs.
  - Example: `curl -s https://api.github.com`
- **`jq`**: Command-line JSON processor. Used to parse and format the output of APIs.
  - Example: `curl -s https://api.example.com/data | jq '.name'`
- **IaC (Infrastructure as Code) Principles**: Managing and provisioning computing infrastructure through machine-readable definition files (e.g., Terraform, Ansible), rather than physical hardware configuration or interactive configuration tools.

---

## ⏳ 6. Career & Portfolio Check

- [ ] Review current resume: Add new skills (Bash/Python automation, Git workflow, log parsing).
- [ ] Ensure `~/git_repos/devsecops/` is clean and ready for portfolio projects.
- [ ] Move all messy lab files to `02_labs_and_playground/`.

---

### How to save this:

```text
cd ~/git_repos/devsecops/01_knowledge_base/
nano Week4_Automation_Scripting.md
```

_(Paste it in, `Ctrl+O` to save, `Enter` to confirm, `Ctrl+X` to exit)._

How does this full version look? It gives you the complete map for the week.

Whenever you're ready, we can either:

1. Dive into **Task Automation (`cron`)** to check off the next box.
2. Jump into **Git fundamentals**.
3. Take a breather. (Seriously, protect your peace today).

Your call, Rehanna.
