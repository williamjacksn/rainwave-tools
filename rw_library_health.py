#!/usr/bin/env python3

import subprocess

missing_art = subprocess.check_output(['missing_art'])

print(repr(missing_art))
