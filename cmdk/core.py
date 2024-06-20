from typing import Union
import maya.cmds as cmds
from cmdk.dg.omUtils import isDagNode
from cmdk.dg.depNode import DepNode
from cmdk.dag.dagNode import DagNode
from cmdk.attr.kVector import KVector
from cmdk.attr.kMatrix import KMatrix

def vector(x=0, y=0, z=0):
    return KVector(x, y, z)
    
def matrix(v1=KVector(1, 0, 0), v2=KVector(0, 1, 0), v3=KVector(0, 0, 1), off=KVector(0, 0, 0)):
    return KMatrix(v1, v2, v3, off)

def createDagNode(typ: str, name :str = '') -> DagNode:
    return DagNode(typ, name)
    
def createDepNode(typ: str, name :str = '') -> DepNode:
    return DepNode(typ, name)
    
def kNode(name: Union[str, tuple, list]) -> DepNode | DagNode:
    if isinstance(name, str):
        if not cmds.objExists(name):
            raise ValueError('The specified object does not exist: {}'.format(name))
        return DagNode('', name) if isDagNode(name) else DepNode('', name)
    
    elif isinstance(name, (tuple, list)):
        if not all(cmds.objExists(_n) for _n in name):
            raise ValueError('Contains one or more invalid objects: {}'.format(name))
        return [DagNode('', _n) if isDagNode(_n) else DepNode('', _n) for _n in name]
    else:
         raise ValueError('Invalid input type: {}. Expected str, tuple, or list.'.format(type(name).__name__))

def getCache() -> dict:
    return DepNode.getCache()
    
def clearCache() -> None:
    return DepNode.clearCache()
    
def removeFromCache(uuid: str) -> None:
    return DepNode.removeFromCache(uuid)