# Publish `kali-list` to Kali

The repository and maintainer metadata are set for the initial public release.

## Release checklist

1. Create a public Git repository named `kali-list` and push this source.
2. Create and push the release tag `v1.0.0`.
3. Build and test on Kali:

   ```bash
   sudo apt update
   sudo apt install build-essential debhelper-compat dh-python python3-all python3-setuptools
   dpkg-buildpackage -us -uc
   sudo apt install ../kali-list_1.0.0-1_all.deb
   kali-list packages --search nmap
   kali-list commands --search nmap
   ```

4. Search Kali's bug tracker for an existing request before filing a new one.
5. Submit a **New Tool Requests** issue at https://bugs.kali.org with
   reproducibility **N/A**, severity **minor**, and priority **normal**.

## Ready-to-edit issue text

**Summary:** `[New Tool] kali-list — compact Kali package and command catalog`

```text
Name: kali-list
Version: 1.0.0
Homepage: https://github.com/zipperswag111/kali-list
Download: https://github.com/zipperswag111/kali-list/archive/refs/tags/v1.0.0.tar.gz
Author: kali-list contributors
Licence: MIT

Description:
kali-list is a compact terminal catalog for the APT packages configured on a
Kali Linux system. It lists package names, sections, versions, and executable
commands without emitting long package descriptions. It is intentionally a
local metadata browser: package information comes from the APT cache and
installed command information comes from dpkg file lists. It makes no network
calls and performs no system modifications.

Dependencies:
python3 (>= 3.9), apt, dpkg.

Similar tools:
apt-cache, apt list, apt-file, dpkg-query, and kali-menu. Unlike these,
kali-list provides one compact, searchable listing focused on package names
and installed executable commands, organized by Debian section.

Activity:
Project started November 4, 2026. Initial release is 1.0.0; maintenance will
track Kali and Debian packaging requirements.

How to install:
sudo apt update
sudo apt install build-essential debhelper-compat dh-python python3-all python3-setuptools
dpkg-buildpackage -us -uc
sudo apt install ../kali-list_1.0.0-1_all.deb

Debian packaging:
Included. The source contains a debian/ directory using debhelper compat 13
and pybuild.
```

Kali's official guidance requires Debian packaging and asks submitters to
provide the license, dependencies, similar tools, development activity, and
installation details. A request is reviewed; creating this source package does
not itself add the command to Kali's repository.
