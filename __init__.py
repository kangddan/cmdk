import maya.cmds as cmds
from cmdk.dg.omUtils import isDagNode
from cmdk.dg.depNode import DepNode
from cmdk.dag.dagNode import DagNode



def createDagNode(typ, name):
    return DagNode(name, typ)
    
def createDepNode(typ, name):
    return DepNode(name, typ)
    
def kNode(name):
    if not cmds.objExists(name):
        raise ValueError('Invalid Object')
    return DagNode(name) if isDagNode(name) else DepNode(name)
    
