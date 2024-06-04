from typing import Union
import maya.cmds as cmds
from cmdk.dg.omUtils import isDagNode
from cmdk.dg.depNode import DepNode
from cmdk.dag.dagNode import DagNode



def createDagNode(typ: str, name: str) -> DagNode:
    return DagNode(name, typ)
    
def createDepNode(typ: str, name: str) -> DepNode:
    return DepNode(name, typ)
    
def kNode(name: Union[str, tuple, list]) -> DepNode | DagNode:
    if isinstance(name, str):
        if not cmds.objExists(name):
            raise ValueError('The specified object does not exist: {}'.format(name))
        return DagNode(name) if isDagNode(name) else DepNode(name)
    
    elif isinstance(name, (tuple, list)):
        if not all(cmds.objExists(_n) for _n in name):
            raise ValueError('Contains one or more invalid objects: {}'.format(name))
        return [DagNode(_n) if isDagNode(_n) else DepNode(_n) for _n in name]
    else:
         raise ValueError('Invalid input type: {}. Expected str, tuple, or list.'.format(type(name).__name__))

        
