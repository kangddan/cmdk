from cmdk.dag.dagNode import DagNode
from cmdk.dg.depNode import DepNode
from cmdk.dg.omUtils import isDagNode

def createDagNode(typ, name):
    return DagNode(name, typ)
    
def createDepNode(typ, name):
    return DepNode(name, typ)
    
def kNode(name):
    return DagNode(name) if isDagNode(name) else DepNode(name)
