from importlib import reload
import cmdk.dg.depNode as depNode
import cmdk.dg.omUtils as omUtils



def reloadIt():
    reload(depNode)
    reload(omUtils)



    print('-------------------- DG RELOAD : OK')