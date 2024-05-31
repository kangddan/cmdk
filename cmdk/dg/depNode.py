import maya.cmds as cmds
import maya.api.OpenMaya as om2
import cmdk.dg.omUtils as omUtils
#from cmdk.attr.attribute import Attribute
from cmdk.attr.attribute import Attr

class DepNode(object):
    _NODETYPE = cmds.allNodeTypes()
    _CACHE    = {}
    
    def __new__(cls, *args, **kwargs) -> 'self':
        nodeName = args[0] if len(args) > 0 else kwargs.get('nodeName')
        if not isinstance(nodeName, str):
            raise ValueError('The nodeName must be a string')
        
        nodeType = args[1] if len(args) > 1 else kwargs.get('nodeType')
        if nodeType and nodeType not in cls._NODETYPE:
            raise ValueError('NodeType error')
        
        if nodeType is None:
            uuid = omUtils.getUUID(nodeName)
            if omUtils.UUIDExists(uuid) and uuid in cls._CACHE:
                return cls._CACHE[uuid]

        return super(DepNode, cls).__new__(cls)
            
    
    def __init__(self, nodeName :str = '', nodeType :str = ''):
        if not hasattr(self, '_initOk_'):
            #self.__dict__['_IS_INITIALIZED_'] = False 
            
            self.node = nodeName
            if not self.exists() and nodeType:
                self._create(nodeType)
            
            if self._apiNode:
                self._instanceUUID = self.uuid
                '''
                Add to cache dict to help implement the singleton pattern
                '''
                DepNode._CACHE[self.uuid] = self
            self._initOk_ = True
            
            #self.__dict__['_IS_INITIALIZED_'] = True 

    
    def __repr__(self) -> str:
        try:
            return "<{0} {1} '{2}'>".format(self.__class__.__name__, self.type, 
                                     omUtils.getNodeNameFromUUID(self._instanceUUID))
        except Exception:
            '''
            Once I add error handling, unexpected situations may occur!!
            For example, when deleting an object, running the repr method on the instance will trigger an error.
            if I undo the operation and run repr again, everything returns to normal
            '''
            return 'Invalid Object'
            
    def __str__(self) -> str:
        fullPath = self.fullPath
        if not fullPath:
            return om2.MGlobal.displayWarning('INVALID OBJECT')
        return fullPath
        # try:
        #     return omUtils.getNodeNameFromUUID(self._instanceUUID)
        # except:
        #     return 'Invalid Object'
            
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.fullPath == other.fullPath
        elif self.fullPath == other:
            return True
        elif self.path == other:
            return True
        else:
            return False
    
    @property
    def node(self) -> str:
        return self._node
        
    @node.setter
    def node(self, nodeName: str):
        self._apiNode = False
        self._node = nodeName
        
        if self._node and cmds.objExists(self._node):
            self._apiNode = omUtils.toMDagPathOrDepNode(self._node)
    
    def _create(self, nodeType: str):
        self.node = omUtils.createNode(nodeType, self.node)
        return self
        
    @property
    def apiNode(self) -> om2.MFnDependencyNode:
        if self._apiNode is None and omUtils.UUIDExists(self._instanceUUID):
            nodeName = omUtils.getNodeNameFromUUID(self._instanceUUID)
            self._apiNode = omUtils.toMDagPathOrDepNode(nodeName)
                
        return self._apiNode
        
    def exists(self) -> bool:
        if self.fullPath and cmds.objExists(self.fullPath):
            return True
        return False
        
    # -----------------------------------------------------------
    @property
    def attr(self):
        return Attr(self)
    
    """
    def __getattr__(self, attr):
        if attr == '_initOk_':
            raise AttributeError
        return self.__dict__.get(attr, Attribute(self, attr))

    def __setattr__(self, attr, value):
        '''
        Note: Do not use self.__dict__.get(attr) is None to check if an attribute is an instance attribute,
        because calling get will trigger the __getattr__ method again, causing infinite recursion !!!
        '''
        if self._IS_INITIALIZED_ and attr not in self.__dict__:
            getattr(self, attr).set(value)
        else:
            object.__setattr__(self, attr, value)
            
    def __getitem__(self, attr):
        return self.__getattr__(attr)


    def __setitem__(self, attr, value):
        self.__setattr__(attr, value)
    """
    
    # -----------------------------------------------------------
    @property
    def path(self) -> str | None:
        return (None 
                if self.fullPath is None 
                else 
                self.fullPath.split("|")[-1])
                
    @property
    def fullPath(self) -> str | None:
        if self.apiNode:
            return (self._apiNode.fullPathName() 
                    if isinstance(self._apiNode, om2.MDagPath) 
                    else self._apiNode.name())        
        return None
        
    @property
    def name(self) -> str | None:
        return self.fullPath.split("|")[-1].split(':')[-1]
        
    @property
    def namespace(self) -> str | None:
        return self.fullPath.split("|")[-1].rpartition(':')[0]
    
    @property
    def type(self) -> str:
        try:
            return cmds.objectType(self.fullPath)
        except:
            return 'No Type'
    
    @property    
    def uuid(self) -> str:
        return omUtils.getUUID(self.fullPath)
        
    def rename(self, newName: str) -> 'self':
        cmds.rename(self.fullPath, newName)
        return self
        
    def lock(self, state=True) -> 'self':
        cmds.lockNode(self.fullPath, lock=state)
        return self
        
    def select(self, **kwargs) -> 'self':
        cmds.select(self.fullPath, **kwargs)
        return self
    
    @property
    def isLocked(self) -> bool:
        return cmds.lockNode(self.fullPath, query=True, lock=True)[0]
        
    def delete(self):
        cmds.delete(self.fullPath)
        self._apiNode = None 
        
    # -------------------------------------------------------------------------------------------
    """
    def listAttr(self, **kwargs):
        return [Attribute(self, attr) for attr in cmds.listAttr(self.fullPath, **kwargs) or []]
                
    def addAttr(self, attrName='', **kwargs):
        '''
        add attr / longName: str
        attributeType: str / dataType: str
        '''
        cmds.addAttr(self.fullPath, ln=attrName, **kwargs)
        return Attribute(self, attrName)

        
    def allConnections(self, **kwargs) -> list['self'] | None:
        from cmdk.dag.dagNode import DagNode
        '''
        Why use snc=True? 
        This will avoid returning unitConversion nodes
        as calling the delete() method will automatically delete them
        '''
        nodes = cmds.listConnections(self.fullPath, scn=True, **kwargs) or []
        if not nodes: return
        return [DagNode(node) if omUtils.isDagNode(node) else DepNode(node) for node in nodes]
    """

if __name__ == '__main__':
    testNode = DepNode('testNode', 'joint')
    testNode.attr
    #testNode.attr.tx = 15
    









 



        












        
