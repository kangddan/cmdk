from importlib import reload

import cmdk.attr.reloadAttr as reloadAttr
import cmdk.dag.reloadDag   as reloadDag
import cmdk.dg.reloadDg     as reloadDg

import cmdk.__init__        as __init__
import cmdk.core            as core


def reloadIt():
    
    reload(reloadAttr)
    reload(reloadDg)
    reload(reloadDag)
    

    reloadAttr.reloadIt()
    reloadDg.reloadIt()
    reloadDag.reloadIt()
    reload(__init__)
    reload(core)

    print('-------------------- ALL RELOAD : OK')
    
if __name__ == '__main__':
    reloadIt()
    
