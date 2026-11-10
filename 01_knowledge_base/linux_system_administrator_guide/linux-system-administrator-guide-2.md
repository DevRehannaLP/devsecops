# Linux System Administration · Unit 2: User and Group Management

## 🚪 The Gatekeepers of Your System: Users and Groups
Imagine a busy office building. Every employee has a badge that grants access to specific floors and rooms. Some badges open the server room, others only the break room. In Linux, **users and groups are that badge system**. Without them, every process would run with the same unlimited power — a recipe for chaos and security disasters.

> 💡 **Catch Wisdom**  
> Every file, process, and service in Linux is owned by someone. Mastering user and group management is the first step to securing and organizing your system.

### 🎯 This Unit Will Give You 3 Things:
1. Recognize the three types of Linux accounts and their UID ranges.
2. Understand how to create, modify, and lock user accounts using `useradd`, `usermod`, and `passwd`.
3. Learn the structure of `/etc/passwd` and `/etc/shadow` and why you should **never** edit them directly.

> 🛑 **Myth vs. Fact**  
> **Myth:** "It is safe to edit `/etc/passwd` directly with a text editor to add or modify user accounts."  
> **Fact:** False. Always use dedicated commands (`useradd`, `vipw`, etc.) to safely modify account records and ensure proper file locking.

---

## 👤 The Three Types of Linux Accounts
Linux distinguishes three categories of user accounts, each with a specific purpose and a numeric User ID (UID) range. 

| Account Type | UID Range | Purpose & Characteristics |
| :--- | :--- | :--- |
| **Root** | `0` | Unrestricted access. Full system control. *Never use for daily tasks.* |
| **System Users** (Service Accounts) | `1` – `999` | Run background services (web servers, databases). Usually have **no home directory** and **no login shell** (`/usr/sbin/nologin`) to prevent interactive logins. |
| **Regular Users** (Human Accounts) | `1000+` | Interactive human accounts. Have a home directory and a login shell (e.g., `/bin/bash`). Starts at 1000 on Ubuntu, 500 on older RHEL. |

*Note: UID ranges are configured in `/etc/login.defs` and can vary by distribution.*

> ⚠️ **Why not use root for everything?**  
> Root can do anything, including accidentally deleting critical system files. Always create a regular user for daily work and use `sudo` for administrative tasks.

---

## 📂 The Core Configuration Files
Linux stores user and group information in plaintext files. Administrators can read them, but should **never edit them directly** with a standard text editor. Dedicated commands modify these files safely.

- **`/etc/passwd`**: Contains basic user info (7 colon-separated fields). The password field is just an `x` placeholder.
- **`/etc/shadow`**: Contains the actual hashed passwords and password expiry info. Readable **only by root**.
- **`/etc/group`** & **`/etc/gshadow`**: Store group information and group passwords.

### 🧬 Anatomy of `/etc/passwd`
```text
jsmith:x:1001:1001:John Smith:/home/jsmith:/bin/bash
  |   |  |    |     |          |            |
  1   2  3    4     5          6            7
```
1. **Username**: `jsmith`
2. **Password placeholder**: `x` (actual hash is in `/etc/shadow`)
3. **UID**: `1001`
4. **GID**: `1001` (Primary Group ID)
5. **GECOS**: `John Smith` (Comment field, often full name)
6. **Home directory**: `/home/jsmith`
7. **Default shell**: `/bin/bash`

> ❌ **Common Mistakes**  
> - **Wrong**: Editing `/etc/passwd` directly. → **Correct**: Use `vipw` or `useradd`.  
> - **Wrong**: Storing actual passwords in `/etc/passwd`. → **Correct**: Use `/etc/shadow` for hashes.  
> - **Wrong**: Assuming the GID field is the group name. → **Correct**: It's the numeric ID; name is looked up in `/etc/group`.

---

## 🛠️ Creating Users: `useradd` vs `adduser`

| Distribution | Command | Behavior |
| :--- | :--- | :--- |
| **Debian/Ubuntu** | `sudo adduser jsmith` | Interactive wrapper. Creates user, home dir, copies `/etc/skel`, sets shell, and prompts for password/GECOS. |
| **RHEL/CentOS/Arch** | `sudo useradd -m -s /bin/bash jsmith` <br> `sudo passwd jsmith` | Low-level, portable. Requires `-m` for home dir, `-s` for shell. Password must be set separately. |
| **System/Service Account** | `sudo useradd -r -s /usr/sbin/nologin myapp` | `-r` assigns a system UID (<1000). `/usr/sbin/nologin` prevents interactive login. No home dir by default. |

### 🔍 Verify the New User
```bash
id jsmith                  # See UID, GID, and group memberships
grep jsmith /etc/passwd    # Confirm the entry exists
ls -la /home/jsmith        # Check that the home directory was created
su - jsmith                # Test login by switching to the new user
```

---

## 🔧 Modifying Users with `usermod`
The `usermod` command changes attributes of existing accounts. 

- **Change shell**: `usermod -s /bin/zsh username`
- **Rename user**: `usermod -l newname oldname` *(Note: home dir path doesn't change automatically; use `-d` and `-m` to move it).*
- **Set expiry date**: `usermod -e 2025-12-31 username`
- **Lock account**: `usermod -L username` *(Prepends `!` to the hash in `/etc/shadow`)*
- **Unlock account**: `usermod -U username`

> ⚠️ **The `-aG` Pitfall**  
> When adding a user to supplementary groups, **always use `-aG`** (append).  
> If you run `usermod -G docker,www-data jsmith` *without* `-a`, the user will **lose all existing supplementary group memberships**.  
> ✅ **Correct**: `sudo usermod -aG docker jsmith`

---

## 👥 Group Management Essentials
Groups are managed with a parallel set of commands:
- `groupadd`: Creates a new group.
- `groupmod`: Changes group name or GID.
- `groupdel`: Removes a group.
- `gpasswd`: Manages group passwords and administrators.

> 💡 **Pro Tip**  
> When you add a user to a supplementary group with `usermod -aG`, the change takes effect immediately for *new* logins. The user must log out and back in to see the new group memberships in their current session.

---

## 🔐 Password Management and Account Expiry

1. **Set or change a password**:  
   `sudo passwd jsmith` *(A user created with `useradd` has no password by default and cannot log in until one is set).*
2. **Enforce password expiry with `chage`**:  
   - `sudo chage -M 90 jsmith` (Password expires after 90 days)  
   - `sudo chage -W 7 jsmith` (Warn the user 7 days before expiry)  
   - `sudo chage -E 2025-12-31 jsmith` (Set absolute account expiry date)
3. **Lock/Unlock**:  
   - Lock: `sudo usermod -L jsmith`  
   - Unlock: `sudo usermod -U jsmith`

---

## ⚙️ System Accounts and Declarative Creation
Service accounts should be locked down. Use `useradd -r -s /usr/sbin/nologin myapp`.

On **systemd-based distributions**, you can also create service users declaratively by placing a file in `/etc/sysusers.d/`.  
Format: `type name UID GECOS home_directory shell`  
Example: `u myapp - "My App Service" /var/lib/myapp /usr/sbin/nologin`  
*This is idempotent (safe to run multiple times) and great for configuration management.*

---

## 📌 Key Takeaways
- Linux has three account types: **Root** (UID 0), **System Users** (UID 1-999), and **Regular Users** (UID 1000+).
- User data is stored in `/etc/passwd` (basic info) and `/etc/shadow` (hashed passwords/expiry). **Never edit these directly.**
- Use `useradd` for portable scripting and `adduser` for interactive setup on Debian/Ubuntu.
- **Always** use `usermod -aG` to append supplementary groups; omitting `-a` replaces all existing memberships.
- System accounts should use `/usr/sbin/nologin` as the shell and can be created declaratively via `sysusers.d` on systemd systems.

***

How does this look for your notes, Rehanna? If you want, we can pick one of those practice scenarios (like the `-aG` pitfall or the system account creation steps) and run through it in your WSL terminal together. You've got this! 💪☬
