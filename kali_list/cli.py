"""Compact browsing of APT packages and installed executable commands."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Package:
    name: str
    version: str
    section: str


def run(*args: str) -> str:
    """Run a read-only system query and return standard output."""
    try:
        return subprocess.check_output(args, text=True, stderr=subprocess.DEVNULL)
    except (OSError, subprocess.CalledProcessError):
        return ""


def available_packages() -> list[Package]:
    """Read package data from APT's local cache with no network calls."""
    data = run("apt-cache", "dumpavail")
    packages: dict[str, Package] = {}
    for paragraph in data.split("\n\n"):
        fields: dict[str, str] = {}
        for line in paragraph.splitlines():
            if ":" in line and not line.startswith((" ", "\t")):
                key, value = line.split(":", 1)
                fields[key] = value.strip()
        name = fields.get("Package")
        if name:
            packages[name] = Package(name, fields.get("Version", "?"), fields.get("Section", "other"))
    return sorted(packages.values(), key=lambda item: (item.section, item.name))


def installed_commands() -> Iterable[tuple[str, str]]:
    """Yield (command, package) pairs for executable files on the current system."""
    seen: set[tuple[str, str]] = set()
    info_dir = Path("/var/lib/dpkg/info")
    for list_file in info_dir.glob("*.list"):
        # Debian records one .list file per installed binary package. Reading
        # these files avoids launching dpkg once for every installed package.
        package = list_file.name.removesuffix(".list")
        for filename in list_file.read_text(errors="replace").splitlines():
            path = Path(filename)
            if path.parent not in (Path("/bin"), Path("/sbin"), Path("/usr/bin"), Path("/usr/sbin")):
                continue
            if not os.access(filename, os.X_OK):
                continue
            entry = (path.name, package)
            if entry not in seen:
                seen.add(entry)
                yield entry


def matches(value: str, search: str | None) -> bool:
    return not search or search.lower() in value.lower()


def print_packages(args: argparse.Namespace) -> int:
    records = [p for p in available_packages() if matches(p.name, args.search)]
    if args.section:
        records = [p for p in records if p.section.lower() == args.section.lower()]
    if not records:
        print("No matching packages found. Run sudo apt update if the local APT cache is empty.", file=sys.stderr)
        return 1
    grouped: dict[str, list[Package]] = defaultdict(list)
    for record in records:
        grouped[record.section].append(record)
    shown = 0
    for section, items in grouped.items():
        print(f"\n[{section}]")
        for item in items:
            print(f"  {item.name:<42} {item.version}")
            shown += 1
            if args.limit and shown >= args.limit:
                print(f"\nShowing first {args.limit} packages. Use --limit 0 for all.")
                return 0
    print(f"\n{shown} package(s)")
    return 0


def print_commands(args: argparse.Namespace) -> int:
    records = sorted((command, package) for command, package in installed_commands() if matches(command, args.search))
    if not records:
        print("No matching installed commands found.", file=sys.stderr)
        return 1
    for command, package in records:
        print(f"{command:<36} {package}")
    print(f"\n{len(records)} command(s) from installed packages")
    return 0


def print_info(args: argparse.Namespace) -> int:
    package = next((p for p in available_packages() if p.name == args.package), None)
    if package is None:
        print(f"Package not found: {args.package}", file=sys.stderr)
        return 1
    print(f"Package: {package.name}\nVersion: {package.version}\nSection: {package.section}")
    commands = sorted(command for command, owner in installed_commands() if owner.split(":", 1)[0] == package.name)
    if commands:
        print("Commands:\n  " + "\n  ".join(commands))
    else:
        print("Commands: package is not installed, or it has no standard executable commands.")
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="kali-list", description="Browse APT packages and installed commands without long descriptions.")
    subcommands = root.add_subparsers(dest="action", required=True)
    packages = subcommands.add_parser("packages", help="list packages from the local APT cache")
    packages.add_argument("--search", metavar="TEXT", help="filter by package name")
    packages.add_argument("--section", metavar="SECTION", help="filter by Debian section")
    packages.add_argument("--limit", type=int, default=100, help="maximum results (0 means all; default: 100)")
    packages.set_defaults(handler=print_packages)
    commands = subcommands.add_parser("commands", help="list executable commands from installed packages")
    commands.add_argument("--search", metavar="TEXT", help="filter by command name")
    commands.set_defaults(handler=print_commands)
    info = subcommands.add_parser("info", help="show a package and its installed commands")
    info.add_argument("package")
    info.set_defaults(handler=print_info)
    return root


def main() -> int:
    args = parser().parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
