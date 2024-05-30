# -*- coding: utf-8 -*-
from importlib import reload
import cmdk.attr.attribute as attribute



def reloadIt():
    reload(attribute)



    print('-------------------- ATTR RELOAD : OK')