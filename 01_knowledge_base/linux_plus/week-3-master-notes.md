# Linux+ Week 3: Security & Hardening

## 1. Special Permissions Audit (Setuid, Setgid, Sticky)

- **Setuid (4000)**: Executes with the permissions of the file's _owner_ (often
  root).
- _Example_: `passwd` needs this to let users update `/etc/shadow`.
- _Audit Command_: `find / -type f -perm -4000 2>/dev/null`
- _Remediation (Remove setuid)_: `chmod u-s /path/to/file`
- **Setgid (2000)**: Executes with the permissions of the file's _group_, or
  forces new files in a directory to inherit the directory's group.
- **Sticky Bit (1000)**: On directories (like `/tmp`), only the file owner or
  root can delete files, even if the directory is world-writable.

## 2. SSH Key Management (NEXT)

- Generating keys (`ssh-keygen`)
- Copying keys to remote hosts (`ssh-copy-id`)
- Disabling password authentication in `sshd_config`

## 3. Basic Firewall (NEXT)

- UFW (Uncomplicated Firewall) basics
- Allowing specific ports (e.g., `ufw allow 22/tcp`)
- Checking status (`ufw status verbose`)
- **firewalld (RHEL/CentOS):** `firewall-cmd --state`
- **Add port:** `firewall-cmd --add-port=80/tcp --permanent`

## 4. SELinux / AppArmor Basics (NEXT)

- Concept of Mandatory Access Control (MAC) vs. Discretionary Access Control
  (DAC)
- Checking status (`getenforce` or `aa-status`)

## 5. File Integrity & Hashing (Crucial!)

- You need to know how to verify that a file hasn't been tampered with.
  - **Commands:** sha256sum, md5sum.
  - Connections: Remember that md5sum.txt file in your Ubuntu ISO screenshot?
    That's exactly what this is for!

## 6. Sudo Configuration

- You know how to use sudo, but the exam tests how to configure it.
  - **Concept:** The /etc/sudoers file.
  - **Rule:** Never edit it directly. Always use the visudo command to edit
    safely.

## 7. PAM (Pluggable Authentication Modules)

- **Concept:** A system Linux uses to authenticate users (enforcing password complexity, locking accounts after failed attempts).
- **Exam Keywords:** `pam_faillock` (modern RHEL/Ubuntu) or `pam_tally2` (older systems) are the specific modules used to lock accounts after X failed attempts.
- _Rule:_ You don't need to memorize the config files, just know what PAM does and those module names.
