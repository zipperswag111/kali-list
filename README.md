# kali-list

`kali-list` is a compact command-line catalog for the APT packages configured on a Kali Linux machine. It focuses on package names, sections, versions, and executable commands rather than lengthy package documentation.

## Commands

```bash
# Browse all available packages, grouped by Debian section
kali-list packages

# Find available packages without package descriptions
kali-list packages --search wireless
kali-list packages --section net

# List executable commands supplied by installed packages
kali-list commands
kali-list commands --search nmap

# Show package metadata and installed executable commands
kali-list info nmap
```

The `packages` command reads the local APT cache, so run `sudo apt update` when you want it refreshed. `commands` intentionally reports commands from installed packages: Debian repository metadata does not consistently provide a command-to-package index, and guessing would be misleading.

## Install locally

```bash
sudo apt install python3
python3 -m pip install .
```

Or build the Debian package:

```bash
sudo apt install build-essential debhelper-compat python3-all
dpkg-buildpackage -us -uc
sudo apt install ../kali-list_1.0.0_all.deb
```

## License

MIT. See [LICENSE](LICENSE).
