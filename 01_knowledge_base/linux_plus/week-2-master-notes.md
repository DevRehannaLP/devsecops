# Week 2 Master Notes: Services & User Management (Linux+ XK0-006)

Domain 2.0 Services and User Management (20%), plus the permissions and access-control parts of Domain 3.0 Security that I study alongside it.

**What this file is:** my original Week 2 notes (April 27, 2026) merged with the notes from the users, groups, `chage`, and permissions labs, then checked against the official XK0-006 objectives (document version 5.0). Anything marked **(added)** was missing and comes from the objectives.

---

## Objective Coverage Map

| Objective | Topic                                                                 | Section |
| --------- | --------------------------------------------------------------------- | ------- |
| 2.2       | Local account management                                              | 1 to 6  |
| 3.3       | Hardening: privilege escalation (sudo/su)                             | 7       |
| 3.3       | Hardening: permissions, special bits, umask, file attributes          | 8       |
| 3.3       | Hardening: ACLs                                                       | 9       |
| 2.5       | systemd units, targets, timers, utilities                             | 10      |
| 3.1       | Logging (`journalctl`)                                                | 11      |
| 1.4       | Network configuration basics (full tool list is in Week 1, section 4) | 12      |
| 2.1       | Files and directories (covered in Week 1, section 8)                  | n/a     |

**Later weeks:** SELinux, SSH, firewalls, and account hardening are Week 3. Processes and jobs (2.3) and packages (2.4) are in the Week 1 notes.

---

## 1. The Big Idea: Account Files

Linux has no hidden user database. Every account and group is a line in a plain text file in `/etc`. The commands (`useradd`, `usermod`, `passwd`, `groupadd`, `userdel`) are tools that edit those files for me.

| File          | What it holds                                  |
| ------------- | ---------------------------------------------- |
| `/etc/passwd` | The list of accounts, one per line             |
| `/etc/group`  | The list of groups and their secondary members |
| `/etc/shadow` | Password hashes and password aging rules       |

- When a command changes one of these, Linux saves the previous version as `passwd-`, `group-`, `shadow-`. A file in `/etc` ending in `-` is the "one version ago" backup.
- `passwd` is a **file**, not a folder. `cd` is for folders. Read files with `cat`, `head`, `tail`, `less`, or `grep`.
- "Permission denied" reading a file in `/etc`? Almost always forgot `sudo`.

---

## 2. The Three Files in Detail

### /etc/passwd: 7 fields

Format: `username:x:uid:gid:info:home:shell`

Mine: `rlpor_6zv:x:1000:1000::/home/rlpor_6zv:/bin/bash`

| #   | Field                                                        | Example           |
| --- | ------------------------------------------------------------ | ----------------- |
| 1   | Username                                                     | `rlpor_6zv`       |
| 2   | Password placeholder (`x` = hash is in `/etc/shadow`)        | `x`               |
| 3   | User ID (UID)                                                | `1000`            |
| 4   | Primary group ID (GID)                                       | `1000`            |
| 5   | Comment / GECOS (often a full name, can be blank like `,,,`) | (blank)           |
| 6   | Home directory                                               | `/home/rlpor_6zv` |
| 7   | Login shell                                                  | `/bin/bash`       |

- System accounts use `/usr/sbin/nologin` as their shell: they exist but can't log in.
- `/etc/passwd` is world-readable because programs constantly look up usernames and IDs. That is why hashes were moved out of it into `/etc/shadow`.
- `head -3` and `tail -3` only show the ends of the file. Accounts in the middle won't appear.
- List only real accounts:

```bash
awk -F: '$3 >= 1000 {print $1, $3}' /etc/passwd
```

`-F:` splits on colons and `$3` is the third field. My output: `nobody 65534` and `rlpor_6zv 1000`.

### /etc/group: 4 fields

Format: `groupname:x:gid:members` Example: `sudo:x:27:rlpor_6zv`

| #   | Field                                    |
| --- | ---------------------------------------- |
| 1   | Group name                               |
| 2   | Password placeholder (almost always `x`) |
| 3   | Group ID (GID)                           |
| 4   | Member list (comma-separated)            |

**Primary vs secondary groups**

- **Primary group:** recorded in field 4 of `/etc/passwd`. It is the group assigned to files I create.
- **Secondary groups:** extra memberships listed in the last field of `/etc/group`. They grant extra access.
- On Ubuntu, each new user gets a **user private group** with the same name as the account (mine: `rlpor_6zv`, GID 1000).
- A private group's member list is **empty**, because the primary group is tracked in `/etc/passwd`. The member list only tracks **secondary** memberships.
- My secondary groups: `adm` (read logs in `/var/log`), `cdrom`, `sudo` (GID 27, lets me run `sudo`), `dip`, `plugdev`, `users`.

Look up a group by ID (colons on both sides match only the ID field): `grep :1000: /etc/group`

### /etc/shadow: hashes and aging

Readable by root only:

```
-rw-r--r-- 1 root root     /etc/passwd    (everyone can read)
-rw-r----- 1 root shadow   /etc/shadow    (owner rw, group r, others nothing)
```

Format: `username:hash:lastchange:min:max:warn:inactive:expire:reserved`

| #   | Field                                                             |
| --- | ----------------------------------------------------------------- |
| 1   | Username                                                          |
| 2   | Password hash (`!` = locked or no password set)                   |
| 3   | Day of last password change (days since Jan 1, 1970)              |
| 4   | Minimum days before it can change again                           |
| 5   | Maximum days before it must change (`99999` is effectively never) |
| 6   | Warning days before expiry                                        |
| 7   | Inactive days after expiry                                        |
| 8   | Account expiration date                                           |
| 9   | Reserved                                                          |

Hash prefixes: `$y$` is yescrypt (Ubuntu's modern default, strong), `$6$` is SHA-512 (older systems, shows up on the exam). Never paste a real account's hash anywhere.

---

## 3. Account Types and IDs (added)

| Account type            | UID range            | Notes                                                                                                           |
| ----------------------- | -------------------- | --------------------------------------------------------------------------------------------------------------- |
| root                    | `0`                  | Always root, never changes                                                                                      |
| System accounts         | under 1000           | Run background services (`daemon`, `bin`, `tcpdump`)                                                            |
| Service accounts        | usually system range | One per service (`www-data`, `mysql`), normally with a `nologin` shell, so a hacked service gets limited access |
| Regular (user) accounts | `1000` and up        | Real people. The first one is usually 1000                                                                      |
| `nobody`                | `65534`              | Almost no access, parked at a high number on purpose                                                            |

Identity attributes:

- **UID / GID:** the account's user ID and primary group ID.
- **EUID / EGID:** the _effective_ IDs, which are what permission checks actually use. Normally the same as UID/GID. Running a setuid program changes the EUID to the file owner's. See them with `ps -o pid,euid,ruid,comm`.

Defaults for new accounts come from `/etc/login.defs` (UID ranges, password aging, umask) and `/etc/default/useradd` (shell, home base). `useradd -D` shows them.

---

## 4. Managing Accounts

### Creating users

```bash
sudo useradd -m -s /bin/bash username
sudo passwd username
```

- `useradd` with no options gives **bare defaults**: shell `/bin/sh`, **no home folder**, **no password** (locked with `!`).
- `-m` creates the home directory (copying the template files from `/etc/skel`). Without it, the path is written in `/etc/passwd` but nothing is built.
- `-s` sets the login shell. `passwd` prompts twice and shows nothing as you type. It fills in the hash in `/etc/shadow`.
- `adduser username` (Debian/Ubuntu, added): a friendlier wrapper that is interactive, creates the home, and asks for the password. On RHEL, `adduser` is just `useradd`.
- **`/etc/skel`** (added): template folder copied into every new home (`.bashrc`, `.profile`). **`/etc/profile`** (added): system-wide settings run for login shells.

### Modifying users

```bash
sudo usermod -aG groupname username     # add to a secondary group
sudo usermod -s /bin/bash username      # change shell
sudo usermod -d /new/home -m username   # change home and move the files (added)
sudo usermod -g groupname username      # change primary group (added)
sudo groupmod -n newname oldname        # rename a group
sudo chsh -s /bin/zsh username          # change shell (added)
sudo passwd username                    # set or change a password
```

**The exam trap: `-a` with `-G`**

- `usermod -aG group user` **appends** and keeps the others.
- `usermod -G group user` **replaces** the entire secondary group list.
- Tested on `testuser`: `-G qa` alone wiped `devteam`. Fixed with `-aG devteam`.
- On my own account, forgetting `-a` would strip me out of `sudo`.

**Always type `-aG` together.**

### Locking and unlocking (added)

```bash
sudo usermod -L username     # lock: puts ! in front of the hash
sudo usermod -U username     # unlock
sudo passwd -l username      # same as -L
sudo passwd -u username      # same as -U
sudo passwd -S username      # status: L locked, P has password, NP no password
sudo chage -E 0 username     # expire the whole account immediately
```

Gotcha: locking the password does **not** block SSH key logins. To fully shut someone out, also expire the account (`chage -E 0`) or give them a `nologin` shell (`usermod -s /usr/sbin/nologin`).

### Password aging: chage

```bash
sudo chage -l username          # list settings (read-only)
sudo chage -M 90 -W 14 user     # max 90 days, warn 14 days before
sudo chage -d 0 user            # force a password change at next login
```

| Option | Meaning                                                            |
| ------ | ------------------------------------------------------------------ |
| `-l`   | List the settings                                                  |
| `-M`   | Max days a **password** lasts                                      |
| `-m`   | Min days between changes                                           |
| `-W`   | Warning days before expiry                                         |
| `-I`   | Inactive days after expiry before the **account** locks            |
| `-E`   | Date the whole **account** expires                                 |
| `-d 0` | Sets last change to Jan 1, 1970, so the password counts as expired |

- "Password expires" = last password change + max days. Today + 90 days gave Jan 25, 2027 in the lab.
- `-M` expires the password (user can set a new one). `-E` expires the account (user is locked out).
- `sudo passwd -e user` also forces a change at next login.
- Ubuntu defaults: min `0`, max `99999` (shows as "never"), warn `7`.
- `chage -l` is a readable view of fields 3 to 8 of the `shadow` line.

### Groups

```bash
sudo groupadd devteam
sudo groupmod -n newname oldname
sudo groupdel devteam
```

### Deleting users

```bash
sudo userdel username        # delete user, home directory stays
sudo userdel -r username     # delete user AND home directory
```

- `-r` is the mirror of `-m`. Without it, the home directory is left behind as an orphan.
- `userdel` **refuses** to delete a user who still has running processes.
- `mail spool not found` is a harmless warning.
- Debian/Ubuntu also have `deluser --remove-home username` (added).

### Listing and checking (added where marked)

```bash
whoami                      # current username
id                          # my UID, primary group, all groups
id username                 # another user's info
groups username             # a user's groups
getent passwd username      # look up an account (also works for LDAP users) (added)
last                        # login history, from /var/log/wtmp (added)
lastlog                     # last login per user (added)
w                           # who is logged in and what they are doing (added)
who                         # who is logged in (added)
su - username               # log in as that user (full login shell)
sudo -u username cmd        # run one command as that user, no shell left behind
```

`su -` (with the dash) gives a full login: that user's shell, environment, and home folder. Without the dash I become them but stay in my own directory.

---

## 5. Key Concepts to Remember

- `uid=0` is always root.
- Being in the `sudo` group means I can run sudo commands.
- `-aG` always go together in `usermod`.
- Primary group lives in `/etc/passwd`, secondary members live in `/etc/group`.
- Locked password (`!`) is not the same as an expired account.

---

## 6. Troubleshooting: "user is currently used by process"

Error: `userdel: user testuser is currently used by process 4432`

1. See what is running as that user: `ps -u testuser`
2. The `bash` entry on `pts/0` is the shell. `systemd` and `(sd-pam)` are helpers that end on their own.
3. Polite stop (did nothing here, bash ignores it): `sudo pkill -u testuser`
4. Forceful stop (signal 9, cannot be ignored): `sudo pkill -9 -u testuser`
5. Confirm with `ps -u testuser`, then rerun `userdel -r`.

Lesson: when a delete is refused, the answer is in `ps`.

---

## 7. Privilege Escalation: sudo and su (added)

- `sudo command` runs a command as root (or another user with `-u`). `sudo -i` opens a root login shell. `sudo -l` lists what I'm allowed to run.
- `su -` switches to another user with their full environment. It needs _that user's_ password (root is often locked on Ubuntu, which is why `sudo` is used instead).
- **Who gets sudo:** members of the `sudo` group on Debian/Ubuntu, or the `wheel` group on RHEL. Add with `usermod -aG sudo user`.
- **The rules live in `/etc/sudoers`** and drop-in files in `/etc/sudoers.d/`. **Always edit with `visudo`** (it checks the syntax so a typo can't lock me out of sudo). For a drop-in: `sudo visudo -f /etc/sudoers.d/name`.
- Drop-in files with a `.` in the name or ending in `~` are ignored.

Example lines:

```
rlpor_6zv ALL=(ALL:ALL) ALL            # user can run anything
%sudo     ALL=(ALL:ALL) ALL            # % means a group
deploy    ALL=(ALL) NOPASSWD: ALL      # no password prompt
helper    ALL=(ALL) NOEXEC: /usr/bin/less
```

- **`NOPASSWD`:** no password needed. Convenient for automation, but anyone who gets into that session has root with no further check.
- **`NOEXEC`:** the allowed program can't launch other programs, which blocks "shell escapes" from things like `less` or `vi`.

---

## 8. File Permissions

### Reading permissions

`ls -l` shows a string like `-rwxr-xr-x 1 owner group size date name`.

- 1st character is the type: `-` file, `d` directory, `l` symlink
- Then three chunks: **owner**, **group**, **others**
- Letters: `r` read, `w` write, `x` execute. A dash means not allowed.

Numeric values: `r` = 4, `w` = 2, `x` = 1. Add them per chunk: `rwx` = 7, `rw-` = 6, `r-x` = 5, `r--` = 4, `---` = 0.

| Mode  | String      | Typical use                               |
| ----- | ----------- | ----------------------------------------- |
| `777` | `rwxrwxrwx` | Everyone full access, dangerous           |
| `755` | `rwxr-xr-x` | Folder or script                          |
| `644` | `rw-r--r--` | Normal file                               |
| `640` | `rw-r-----` | Locked-down file (like `/etc/shadow`)     |
| `600` | `rw-------` | Private file (SSH private keys need this) |
| `700` | `rwx------` | Private folder                            |

Use `ls -ld folder` to see a **folder's own** permissions instead of its contents.

### Ownership: chown and chgrp

- The **owner** of a new file is whoever created it.
- The **group** of a new file is the creator's **primary group**, not just any group they belong to.
- Created with `sudo`, the file is owned by `root:root`.

```bash
sudo chown user file          # owner only
sudo chgrp group file         # group only
sudo chown user:group file    # both (colon between)
sudo chown :group file        # group only, same as chgrp
sudo chown -R user dir/       # recursive (added)
```

Lab: a root-owned `rw-r--r--` file could be read but not written by me ("other"), so `echo hello > file` gave `Permission denied`. After `chown`, the same command worked.

### chmod

Symbolic form: **who** (`u` owner, `g` group, `o` others, `a` all) + **action** (`+` add, `-` remove, `=` set exactly) + **what** (`r`, `w`, `x`).

```bash
chmod u+x script.sh    # owner gains execute
chmod o-r file         # others lose read
chmod a+x file         # everyone gains execute
chmod 644 file         # numeric form
chmod -R 755 dir/      # recursive (added)
```

### Directory permissions

| Bit | On a directory                                    |
| --- | ------------------------------------------------- |
| `r` | List the names inside                             |
| `w` | Create, delete, or rename entries (needs `x` too) |
| `x` | Enter it and reach the files inside               |

- With `chmod 600` on a folder (no `x`), `ls -l` showed `-?????????` for the file inside. Linux could read the **name** but not look up its details, and `cd` gave `Permission denied`.
- **Owning a directory does not let me enter it. Only `x` does.**
- Deleting a file is a **write on the folder**, not on the file.

### umask

The umask lists permissions to **take away** from the starting point. New files start at `666` (never `x` automatically) and new directories at `777`.

| umask | Files | Directories |
| ----- | ----- | ----------- |
| `022` | `644` | `755`       |
| `077` | `600` | `700`       |

- Each digit says what to remove for owner, group, others. `022` removes write from group and others.
- `umask 700` does **not** give 700. It removes everything from the **owner** and nothing from the rest, the opposite of private.
- The leading `0` in `0022` is the slot for the special bits.
- `umask 077` lasts only for the current terminal. To make it permanent, put it in `~/.bashrc` (or set `UMASK` in `/etc/login.defs`).
- The subtraction is a shortcut for a bitwise operation, but it works for normal masks.

### Special bits: SUID, SGID, sticky

A fourth digit in front of the normal three: `1` sticky, `2` setgid, `4` setuid. They add up like the others.

| Bit    | Number | Shows as          | Works on              | What it does                                                       |
| ------ | ------ | ----------------- | --------------------- | ------------------------------------------------------------------ |
| Sticky | 1      | `t` (others slot) | Directory             | Only a file's owner (or the folder's owner, or root) can delete it |
| Setgid | 2      | `s` (group slot)  | Directory (and files) | New files inherit the folder's group                               |
| Setuid | 4      | `s` (owner slot)  | Programs              | Runs as the file's owner                                           |

```bash
chmod 4755 file    # or: chmod u+s file      (setuid)
chmod 2755 dir     # or: chmod g+s dir       (setgid)
chmod 1777 dir     # or: chmod +t dir        (sticky)
```

**Sticky bit**

- `/tmp` is `1777`, shown as `rwxrwxrwt`: everyone can write, but you can only delete your own files.
- Lab: user `sticky2` could write to a `777` sticky folder but could not delete my file. Only the `t` stopped it.
- `rm` first asked "remove write-protected file?" because the file was `644` and sticky2 had no write on it. That prompt is `rm` being polite and is separate from the sticky bit. Expected refusal after it: `Operation not permitted`.

**Setuid**

- `/usr/bin/passwd` is `rwsr-xr-x` (`4755`), owned by root. That is how a normal user can change their own password even though it means editing the root-only `/etc/shadow`.
- A plain program like `/bin/ls` has a normal `x` and runs as me. `ls` shows setuid files with a red background.
- Lowercase `s` = setuid plus execute. Capital `S` = setuid with no execute underneath, usually a mistake.
- **On a directory, setuid does nothing on Linux.** A new file's owner is always its creator.
- Security: every setuid-root program is a place where a bug could hand out root.

**Setgid**

- Use: team folders, so everyone's new files share one group. A team folder is usually `2775` so the group can also write.
- Lab: `before.txt` (made before setgid) got my private group. `after.txt` (made after `chmod g+s`) got `shared`. The only change was the `s`.
- The `s` doesn't give the group any access. Access still comes from `r` and `x`.

**Capital letters and numeric chmod**

- Capital `S` or `T` means the special bit is set but the execute bit is not.
- A numeric `chmod` with a leading digit **replaces** all special bits at once. `chmod 4755` on a setgid folder removes the setgid.

Spot them: `ls -l /usr/bin/passwd` (the `s`), `ls -ld /tmp` (the `t`).

### File attributes: chattr and lsattr (added)

Attributes sit below normal permissions and can stop even root.

```bash
lsattr file                  # view attributes
sudo chattr +i file          # immutable: can't modify, delete, or rename, even as root
sudo chattr -i file          # remove it
sudo chattr +a file          # append-only (good for logs)
```

---

## 9. ACLs (Access Control Lists)

Standard permissions only cover owner, group, and others. ACLs give **per-user or per-group** permissions on one specific file.

Install the tools if needed: `sudo apt install acl -y`

```bash
getfacl filename                          # view ACLs
sudo setfacl -m u:username:rw filename    # give a user read+write
sudo setfacl -m u:username:rwx filename   # full access
sudo setfacl -m g:groupname:rx filename   # give a group read+execute
sudo setfacl -x u:username filename       # remove one entry
sudo setfacl -b filename                  # remove ALL ACLs
```

Reading `getfacl` output:

```
# file: testfile.txt
# owner: devrehannalp
# group: devrehannalp
user::rw-               <- owner permissions
user:acltest:rw-        <- ACL entry for a specific user
group::r--              <- group permissions
mask::rw-               <- maximum permissions any ACL entry can have
other::r--              <- others permissions
```

More to know (added):

- `ls -l` shows a **`+`** at the end of the permission string when a file has an ACL.
- The **mask** caps the effective permissions of named users, named groups, and the owning group. Running `chmod` on a file with an ACL changes the mask. `getfacl` shows the result as `#effective:`.
- **Default ACLs** on a directory are inherited by new files inside: `setfacl -d -m g:team:rwx dir/`.
- Recursive: `setfacl -R -m ...`. Back up and restore: `getfacl -R dir > acls.txt` then `setfacl --restore=acls.txt`.
- Backups must opt in to keep ACLs (for example `tar --acls`, `rsync -A`).

---

## 10. systemd Deeper

### Units and states (2.5)

Unit types: **services**, **timers**, **mounts**, **targets** (also sockets and paths).

```bash
sudo systemctl start|stop|restart|reload|status <unit>
sudo systemctl enable|disable <unit>
sudo systemctl mask|unmask <unit>      # mask blocks it from starting at all
sudo systemctl edit <unit>             # safe override file (drop-in) (added)
sudo systemctl daemon-reload           # after changing unit files
systemctl list-units --type=mount      # mounts are units too (added)
```

Unit files: admin-made in `/etc/systemd/system/`, package-provided in `/usr/lib/systemd/system/`.

### Targets

Targets define what state the system boots into.

| Target              | Purpose                                     | Old runlevel (added) |
| ------------------- | ------------------------------------------- | -------------------- |
| `poweroff.target`   | Shutdown                                    | 0                    |
| `rescue.target`     | Single user, minimal, like safe mode        | 1                    |
| `multi-user.target` | Normal server mode, no GUI                  | 3                    |
| `graphical.target`  | Normal desktop mode with GUI                | 5                    |
| `reboot.target`     | Reboot                                      | 6                    |
| `emergency.target`  | Bare minimum, something is seriously broken | n/a                  |

```bash
systemctl get-default                           # check current target
sudo systemctl set-default multi-user.target    # switch to server mode
sudo systemctl set-default graphical.target     # switch to desktop mode
sudo systemctl isolate rescue.target            # switch right now (added)
systemctl list-dependencies multi-user.target   # what it pulls in (added)
```

Servers typically run `multi-user.target`.

### Timers

Timers are systemd's scheduler, an alternative to cron.

```bash
systemctl list-timers           # active timers
systemctl list-timers --all     # including inactive
```

Columns: `NEXT` (when it runs next), `LEFT` (time until then), `LAST` (when it last ran), `UNIT` (the `.timer`), `ACTIVATES` (the `.service` it triggers).

System timers I've seen: `apt-daily.timer` (package updates), `logrotate.timer` (log rotation), `dpkg-db-backup.timer`, `man-db.timer`.

**Making my own (added):** a timer is a pair of files. The `.timer` triggers the `.service` with the same name.

```
# /etc/systemd/system/backup.service
[Unit]
Description=Nightly backup
[Service]
Type=oneshot
ExecStart=/home/user/backup.sh

# /etc/systemd/system/backup.timer
[Unit]
Description=Run backup nightly
[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true
[Install]
WantedBy=timers.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now backup.timer
systemd-analyze calendar "*-*-* 02:00:00"    # check a schedule is valid
```

- `OnCalendar=` is a clock time. `OnBootSec=` and `OnUnitActiveSec=` are relative to boot or the last run.
- `Persistent=true` runs a job that was missed while the machine was off.
- Enable the **timer**, not the service.

### Utilities from the objectives (added)

| Command           | Does                                                                                                                                                                                               |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `hostnamectl`     | Show or set the hostname (`sudo hostnamectl set-hostname name`)                                                                                                                                    |
| `resolvectl`      | DNS status and lookups (`resolvectl status`, `resolvectl query host`). `systemd-resolved` is the resolver service behind it                                                                        |
| `sysctl`          | Kernel settings: `sysctl -a`, `sysctl net.ipv4.ip_forward`, `sudo sysctl -w key=value` (until reboot). Make permanent in `/etc/sysctl.conf` or `/etc/sysctl.d/`, apply with `sudo sysctl --system` |
| `systemd-analyze` | Boot time. `systemd-analyze blame` shows the slowest units (the objectives call it "systemd-blame"). `critical-chain` shows what delayed boot                                                      |
| `timedatectl`     | Time, timezone, NTP (see Week 1, section 13)                                                                                                                                                       |

---

## 11. Logs: journalctl

```bash
journalctl -n 20                    # last 20 entries
journalctl -f                       # follow live
journalctl -u servicename           # one service
journalctl --since "1 hour ago"     # time filter
journalctl -p err                   # errors and worse
journalctl -p err -n 10             # last 10 errors
journalctl -b                       # since last boot
journalctl -k                       # kernel messages only (added)
journalctl --disk-usage             # how much space logs use (added)
sudo journalctl --vacuum-time=7d    # trim old logs (added)
```

- Priorities (low number is worse): 0 emerg, 1 alert, 2 crit, 3 err, 4 warning, 5 notice, 6 info, 7 debug. `-p err` shows err and everything worse.
- Reading a log line: `Apr 27 17:36:21 RehannaLP systemd-resolved[139]: Clock change detected.` is timestamp, hostname, service and PID, then the message.
- Classic log files: `/var/log/auth.log` on Debian/Ubuntu, `/var/log/secure` on RHEL. `rsyslog` writes them and `logrotate` rotates them.

---

## 12. Network Configuration Basics

Full tool list and Netplan/NetworkManager are in Week 1, section 4. The basics:

```bash
hostname              # machine name
hostname -I           # IP address only
ip addr               # all interfaces and IPs
```

- `lo` is the loopback interface, always `127.0.0.1`: the system talking to itself.
- `eth0` is the real interface in WSL (my real IP). MAC address is the hardware identifier (like `00:15:5d:10:64:8a`).
- **`/etc/resolv.conf`:** `nameserver` lines name the DNS servers. On WSL it points to WSL's internal resolver. On real servers it's often `8.8.8.8` or company DNS.
- **`/etc/hosts`:** the system checks this **before** asking DNS. `127.0.0.1 localhost` always resolves to myself. On servers it maps internal names without DNS:

```
192.168.1.50    webserver.company.com
192.168.1.51    database.company.com
```

---

## 13. Labs Done

1. `useradd testuser` showed the bare defaults (UID 1001, `/bin/sh`, no home). Removed it and redid it with `-m -s /bin/bash`.
2. `passwd` changed the `shadow` field from `!` to a hash. `su - testuser`, then `whoami` and `pwd`, proved the account works.
3. `groupadd devteam`, `usermod -aG`, hit the `-G` trap and fixed it.
4. `userdel -r` refused until `pkill -9` ended the leftover shell.
5. `chage -M 90 -W 14` moved "expires" from `never` to a real date. `chage -d 0` forced a password change.
6. Permissions: root-owned file (`Permission denied` until `chown`), `chmod o-r` and `chmod 644`, folder without `x` (`?????????`), umask `077`.
7. Special bits: sticky bit stopped `sticky2` from deleting my file, `ls -l /usr/bin/passwd` showed the setuid `s`, setgid made `after.txt` inherit group `shared`.
8. Cleaned up every test user, group, and file each time.

---

## 14. Mistakes Worth Remembering

- `touch hello > file` is not `echo hello > file`. `touch` makes an empty file named `hello`. `echo` prints the text that `>` sends into the file.
- The path is `/tmp/name`, not `~/tmp/name`. The `~` means my home.
- `~name` without the slash means "the home of a user named name".
- Step out of a folder before deleting it. Don't keep using a folder after removing it.
- `cd passwd` fails because `passwd` is a file.

---

## 15. Exam Gotchas (quick list)

**Accounts**

- `useradd` without options: `/bin/sh`, no home, no password. `-m` creates the home.
- `usermod -G` without `-a` replaces secondary groups.
- `userdel -r` removes the home directory. `userdel` fails if the user has running processes.
- System UIDs are below 1000, regular users start at 1000, `nobody` is 65534.
- Primary group lives in `/etc/passwd`, secondary members live in `/etc/group`.
- `x` in `/etc/passwd` means the hash is in `/etc/shadow`. `/etc/shadow` is root-only.
- `chage -M` expires the password, `chage -E` expires the account, `chage -d 0` forces a change.
- A locked password (`usermod -L`) does not block SSH keys. Expire the account too.
- Always edit sudoers with `visudo`. Debian/Ubuntu use the `sudo` group, RHEL uses `wheel`.
- `NOPASSWD` removes the password check. `NOEXEC` blocks shell escapes.

**Permissions**

- New file group = creator's **primary** group.
- `chown user:group file` sets both, `chown :group file` sets only the group.
- A folder needs `x` to be entered. Deleting a file needs write on the **folder**.
- umask is subtracted from `666` (files) and `777` (directories). `022` gives 644/755, `077` gives 600/700.
- Sticky `t` on `/tmp`, setuid `s` on `passwd`, setgid `s` on team folders. Setuid on a directory is ignored.
- Capital `S` or `T` means the special bit is set but execute is not.
- `ls -l` shows `+` when a file has an ACL. `chmod` on an ACL file changes the mask.
- `chattr +i` makes a file immutable even for root.

**systemd**

- `enable` is for boot, `start` is for now. `mask` is stronger than `disable`.
- After editing a unit file: `daemon-reload`. Enable the `.timer`, not the `.service`.
- `/etc/hosts` is checked before DNS.

---

## 16. Self-Check Questions (cover the answers and try)

1. Which file holds the password hashes, and why is it separate from `/etc/passwd`?
2. What does the 4th field of `/etc/passwd` store?
3. What UID do regular users start at? What is 65534? What is a service account?
4. What does `useradd` do if I give it no options? What does `/etc/skel` do?
5. What is the difference between `usermod -G` and `usermod -aG`?
6. How do I lock an account fully, and why isn't `passwd -l` enough?
7. What is the difference between `chage -M` and `chage -E`? How do I force a password change at next login?
8. `userdel` says the user is "currently used by process". What do I run first, and what is the forceful fix?
9. How do I safely edit sudoers? Which group grants sudo on Ubuntu vs RHEL?
10. A new file gets which group? What if I create it with `sudo`?
11. What are the numbers for `rw-r-----`? For `rwxr-xr-x`?
12. Why can't I `cd` into a folder I own that has mode `600`?
13. What does umask `022` produce for new files and directories? Why does `umask 700` not give mode 700?
14. What problem does the sticky bit solve, and where is it used?
15. Why can a normal user run `passwd` and still change `/etc/shadow`? What is EUID?
16. What does setgid do on a directory?
17. What does `chattr +i` do that `chmod` can't?
18. What does the `+` at the end of a permission string mean? What is the ACL mask?
19. What is the difference between `systemctl set-default` and `systemctl isolate`?
20. How do I make a systemd timer that runs a script nightly, and what does `Persistent=true` do?
21. What does `systemctl mask` do that `disable` doesn't?
22. Which file does the system check before asking DNS?

---

## Appendix: Git Sync Habits (move to the github-commands cheatsheet when ready)

Repos live in `~/git_repos` (underscore) on the computer and the tablet, cloned from GitHub, which is the source of truth. Habit: `git pull` before working, `git commit` then `git push` when finished.

```bash
git status                            # modified or untracked files
git fetch                             # refresh remote info without changing files
git log --oneline -3                  # compare top hash across devices
git log origin/main..HEAD --oneline   # commits that never reached GitHub
git stash list                        # stashed work
git status --ignored                  # ignored files a re-clone won't bring back
git restore README.md                 # discard a local edit (permanent)
git reset --hard origin/main          # make local match GitHub exactly
git mv oldpath newpath                # move a file and let Git track it
diff -rq folderA folderB              # compare two folders, differences only
```

A normal `mv` works too: after `git add .`, `git status` shows the move as a rename. A fresh clone only holds what was committed, so ignored or never-tracked files do not come with it.

---

## Next

- Find setuid files on the system: `find / -perm -4000 -type f 2>/dev/null` (security audit)
- Week 3 (Security): SELinux, SSH keys, firewalls (`ufw`, `iptables`), account hardening, PAM

---

_CompTIA Linux+ XK0-006 | Week 2 Master Notes | DevRehannaLP_

∞ ☬ DevRehannaLP ☬ | DevSecOps ∞
