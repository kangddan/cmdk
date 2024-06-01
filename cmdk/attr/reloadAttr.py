# -*- coding: utf-8 -*-
from importlib import reload
import cmdk.attr.attribute as attribute
import cmdk.attr.get as get



def reloadIt():
    reload(attribute)
    reload(get)



    print('-------------------- ATTR RELOAD : OK')