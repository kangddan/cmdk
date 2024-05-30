from importlib import reload
import cmdk.dg.depNode as depNode



def reloadIt():
    reload(depNode)



    print('-------------------- DG RELOAD : OK')