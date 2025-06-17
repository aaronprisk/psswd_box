#!/usr/bin/env python3
import sys
import os
print("QT_PLUGIN_PATH:", os.environ.get("QT_PLUGIN_PATH"))
print("LD_LIBRARY_PATH:", os.environ.get("LD_LIBRARY_PATH"))

sys.path.insert(0, "/snap/psswd-box/current/lib")

from psswd_box.app import main

if __name__ == "__main__":
    main()

