#!/usr/bin/env python3
import os
import sys

# Ensure Python can find the bundled app code
sys.path.insert(0, os.path.join(os.environ["SNAP"], "lib"))

os.environ.setdefault("QT_QPA_PLATFORM", "xcb")  # fallback to X11 if Wayland fails

from psswd_box.app import main

if __name__ == "__main__":
    main()
