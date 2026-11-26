# Current Toolkit and Skills

- **Git/SSH Workflow:**
  - WSL uses a dedicated SSH key to avoid conflicting with VMware: `~/.ssh/id_ed25519_wsl`
  - GitHub SSH mapping is stored in `~/.ssh/config`:

    ```text
    Host github.com
      IdentityFile ~/.ssh/id_ed25519_wsl
      IdentitiesOnly yes
    ```

  - Test authentication with: `ssh -T git@github.com`
