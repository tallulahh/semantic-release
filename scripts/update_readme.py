#!/usr/bin/env python3
import os
import sys

with open("README.md", "r") as f:
    readme = f.read()
    
with open("README.md", "w") as f:
    readme = f.write("Test update to readme")