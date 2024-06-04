# -*- coding: utf-8 -*-
from importlib import reload

import cmdk.attr.attribute as attribute
import cmdk.attr.attrUtils as attrUtils
import cmdk.attr.get as get

import cmdk.attr.kVector as kVector
import cmdk.attr.kMatrix as kMatrix
import cmdk.attr.KQuaternion as KQuaternion






def reloadIt():
    reload(attribute)
    reload(attrUtils)
    reload(get)
    reload(kVector)
    reload(kMatrix)
    reload(KQuaternion)



    print('-------------------- ATTR RELOAD : OK')