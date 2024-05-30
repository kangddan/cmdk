from importlib import reload

import cmdk.attr.reloadAttr as reloadAttr
import cmdk.dag.reloadDag   as reloadDag
import cmdk.dg.reloadDg     as reloadDg


def reloadIt():
    
    reload(reloadAttr)
    reload(reloadDag)
    reload(reloadDg)

    reloadAttr.reloadIt()
    reloadDag.reloadIt()
    reloadDg.reloadIt()

    print('-------------------- ALL RELOAD : OK')
    
if __name__ == '__main__':
    reloadIt()
    
