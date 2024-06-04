from importlib import reload
import cmdk.dag.dagNode as dagNode



def reloadIt():
    reload(dagNode)



    print('-------------------- DAG RELOAD : OK')