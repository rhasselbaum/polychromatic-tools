#!/usr/bin/env python3

"""Applies a Razer keyboard Polychromatic effect once and any time the keyboard is plugged in.

The process blocks until SIGINT or SIGTERM. While running, it monitors DBus device add events for Razer.
"""


import dbus
import subprocess
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import sys


def main():
    if len(sys.argv) < 2:
        sys.exit(f"Usage {sys.argv[0]} <effect-file.json>")

    cmd = ["polychromatic-cli", "-d", "keyboard", "-e", sys.argv[1]]
    print(f"Started. Running: {cmd}")
    subprocess.run(cmd)

    # Adapted from https://github.com/polychromatic/polychromatic/issues/186#issuecomment-437706484
    DBusGMainLoop(set_as_default=True)
    session_bus = dbus.SessionBus()

    def device_changed(sender=None):
        print(f"Device plugged in. Running: {cmd}")
        subprocess.run(cmd)

    proxy = session_bus.get_object("org.razer", "/org/razer")

    proxy.connect_to_signal("device_added", device_changed)
    # There is also 'device_removed'

    try:
        loop = GLib.MainLoop()
        loop.run()
    except KeyboardInterrupt:
        print("Bye.")
        sys.exit(0)


if __name__ == "__main__":
    main()
