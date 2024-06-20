import maya.cmds as cmds
import maya.api.OpenMaya as om2


def toMObject(nodeName: str) -> om2.MObject:
    '''
    create mobject
    '''
    return om2.MGlobal.getSelectionListByName(nodeName).getDependNode(0)

def toDependencyNode(nodeName: str) -> om2.MFnDependencyNode:
    '''
    Convert a node ito an OpenMaya Dependency Node
    '''
    return om2.MFnDependencyNode(toMObject(nodeName)) 

def toMDagPath(nodeName: str) -> om2.MDagPath | None:
    ''' 
    Convert a node ito an OpenMaya Dag Node
    '''
    return om2.MDagPath.getAPathTo(toMObject(nodeName)) 
    

def toMDagPathOrDepNode(node: str | om2.MObject) -> om2.MDagPath | om2.MFnDependencyNode:
    '''
    create dagNode or dgNode
    '''
    mobj = toMObject(node) if isinstance(node, str) else node
    return om2.MDagPath.getAPathTo(mobj) if mobj.hasFn(om2.MFn.kDagNode) else om2.MFnDependencyNode(mobj)
        
def getUUID(nodeName: str) -> str | None:
    '''
    Get UUID value as string
    '''
    try:
        return toDependencyNode(nodeName).uuid().asString()
    except:
        return None

def getNodeNameFromUUID(uuid: str) -> str | None:
    '''
    uuid to node name
    '''
    try:
        return cmds.ls(uuid)[0]
    except:
        return None
    
def UUIDExists(uuid: str | om2.MUuid) -> bool:
    '''
    Check if a given UUID string or MUuid object is valid
    '''
    if isinstance(uuid, str):
        return om2.MUuid(uuid).valid()
    elif isinstance(uuid, om2.MUuid):
        return uuid.valid()
    return False

# ---------------------------------------
def isStr(value):
    return isinstance(value, str) and len(value) > 0
    
def createNode(nodeType, nodeName):
    nodeArgs = {'n': nodeName} if isStr(nodeName) else {}
    
    if nodeType == 'locator':
        return cmds.spaceLocator(**nodeArgs)[0]
    return cmds.createNode(nodeType, **nodeArgs)
    

def isDagNode(nodeName: str) -> bool:
    if toMObject(nodeName).hasFn(om2.MFn.kDagNode):
        return True
    return False

        

        

        

