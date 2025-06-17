#!/usr/bin/env python3
import os
os.environ.setdefault("QT_QPA_PLATFORM", "xcb")  # fallback if Wayland fails

from psswd_box.app import main

if __name__ == "__main__":
    main()
