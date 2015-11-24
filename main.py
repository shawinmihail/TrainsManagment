# -*- coding: utf-8 -*-
from archive import schemes

scheme = schemes.scheme1()
for i in range(30):
    scheme.tick(1)


# TODO forbid the same name for RailwayObjects?
# TODO forbid the same train route?
