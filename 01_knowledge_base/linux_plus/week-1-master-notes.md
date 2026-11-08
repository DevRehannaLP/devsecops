# Week 1 Master Notes: System Management (Linux+ XK0-006)

Domain 1.0 System Management (23%)

**What this file is:** my original Week 1 notes (file system, boot, packages,
shell, archiving, storage, processes, logs, time, scheduling, quotas) merged
with the reference notes and checked against the official XK0-006 objectives
(document version 5.0). Anything marked **(added)** was missing from my
original notes and comes from the official objectives.

Trimmed from the originals: the "Question for you" check-ins (they were chat
prompts, not study material), duplicate explanations, and typos. The exam
tricks, warnings, and real-world examples are kept.

---

## Objective Coverage Map

| Objective | Topic                                                                                                           | Section |
| --------- | --------------------------------------------------------------------------------------------------------------- | ------- |
| 1.1       | Basic Linux concepts (boot, FHS, architectures, distros, GUI, licensing)                                        | 1       |
| 1.2       | Device management                                                                                               | 2       |
| 1.3       | Storage (LVM, partitions, filesystems, RAID, mounts, inodes)                                                    | 3       |
| 1.4       | Network services and configuration                                                                              | 4       |
| 1.5       | Common shell operations                                                                                         | 5       |
| 1.6       | Backup and restore                                                                                              | 6       |
| 1.7       | Virtualization                                                                                                  | 7       |
| 1.8       | Files and directories                                                                                           | 8       |
| Extra     | Packages, systemctl, processes, logs, time, scheduling, quotas (studied in Week 1, tested in other domains too) | 9 to 15 |

---

## 1. Basic Linux Concepts (1.1)

### 1.1 Filesystem Hierarchy Standard (FHS)

Everything lives under `/`. Think of a family tree: `/` is the ancestor,
`/home` a child, `/home/rehanna` a grandchild.

**`/` vs `/root`:** `/` is the top of the whole tree. `/root` is the home
folder of the root user. `cd /` goes to the top, `cd ~` goes to my own home.

| Directory        | Purpose                                                                 | Exam trick / warning                                             |
| ---------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `/`              | Top of the tree, parent of everything                                   | Only one root directory. Never delete from it unless sure        |
| `/bin`           | Essential commands for all users (`ls`, `cp`, `mv`, `cat`, `rm`, `pwd`) | On modern Ubuntu, `/bin` is a symlink to `/usr/bin`              |
| `/sbin`          | Admin commands (`reboot`, `fdisk`, `mkfs`, `fsck`, `ip`)                | Usually needs `sudo`                                             |
| `/usr`           | "Unix System Resources": most installed software, docs, libraries       | Where most user apps live is `/usr/bin`, not `/bin`              |
| `/usr/local`     | Software I compile or install manually                                  | Survives system updates                                          |
| `/etc`           | ALL system configuration, as text files                                 | Broken system? Check `/etc` first. Back up before editing        |
| `/home`          | Regular users' personal files and hidden configs (`.bashrc`, `.ssh/`)   | Root is not here                                                 |
| `/root`          | The root user's home                                                    | `/root`, NOT `/home/root`. Regular users get "Permission denied" |
| `/var`           | Variable data: logs, spool, cache, mail, web content                    | The top cause of a full disk                                     |
| `/tmp`           | Temporary files                                                         | Usually cleared on reboot. World-writable with the sticky bit    |
| `/opt`           | Optional third-party software, one folder per app                       | `rm -rf /opt/app` removes it cleanly                             |
| `/dev`           | Device files (hardware as files)                                        | Never delete things in here                                      |
| `/proc`          | Virtual: processes and kernel info, only in RAM                         | `cat /proc/cpuinfo`                                              |
| `/sys`           | Virtual: hardware devices and drivers, only in RAM                      | `/sys/class/net/`                                                |
| `/boot`          | Kernel, initramfs, GRUB files                                           | Deleting the kernel makes the system unbootable                  |
| `/lib`           | Shared libraries (`.so` files) and kernel modules (`/lib/modules/`)     | "cannot open shared object file" error                           |
| `/run`           | Runtime data since boot (in memory) (added)                             |                                                                  |
| `/mnt`, `/media` | Mount points for temporary and removable storage (added)                |                                                                  |
| `/srv`           | Data served by this machine (added)                                     |                                                                  |

Details worth keeping:

- **`/etc`** holds: `/etc/passwd`, `/etc/shadow` (accounts), `/etc/resolv.conf`
  and `/etc/hosts` (network), `/etc/ssh/`, `/etc/systemd/`, `/etc/fstab` (mounts),
  `/etc/sudoers` (edit with `visudo`), `/etc/hostname`.
- **`/etc` vs `/bin`:** `/bin` and `/sbin` are programs. `/etc` is text files
  that tell programs how to behave.
- **`/home` vs `/etc`:** `/home` is user-specific, `/etc` is system-wide. Back
  up `/home/username` regularly. `/etc` mostly for full system migrations.
- **`/var` details:** `/var/log` (logs), `/var/spool` (queued jobs),
  `/var/cache` (caches, like apt), `/var/www` (web files), `/var/mail`. Server
  stopped accepting connections? Check `df -h`, then `du -sh /var/log/*`.
- **`/tmp`:** anything saved here is gone after a reboot. Never keep backups,
  keys, or documents in it.
- **`/opt`:** a program at `/opt/myapp/bin/prog` may need `/opt/myapp/bin` added
  to `PATH`.
- **`/dev` details:** `/dev/sda` is the first SATA/SCSI disk, `/dev/sda1` its
  first partition, `/dev/nvme0n1` an NVMe SSD. Special files: `/dev/null`
  (black hole), `/dev/zero` (endless zeros), `/dev/random` and `/dev/urandom` (random data).
- **`/proc` vs `/sys` vs `/dev`:** `/dev` is hardware access, `/proc` is processes and kernel stats, `/sys` is hardware structure and drivers. `/proc/<PID>/cmdline` shows how a process was started.
- **`/boot` details:** kernel files are named `vmlinuz-...`, initramfs is `initrd.img-...`, GRUB config is under `/boot/grub/`. A full `/boot` can block updates.
- **`/lib` details:** `ldd /usr/bin/program` lists the libraries a program needs.

### 1.2 Boot Process

The order never changes:

1. **BIOS/UEFI** (firmware on the motherboard). Runs POST (power-on self-test), then looks for a bootloader. BIOS is the old way (MBR). UEFI is the modern way (GPT, faster, more secure, supports Secure Boot, uses an EFI System Partition (ESP, FAT32)).
2. **GRUB** (Grand Unified Bootloader). First software loaded from disk. Shows the boot menu and loads the kernel.
3. **initrd/initramfs.** A small temporary filesystem in RAM with the drivers the kernel needs to find the real root filesystem.
4. **Kernel** (`vmlinuz-...`). Takes over CPU, memory, and hardware, loads drivers, mounts the real root `/`.
5. **systemd.** The first process, always **PID 1**. Starts all services and reaches the default target (`multi-user.target` for servers, `graphical.target` for desktops).

**PXE (Preboot Execution Environment):** boots a machine over the network instead of a local disk. Used in data centers to deploy Linux to many machines at once.

**Bootloader config and kernel parameters (added):**

- GRUB settings live in `/etc/default/grub` (kernel parameters go in `GRUB_CMDLINE_LINUX`).
- The generated config is `/boot/grub/grub.cfg`. Do not edit it by hand. Regenerate with `update-grub` (Debian/Ubuntu) or `grub2-mkconfig -o ...` (RHEL family).
- At the boot menu, press `e` to edit parameters for one boot. Examples: `quiet`, `ro`, `systemd.unit=rescue.target`.
- A corrupted GRUB config drops me to a `grub rescue>` prompt.

**initrd management (added):** rebuild it with `update-initramfs -u` (Debian/Ubuntu), `dracut --force` (RHEL family), or the older `mkinitrd`.

**Exam tricks:**

- First process the kernel starts: systemd (PID 1).
- Kernel can't find the root filesystem: it drops to an initramfs/emergency shell (or a kernel panic).
- GRUB broken: boot a live USB, chroot into the system, and reinstall GRUB.
- Kernel messages: `dmesg`. This boot's logs: `journalctl -b`.

**WSL note:** WSL does not boot through GRUB, so bootloader work can only be studied, not practiced there.

### 1.3 Server Architectures

| Architecture       | What it is                                           |
| ------------------ | ---------------------------------------------------- |
| `x86`              | 32-bit Intel/AMD, older systems                      |
| `x86_64` / `AMD64` | 64-bit Intel/AMD, most desktops and servers          |
| `AArch64`          | 64-bit ARM: Raspberry Pi, cloud servers, mobile      |
| `RISC-V`           | Open-source architecture, emerging, embedded systems |

Check mine with `uname -m` or `lscpu`. Most Linux servers run x86_64. AArch64 is growing fast in the cloud.

### 1.4 Distributions (added)

- **RPM-based:** RHEL, Fedora, Rocky, Alma (SUSE also uses RPM). Tools: `rpm`, `dnf`/`yum`.
- **dpkg-based:** Debian, Ubuntu. Tools: `dpkg`, `apt`.

### 1.5 GUI Components (added)

- **Display manager:** the graphical login screen (GDM, SDDM, LightDM).
- **Window manager:** draws and moves windows (i3, Openbox, Mutter in GNOME).
- **X Server (X11):** the older display system.
- **Wayland:** the modern replacement for X.
- The `DISPLAY` environment variable tells programs which X display to use.

### 1.6 Software Licensing

| License type  | What it means                                                                   |
| ------------- | ------------------------------------------------------------------------------- |
| Open source   | Source code is public, anyone can view and modify                               |
| Free software | Freedom to run, study, share, modify. Free as in freedom, not necessarily price |
| Proprietary   | Source closed. Use it, but can't modify it                                      |
| Copyleft      | Modified versions must also stay open (example: GPL)                            |

Linux itself uses the GPL, a copyleft license.

---

## 2. Device Management (1.2) (added)

### Kernel modules

Modules are drivers the kernel loads on demand. They live in `/lib/modules/<kernel version>/`.

| Command            | Does                                                  |
| ------------------ | ----------------------------------------------------- |
| `lsmod`            | List loaded modules                                   |
| `modinfo name`     | Show details about a module                           |
| `modprobe name`    | Load a module **and its dependencies**                |
| `modprobe -r name` | Unload it (with dependencies)                         |
| `insmod file.ko`   | Load a module from a file, **no dependency handling** |
| `rmmod name`       | Remove a module                                       |
| `depmod`           | Rebuild the module dependency map                     |

Blacklisting a module: add `blacklist name` to a file in `/etc/modprobe.d/`.

### Hardware information tools

| Command                  | Shows                                                          |
| ------------------------ | -------------------------------------------------------------- |
| `dmesg`                  | Kernel messages (hardware detection, errors)                   |
| `lscpu`                  | CPU details                                                    |
| `lsmem`                  | Memory blocks                                                  |
| `lspci`                  | PCI devices (graphics, network cards)                          |
| `lsusb`                  | USB devices                                                    |
| `lshw`                   | Full hardware list                                             |
| `dmidecode`              | BIOS/system/hardware info (needs root)                         |
| `ipmitool`               | Manage server hardware through the baseboard controller (IPMI) |
| `lm_sensors` (`sensors`) | Temperatures and fan speeds                                    |

`lspci` and `lsusb` read their data from `/sys`.

### Custom hardware

- Embedded systems are small, single-purpose devices running Linux.
- GPU use cases include machine learning and rendering. `nvtop` monitors GPU usage like `htop` does for the CPU.

---

## 3. Storage Management (1.3)

In Linux a drive is a file in `/dev`. To use it, I mount it to a directory (a mount point). Windows uses drive letters. Linux uses paths.

### Checking space

```bash
df -h                  # free space per filesystem, human-readable
df -h /home            # space for the filesystem holding /home
df -i                  # inode usage (added)
du -sh folder/         # size of a folder
du -sh *               # size of everything in the current directory
```

- `df` = how much space on the whole drive. `du` = how much one folder uses.
- "I can't save files" → check `df -h` for 100%. Then `du -sh /var/log/*` to find the culprit.

### Viewing devices

```bash
lsblk                  # tree of disks and partitions
lsblk -f               # adds filesystem type and UUID
blkid                  # UUIDs and filesystem types
findmnt                # what is mounted where (added)
```

Example `lsblk`: `sda` is the first disk, `sda1` and `sda2` are partitions, `MOUNTPOINT` is where it appears in the tree.

**Swap:** disk space used as overflow when RAM is full. Slower than RAM, but it keeps the system from crashing. Shows as `[SWAP]` in `lsblk`. Created with `mkswap`, enabled with `swapon`.

### Partitions (added)

- `fdisk` (MBR and GPT), `gdisk` (GPT), `parted` (both, scriptable).
- `growpart` extends a partition (common on cloud disks).
- Careful: partitioning and `mkfs` wipe data. Double-check the device name.

### Filesystems (added)

| Type    | Notes                                                          |
| ------- | -------------------------------------------------------------- |
| `ext4`  | Ubuntu/Debian default, mature, can grow and shrink             |
| `xfs`   | RHEL default, great for big files, can grow but **not shrink** |
| `btrfs` | Snapshots and built-in volume features                         |
| `tmpfs` | Lives in RAM (`/run`, `/dev/shm`)                              |

Utilities:

| Command                 | Does                                           |
| ----------------------- | ---------------------------------------------- |
| `mkfs.ext4 /dev/sdb1`   | Make a filesystem (wipes data)                 |
| `fsck`                  | Check/repair a filesystem (**unmounted** only) |
| `xfs_repair`            | Repair XFS (XFS uses this instead of `fsck`)   |
| `resize2fs`             | Grow/shrink ext4                               |
| `xfs_growfs mountpoint` | Grow XFS (takes the mount point)               |
| `fio`                   | Benchmark disk I/O                             |

### Mounting

```bash
sudo mount /dev/sdb1 /mnt/data      # mount (lasts until reboot)
sudo umount /mnt/data               # unmount (note: umount, not unmount)
mount | grep sdb                    # is it mounted?
```

- "target is busy" means a file is open or my terminal is inside that directory. Close it or `cd` out.

**Permanent mounts: `/etc/fstab`**

1. Get the UUID: `sudo blkid /dev/sdb1`
2. Create the folder: `sudo mkdir /mnt/data`
3. Edit fstab: `sudo nano /etc/fstab`
4. Add: `UUID=xxxx-xxxx /mnt/data ext4 defaults 0 2`
5. **Test it:** `sudo mount -a`. If this errors, fix it before rebooting, because a bad line can break boot.

Six fields: device (use `UUID=`), mount point, filesystem type, options, dump (0 = no backup), fsck order (0 = skip, 1 = root, 2 = others).

**Why UUID:** device names like `/dev/sdb1` can change when I plug in another drive. UUIDs don't. A drive that vanished after reboot probably was never added to fstab.

Mount-state files (added): `/etc/fstab` (what _should_ mount), `/proc/mounts` and `/etc/mtab` (what _is_ mounted now).

**Mount options (added)**

| Option                   | Meaning                                                                               |
| ------------------------ | ------------------------------------------------------------------------------------- |
| `ro` / `rw`              | Read-only / read-write                                                                |
| `noexec`                 | Block running programs from this mount                                                |
| `nosuid`                 | Ignore setuid/setgid bits                                                             |
| `nodev`                  | Ignore device files                                                                   |
| `noatime` / `nodiratime` | Don't update access times (less disk writing)                                         |
| `nofail`                 | Boot continues even if the device is missing                                          |
| `remount`                | Change options on an already-mounted filesystem, e.g. `mount -o remount,ro /mnt/data` |

`autofs` mounts storage on demand and unmounts it after idle time.

### LVM: Logical Volume Manager (added)

Three layers: **physical volume (PV)** → **volume group (VG)** → **logical volume (LV)**.

| Layer | Create                        | Inspect                      | Other                                                      |
| ----- | ----------------------------- | ---------------------------- | ---------------------------------------------------------- |
| PV    | `pvcreate /dev/sdb1`          | `pvs`, `pvdisplay`, `pvscan` | `pvmove`, `pvremove`, `pvresize`                           |
| VG    | `vgcreate vg0 /dev/sdb1`      | `vgs`, `vgdisplay`, `vgscan` | `vgextend`, `vgremove`, `vgchange`, `vgexport`, `vgimport` |
| LV    | `lvcreate -L 10G -n data vg0` | `lvs`, `lvdisplay`           | `lvextend`, `lvresize`, `lvremove`, `lvchange`             |

**Growing an LV:** extend the LV, then grow the filesystem on it:

```bash
sudo lvextend -L +5G /dev/vg0/data
sudo resize2fs /dev/vg0/data          # ext4
sudo xfs_growfs /mnt/data             # xfs (mount point)
```

`lvextend -r` does both in one step.

### RAID (added)

`mdadm` builds software RAID. Check status with `cat /proc/mdstat` or `mdadm --detail /dev/md0`.

| Level   | What it does             | Notes                            |
| ------- | ------------------------ | -------------------------------- |
| RAID 0  | Striping                 | Fast, **no redundancy**          |
| RAID 1  | Mirroring                | Survives 1 disk failure          |
| RAID 5  | Striping + parity        | Min 3 disks, survives 1 failure  |
| RAID 6  | Striping + double parity | Min 4 disks, survives 2 failures |
| RAID 10 | Mirror + stripe          | Min 4 disks                      |

### Network mounts (added)

- **NFS** (Linux/Unix sharing): `sudo mount -t nfs server:/export /mnt/nfs`
- **SMB/Samba (CIFS)** (Windows sharing): `sudo mount -t cifs //server/share /mnt/share -o username=me`

### Inodes (added)

Every file uses one inode. A disk can have free space but be out of inodes: "No space left on device" while `df -h` looks fine. Check with `df -i`.

---

## 4. Network Services and Configuration (1.4) (added)

### Config files

| File                 | Purpose                                                                        |
| -------------------- | ------------------------------------------------------------------------------ |
| `/etc/hosts`         | Local name-to-IP mappings                                                      |
| `/etc/resolv.conf`   | DNS servers (often managed by systemd-resolved)                                |
| `/etc/nsswitch.conf` | Order of name lookups (e.g. `hosts: files dns` means check `/etc/hosts` first) |
| `/etc/hostname`      | The machine's name (`hostnamectl` changes it)                                  |

### NetworkManager and Netplan

- **NetworkManager:** `nmcli device status`, `nmcli connection show`, `nmcli connection up|down name`. The objectives list `nmcli` and `nmconnect`. `nmcli` is the one to know cold.
- **Netplan** (Ubuntu): YAML files in `/etc/netplan/`.
  - `sudo netplan try` applies with an automatic rollback if I lose connectivity
  - `sudo netplan apply` applies for good
  - `netplan status` shows the current state

### Network tools

| Tool                                | Use                                                  |
| ----------------------------------- | ---------------------------------------------------- |
| `ip address`, `ip link`, `ip route` | Interfaces, link state, routes (replaces `ifconfig`) |
| `ss`                                | Open sockets and listening ports (`ss -tulpn`)       |
| `ping` / `ping6`                    | Reachability                                         |
| `traceroute`, `tracepath`, `mtr`    | Path to a host (`mtr` is live)                       |
| `dig`, `nslookup`                   | DNS lookups                                          |
| `curl`                              | Fetch a URL                                          |
| `nc`                                | Open raw connections, test ports                     |
| `nmap`                              | Port scanning                                        |
| `tcpdump`                           | Capture packets                                      |
| `ethtool`                           | NIC speed and link settings                          |
| `arp`                               | ARP table                                            |
| `iperf3`                            | Measure bandwidth                                    |
| `hostname`                          | Show or set the host name                            |

WSL note: WSL networking is managed by Windows, so some of this behaves differently there.

---

## 5. Shell Operations (1.5)

### Redirection and pipes

| Symbol        | Does                                                           |
| ------------- | -------------------------------------------------------------- |
| `>`           | Send output to a file, **overwrites** (destroys existing data) |
| `>>`          | Append to a file                                               |
| `<`           | Feed a file in as input                                        |
| `2>`          | Redirect errors (stderr) only                                  |
| `&>`          | Redirect output and errors together                            |
| `2>&1`        | Send errors to the same place as normal output                 |
| `2>/dev/null` | Throw errors away                                              |
| `<<`          | Here doc: feed a block of text typed inline (added)            |
| `<<<`         | Here string: feed one string as input (added)                  |
| `\|`          | Pipe: output of the left command becomes input of the right    |

Streams: stdin (input), stdout (normal output), stderr (errors).

```bash
ls > files.txt              # create/overwrite
ls >> files.txt             # add to the bottom
command 2> errors.log       # only errors
ps aux | grep python        # filter processes
cat file.txt | wc -l        # count lines
command | tee file.txt      # show AND save output
```

Chaining: `cmd1 ; cmd2` (both), `cmd1 && cmd2` (only if cmd1 succeeded), `cmd1 || cmd2` (only if cmd1 failed).

### Exit codes

- `echo $?` shows the last command's exit code. `0` = success, anything else = failure.
- Scripts check `$?` to decide what to do next.

### Environment variables

| Variable   | Purpose                                  |
| ---------- | ---------------------------------------- |
| `$PATH`    | Directories searched for commands        |
| `$HOME`    | My home directory                        |
| `$USER`    | My username                              |
| `$SHELL`   | My current shell                         |
| `$PWD`     | Current directory                        |
| `$PS1`     | The prompt format (added)                |
| `$DISPLAY` | Which X display GUI programs use (added) |

```bash
echo $PATH
printenv                  # or: env
VAR=value                 # this shell only
export VAR=value          # also visible to child processes and scripts
today=$(date)             # command substitution
```

`export` only lasts for the session. To make a variable permanent, add it to `~/.bashrc`.

### Shell startup files (added)

- `~/.bashrc`: runs for each new interactive terminal
- `~/.bash_profile` / `~/.profile`: run at login
- Reload without reopening: `source ~/.bashrc`

### Paths (added)

- Absolute starts with `/`. `~` is my home.
- Relative: `.` (here), `..` (parent), `-` (previous directory, as in `cd -`).

### Basic shell utilities (added)

| Command               | Does                                                      |
| --------------------- | --------------------------------------------------------- |
| `!!`                  | Repeat the last command (`sudo !!` after forgetting sudo) |
| `!n`                  | Run history entry number n                                |
| `history`             | Show command history                                      |
| `alias`               | Create a shortcut                                         |
| `awk`                 | Split lines into fields and process them                  |
| `sed`                 | Search and replace in a stream                            |
| `cut`, `tr`           | Pull out columns / translate characters                   |
| `sort`, `uniq`, `wc`  | Sort, remove duplicates, count                            |
| `head`, `tail`        | First or last lines (`tail -f` follows a file)            |
| `cat`, `less`, `more` | View files                                                |
| `echo`, `printf`      | Print text (`printf` allows formatting)                   |
| `bc`                  | Command-line calculator                                   |
| `xargs`               | Turn input into arguments for another command             |
| `uname -a`            | Kernel and system info                                    |
| `source`              | Run a file in the current shell                           |

Editors: `vi`/`vim` and `nano`.

**Exam tricks:**

- Save output without deleting existing content: `>>`.
- `>` destroys data. `echo "hi" > important.txt` wipes the old contents.
- What `grep` receives from a pipe: standard input.

---

## 6. Backup and Restore (1.6)

### Archiving vs compression

- **Archiving:** combine many files into one (the box).
- **Compression:** shrink it (vacuum-seal the box).
- `tar` bundles files. Add a filter flag to compress.

### tar

| Flag     | Meaning                                                 |
| -------- | ------------------------------------------------------- |
| `c`      | Create                                                  |
| `x`      | Extract                                                 |
| `t`      | List contents without extracting                        |
| `v`      | Verbose                                                 |
| `f`      | File name follows (must come right before the filename) |
| `z`      | gzip (fast, common)                                     |
| `j`      | bzip2 (slower, smaller)                                 |
| `J`      | xz (slowest, smallest)                                  |
| `-C dir` | Extract into this directory                             |

```bash
tar -cvf backup.tar folder/             # archive, no compression
tar -czvf backup.tar.gz folder/         # gzip
tar -cjvf backup.tar.bz2 folder/        # bzip2
tar -xzvf backup.tar.gz                 # extract gzip
tar -xzvf backup.tar.gz -C /tmp/dest/   # extract elsewhere
tar -tzvf backup.tar.gz                 # peek inside
tar -tvf backup.tar.gz | grep index.html
```

Danger: extracting in the wrong directory dumps files there and may overwrite existing ones. Check the destination first.

### Compression tools

| Tool          | Compress                                       | Decompress         |
| ------------- | ---------------------------------------------- | ------------------ |
| gzip          | `gzip file` (replaces original, `-k` keeps it) | `gunzip file.gz`   |
| bzip2         | `bzip2 file`                                   | `bunzip2 file.bz2` |
| xz            | `xz file`                                      | `unxz file.xz`     |
| zip           | `zip out.zip folder/`                          | `unzip out.zip`    |
| 7-Zip (added) | `7z a out.7z folder/`                          | `7z x out.7z`      |

Strength: xz is smallest and slowest, then bzip2, then gzip fastest.

### Other tools (added)

| Tool                     | Use                                                                                   |
| ------------------------ | ------------------------------------------------------------------------------------- |
| `cpio`                   | Another archiver (reads a file list from stdin)                                       |
| `rsync -av src/ dest/`   | Efficient copying, only transfers changes, works over SSH. `--delete` mirrors exactly |
| `dd if=src of=dest`      | Raw copy of disks and images. **A wrong `of=` destroys the target**                   |
| `ddrescue`               | Copy from failing disks, skipping bad sectors                                         |
| `zcat`, `zgrep`, `zless` | Read compressed files without extracting                                              |

**Exam tricks:**

- Compressed archive of a directory: `tar -czvf archive.tar.gz directory/`.
- Peek inside: `-t`. The `z` is what adds gzip.

---

## 7. Virtualization (1.7) (added)

- **QEMU:** emulator that runs virtual machines.
- **KVM:** Linux kernel module that gives QEMU hardware acceleration. Together: QEMU/KVM.
- **libvirt:** management layer. Tools: `virsh` (command line) and `virt-manager` (GUI).
- **VirtIO:** paravirtualized drivers, much faster than emulated hardware.
- Check hardware support: `lscpu | grep -i virtualization` and look for `/dev/kvm`.

```bash
virsh list --all
virsh start vmname
virsh shutdown vmname
virsh snapshot-create-as vmname snap1
```

**Disk images:** `raw` (simple) and `qcow2` (copy-on-write, supports snapshots). Manage with `qemu-img info`, `qemu-img convert`, `qemu-img resize`.

**VM operations:** adjust CPU, RAM, storage, and network. Use baseline image templates, cloning, snapshots, and migrations. VM states: running, paused, shut off. Nested virtualization means running a hypervisor inside a VM.

**Bare metal vs VM:** bare metal runs straight on hardware (max performance). VMs share hardware (flexible, isolated, easy to snapshot).

**Virtual network types:**

| Type                 | Meaning                                           |
| -------------------- | ------------------------------------------------- |
| Bridged              | VM appears on the real LAN with its own IP        |
| NAT                  | VM shares the host's IP (libvirt's default)       |
| Host-only / isolated | VM can talk to the host and other VMs only        |
| Routed               | Traffic routed to the outside network without NAT |
| Open                 | No filtering rules applied                        |

---

## 8. Files and Directories (1.8) (added)

| Command                                     | Use                                                                      |
| ------------------------------------------- | ------------------------------------------------------------------------ |
| `ls`, `cd`, `pwd`                           | Look around, move, where am I                                            |
| `cp`, `mv`, `rm`, `rmdir`, `mkdir`, `touch` | Copy, move/rename, delete, remove empty dir, make dir, create empty file |
| `file name`                                 | Identify a file's type                                                   |
| `stat name`                                 | Size, inode, permissions, timestamps                                     |
| `find`                                      | Search live (`find / -name "*.conf" 2>/dev/null`)                        |
| `locate`                                    | Fast search from an index (`updatedb` refreshes it)                      |
| `diff`, `sdiff`                             | Compare files (`sdiff` side by side)                                     |
| `lsof`                                      | Which processes have which files open                                    |
| `ln`                                        | Create links                                                             |

### Links

|                    | Hard link                 | Symbolic (soft) link |
| ------------------ | ------------------------- | -------------------- |
| Create             | `ln file link`            | `ln -s target link`  |
| Points to          | The same inode (the data) | A path (name)        |
| Original deleted   | Link still works          | Link breaks          |
| Across filesystems | No                        | Yes                  |
| Directories        | No                        | Yes                  |

### Device types in /dev

- **Block devices** (`b` in `ls -l`): disks and partitions, read in blocks (`/dev/sda`).
- **Character devices** (`c`): terminals, serial ports, stream data.
- **Special character devices:** `/dev/null`, `/dev/zero`, `/dev/random`.

---

## 9. Package Management

### apt (Debian/Ubuntu)

```bash
sudo apt update              # refresh the package list (installs nothing)
sudo apt upgrade             # install available updates
sudo apt install pkg
sudo apt remove pkg          # removes program, keeps config
sudo apt purge pkg           # removes program AND config
sudo apt autoremove          # remove unneeded dependencies
sudo apt autoclean           # clear old downloaded package files
apt search word
apt show pkg
```

Always run `apt update` first. "Unable to locate package" means I forgot it.

### dpkg (low level)

`apt` uses `dpkg` under the hood. `dpkg` works on single `.deb` files and **does not resolve dependencies**.

```bash
sudo dpkg -i file.deb     # install a .deb
sudo dpkg -r pkg          # remove
sudo dpkg -P pkg          # purge (added)
dpkg -l                   # list installed
dpkg -s pkg               # status of one package
dpkg -L pkg               # files a package installed (added)
dpkg -S /path/to/file     # which package owns a file (added)
```

### Broken installs (critical for the exam)

| Symptom                                       | Fix                                           |
| --------------------------------------------- | --------------------------------------------- |
| "Unmet dependencies" / install failed halfway | `sudo apt --fix-broken install`               |
| `.deb` unpacked but not configured            | `sudo dpkg --configure -a`                    |
| Want to stop a package from updating          | `sudo apt-mark hold pkg` (undo with `unhold`) |

### Repositories

- Lists: `/etc/apt/sources.list` and `/etc/apt/sources.list.d/` (Docker, VS Code, etc.).
- Add a PPA: `sudo add-apt-repository ppa:user/repo`, then **always** `sudo apt update`.
- Third-party repos use GPG signatures to verify packages (added).

### RPM family (RHEL, Fedora, Rocky) (added)

| Task                      | Command                                           |
| ------------------------- | ------------------------------------------------- |
| Install/remove/update     | `dnf install pkg`, `dnf remove pkg`, `dnf update` |
| List installed            | `rpm -qa`                                         |
| Package info              | `rpm -qi pkg`                                     |
| Files in a package        | `rpm -ql pkg`                                     |
| Which package owns a file | `rpm -qf /path`                                   |
| Install an .rpm file      | `rpm -ivh file.rpm`                               |

Repos live in `/etc/yum.repos.d/`.

---

## 10. systemctl and systemd

systemd is PID 1 and manages services, timers, mounts, and targets.

```bash
sudo systemctl start|stop|restart|reload|status <service>
sudo systemctl enable|disable <service>        # boot behavior
sudo systemctl enable --now <service>          # enable AND start
systemctl is-active <service>
systemctl is-enabled <service>
systemctl list-units --type=service [--all]
systemctl --failed
```

- **start/stop** = now. **enable/disable** = boot. Independent.
- `restart` = stop then start. `reload` = re-read config without stopping.
- `mask` blocks a service from starting at all (even manually). `unmask` reverses it (added).
- After editing a unit file: `sudo systemctl daemon-reload` (added).
- Unit files: admin-made in `/etc/systemd/system/`, package-provided in `/usr/lib/systemd/system/` (added).
- `sudo systemctl edit <service>` makes a safe override (added).

**Targets (added):**

| Target              | Meaning                                  |
| ------------------- | ---------------------------------------- |
| `multi-user.target` | Text mode, networking                    |
| `graphical.target`  | Multi-user plus GUI                      |
| `rescue.target`     | Single-user, basic services              |
| `emergency.target`  | Minimal shell, root filesystem read-only |

```bash
systemctl get-default
sudo systemctl set-default multi-user.target
sudo systemctl isolate rescue.target
systemd-analyze blame      # slow startup? find the slow units
```

---

## 11. Process Management

### Viewing processes

- `ps aux`: snapshot of all processes (`a` all users, `u` user format, `x` no terminal). `ps -ef` is the full listing.
- `top`: real-time view (`k` kills, `q` quits). First stop if the server is slow.
- `htop`: colorful `top` (`sudo apt install htop`).
- Also know (added): `pstree`, `pidstat`, `mpstat`, `atop`, `strace`, `lsof`, and `/proc/<PID>`.

**Process IDs and states (added):**

- PID = process ID, PPID = parent's PID. systemd is PID 1.
- States: Running, Sleeping, Blocked, Stopped, **Zombie** (finished but not yet cleaned up by its parent).

### Stopping processes

| Command         | Does                                                         |
| --------------- | ------------------------------------------------------------ |
| `kill PID`      | Sends SIGTERM (15), asks nicely                              |
| `kill -9 PID`   | SIGKILL, instant, no cleanup. Last resort (can corrupt data) |
| `killall name`  | Kill by name                                                 |
| `pkill pattern` | Kill by pattern (`pkill -f python`)                          |

Signals to know: **1 HUP** (hang up, often reload config), **9 KILL**, **15 TERM**.

### Priority

- `nice -n 10 command` starts with low priority. `renice 10 -p PID` changes a running process.
- Range: -20 (highest priority) to 19 (lowest). Default is 0.
- Only root can set negative values. Regular users can only lower priority.

### Job control (added)

| Key / command     | Does                                   |
| ----------------- | -------------------------------------- |
| `command &`       | Run in the background                  |
| `jobs`            | List jobs in this shell                |
| `Ctrl+z`          | Suspend the current job                |
| `bg` / `fg`       | Resume in the background / foreground  |
| `Ctrl+c`          | Interrupt (stop)                       |
| `Ctrl+d`          | End of input / log out                 |
| `nohup command &` | Keep running after the terminal closes |

---

## 12. Log Management

### Where logs live

- `/var/log/`: `syslog` or `messages` (general), `auth.log` or `secure` (logins), `dmesg` (kernel), service logs like `nginx/error.log`.
- `rsyslog` is the classic logging service (added).

### journalctl (systemd logs)

```bash
journalctl                  # everything
journalctl -f               # follow live
journalctl -u nginx         # one service
journalctl -b               # this boot
journalctl -b -1            # previous boot
tail -n 100 /var/log/syslog
tail -f /var/log/syslog
```

### Log rotation: `logrotate`

- Logs grow forever and can fill `/var`. `logrotate` compresses old logs (`syslog.1.gz`) and deletes ones past a set age.
- Config: `/etc/logrotate.conf` and `/etc/logrotate.d/`.
- Disk full with a giant log file? The tool that should have prevented it is `logrotate`. Force a run: `logrotate -f /etc/logrotate.conf`.

---

## 13. Time and Date

- Wrong time breaks SSL certificates, makes logs useless, and shifts cron schedules.
- `timedatectl` shows time, timezone, and NTP status. `timedatectl set-timezone UTC` changes the zone. `timedatectl set-ntp true` turns on sync (added). `timedatectl set-time` sets it manually (avoid on production).
- `date` shows the time. `date +%Y-%m-%d` formats it.
- NTP keeps clocks accurate. Common services: `chrony` (modern) and `ntp`. `chronyc tracking` shows drift (added). PTP is a more precise alternative (added).

---

## 14. Scheduling Tasks

### cron

```bash
crontab -e      # edit mine
crontab -l      # list mine
crontab -r      # remove ALL (careful)
sudo crontab -e # root's crontab
```

Five fields: **minute (0-59), hour (0-23), day of month (1-31), month (1-12), day of week (0-7, 0 and 7 are Sunday)**.

| Expression    | Meaning                          |
| ------------- | -------------------------------- |
| `0 2 * * *`   | Every day at 2:00 AM             |
| `*/5 * * * *` | Every 5 minutes                  |
| `0 0 * * 0`   | Every Sunday at midnight         |
| `0 0 * * 1`   | Midnight on Mondays              |
| `30 8 1 * *`  | 8:30 AM on the 1st of each month |

A syntax error means the job silently won't run. Verify with `crontab -l`.

### Other schedulers

- **systemd timers:** `systemctl list-timers`, `systemctl enable name.timer`. Service-based alternative to cron.
- **`at`** (added): one-time jobs, e.g. `echo "backup.sh" | at 2am`.
- **`anacron`** (added): runs missed jobs on machines that aren't always on.

---

## 15. Disk Quotas

Limit how much space a user or group can use.

- `quota -u user`: show a user's usage and limits
- `edquota -u user`: set limits
- `repquota -a`: report on everyone
- **Soft limit:** warning level, can be exceeded for a grace period. **Hard limit:** absolute, writes are blocked.
- Quotas need `usrquota`/`grpquota` mount options in `/etc/fstab` (added).

Example: 10 GB developer, soft 9 GB, hard 10 GB.

---

## Exam Gotchas (quick list)

**File system and boot**

- Parent of all directories: `/`. Root user's home: `/root`, not `/home/root`.
- Most user apps are in `/usr/bin`. Third-party software goes in `/opt`. Manual installs go in `/usr/local`.
- `/tmp` is wiped on reboot. `/proc` and `/sys` are virtual.
- Boot order: BIOS/UEFI → GRUB → initrd → kernel → systemd. systemd is PID 1.
- Don't edit `/boot/grub/grub.cfg` by hand. Edit `/etc/default/grub` and regenerate.

**Packages and services**

- `apt update` refreshes the list. `apt upgrade` installs updates.
- `remove` keeps config, `purge` removes it. `dpkg -i` doesn't resolve dependencies.
- Broken install: `apt --fix-broken install`. Unconfigured package: `dpkg --configure -a`.
- `start` = now, `enable` = boot. `mask` is stronger than `disable`.
- `restart` stops and starts, `reload` re-reads config.

**Shell and archives**

- `>` overwrites, `>>` appends. `&&` runs on success, `||` on failure. Exit code 0 = success.
- In `tar`, `f` goes right before the filename. `gzip` replaces the original unless `-k`.

**Storage**

- `umount`, not `unmount`. Use UUIDs in fstab and test with `mount -a`.
- `df` = drive space, `du` = folder size, `df -i` = inodes.
- `fsck` only on unmounted filesystems. XFS uses `xfs_repair`.
- After extending an LV, grow the filesystem. XFS can grow but not shrink.
- `modprobe` handles dependencies, `insmod` does not.
- RAID 0 has no redundancy.
- Hard link survives deleting the original, symlink breaks.

**Processes**

- `kill` = SIGTERM (15), `kill -9` = SIGKILL. Only root can lower a nice value below 0.
- `ps` is a snapshot, `top` is live.

---

## Self-Check Questions (cover the answers and try)

1. Where do config files live? Where do logs live? Where is the root user's home?
2. Name the boot steps in order, from firmware to target. What is PID 1?
3. Where do kernel parameters for GRUB get edited, and how do I regenerate the config?
4. What's the difference between `modprobe` and `insmod`?
5. What is the difference between `apt remove` and `apt purge`? What fixes an install that failed halfway?
6. What does `systemctl enable --now ssh` do? What's the difference between `mask` and `disable`?
7. What does `cmd1 && cmd2` do if `cmd1` fails?
8. Write the command to create a gzip tar archive of a folder, and the one to list its contents.
9. When would I use `rsync` instead of `cp`? What's dangerous about `dd`?
10. What are the six fields of an `/etc/fstab` line, and why use UUIDs?
11. How do I safely test an fstab change before rebooting?
12. What is the difference between `df` and `du`? What does `df -i` show?
13. Name the three LVM layers in order. After `lvextend`, what else must I do?
14. Which RAID level has no redundancy? Which survives two disk failures?
15. What is the difference between a hard link and a symbolic link?
16. What does the `nofail` mount option do? What about `noexec`?
17. What does `netplan try` do that `netplan apply` doesn't?
18. Which file sets the order of name lookups (files vs DNS)?
19. Which signal is `kill -9`, and why is it a last resort?
20. What does the cron expression `0 2 * * *` mean?
21. What is a zombie process?
22. Server stopped accepting connections and `/var/log` has a 50 GB file. What went wrong, and which tool prevents it?

---

## Key Takeaways

- Everything in Linux starts at `/`. Know the tree cold.
- `/etc` is where ALL config lives. If something is broken, check there first.
- Boot order never changes: BIOS/UEFI → GRUB → initrd → kernel → systemd.
- systemd is always PID 1. Nothing starts before it.
- `apt` installs software, `dpkg` is what `apt` uses underneath.
- `systemctl enable` survives reboot. `systemctl start` is for now.
- When in doubt about any command: `man <command>`.

---

_CompTIA Linux+ XK0-006 | Week 1 Master Notes | DevRehannaLP_

∞ ☬ DevRehannaLP ☬ | DevSecOps ∞
