# Linux+ Week 3: Security & Hardening

## 1. Special Permissions Audit (Setuid, Setgid, Sticky)

- **Setuid (4000)**: Executes with the permissions of the file's _owner_ (often
  root).
- _Example_: `passwd` needs this to let users update `/etc/shadow`.
- _Audit Commandr_: `find / -type f -perm -4000 2>/dev/null`
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

## 4. SELinux / AppArmor Basics (NEXT)

- Concept of Mandatory Access Control (MAC) vs. Discretionary Access Control
  (DAC)
- Checking startus (`getenforce` or `aa-status`)
