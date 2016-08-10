#!/usr/bin/env python
# description: not implemented
# version: 0.1
# targets: ["pre-applypatch"]
# helpers: []

import sys

def pre_applypatch_common(argv):
   return 0
         
if __name__ == "__main__":
   pre_applypatch_common(sys.argv[1:])

