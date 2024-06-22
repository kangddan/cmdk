import maya.cmds as cmds
import maya.api.OpenMaya as om2
import cmdk.dg.omUtils as omUtils
from cmdk.attr.get import GetAttribute

        
class Attribute(object):
    
    def __new__(cls, *args, **kwargs) -> 'self':
        node, attr = args
        attrName = '{}.{}'.format(node.fullPath, attr)
        if not cmds.objExists(attrName):
            raise AttributeError('The node {} does not have this attribute: {}'.format(node.name, attr))
            
        return super().__new__(cls) 
        
    def __init__(self, node, attr):
        self._node = node
        self._attr = attr

    def __getattr__(self, attr):
        return self.__dict__.get(attr, Attribute(self._node, '{0}.{1}'.format(self._attr, attr)))
        
    def __getitem__(self, index):
        return Attribute(self._node, '{0}[{1}]'.format(self._attr, index))
        
    def __setitem__(self, index, value):
        self.__getitem__(index).set(value)
            
    def __repr__(self):
        return '<{}.{}>'.format('Attribute', self.fullPath)
    
    def __str__(self):
        return self.fullPath
        
    def __lshift__(self, other):
        other.connect(self)
        
    def __rshift__(self, other):
        self.connect(other)
    # ---------------------------------------------------------------------
    @property
    def nodeName(self):
        return self._node.name
        
    @property
    def nodeFullPathName(self):
        return self._node.fullPath
        
    @property
    def type(self) -> str:
        return cmds.getAttr(self.fullPath, typ=True)
    @property
    def path(self) -> str:
        return self.fullPath.split("|")[-1]
    @property    
    def fullPath(self) -> str:
        return '{}.{}'.format(self.nodeFullPathName, self._attr)
    @property
    def name(self) -> str:
        return '{}.{}'.format(self.nodeName, self._attr)
    
    def get(self, *args, **kwargs):
        return GetAttribute(self.nodeFullPathName, self._attr).run(*args, **kwargs)
  
               
    def set(self, *args, **kwargs):
        attrLockState = self.isLocked
        if attrLockState: self.lock(False)
        # -----------------------------------------------------
        try:
            cmds.setAttr(self.fullPath, *args, **kwargs)
        except:
            om2.MGlobal.displayWarning('Parameter Error')
            
        finally:
            # -----------------------------------------------------
            self.lock(attrLockState)
            return self
        
        
    # -----------------------------------------------------------------

    def connect(self, other):
        if not isinstance(other, self.__class__):
            return 
            
        if cmds.isConnected(self.fullPath, other.fullPath): # already connected
            return self
            
        try:
            cmds.connectAttr(self.fullPath, other.fullPath, f=True)
            return self
        except:
            om2.MGlobal.displayWarning('Attributes cannot be connected. ' +
            'Please check the attribute types and connection order: \noutput: {}\ninput:  {}'.format(
                                           self.type, other.type))
                
    def disconnect(self, inputConnect=True):
        
        connections = cmds.listConnections(self.fullPath, s=True, p=True) or []
        if not connections:
            return 
        
        for attr in connections:
            src, dst = (self.fullPath, attr) if inputConnect else (attr, self.fullPath)
            if cmds.isConnected(src, dst):
                cmds.disconnectAttr(src, dst)
        #return self
   
    # -----------------------------------------------------------------   
    @property
    def parent(self):
        return [self._node[subAttr] for subAttr in self.query(listParent=True) or []]
    @property    
    def children(self):
        return [self._node[subAttr] for subAttr in self.query(listChildren=True) or []]
        
    @property
    def isParent(self) -> bool:
        return bool(self.parent)
        
    @property
    def isChildren(self) -> bool:
        return bool(self.children)
          
    # -----------------------------------------------------------------   
    @property
    def has(self) -> bool:
        return cmds.objExists(self.fullPath)
        
    def query(self, **kwargs):
        '''
        attributeQuery cannot query attributes with indices, 
        '''
        _attrName = self._attr.split('.')[-1].split('[')[0]
        return cmds.attributeQuery(_attrName, node=self.nodeFullPathName, **kwargs)
        
    def delete(self):
        self.lock(False)
        try:
            cmds.deleteAttr(self.fullPath)
        except:
            return om2.MGlobal.displayWarning('Unable to delete default attribute')
            
    def lock(self, state=True) -> 'self':
        cmds.setAttr(self.fullPath, lock=state)
        return self
        
    @property
    def isLocked(self) -> bool:
        return cmds.getAttr(self.fullPath, lock=True)
        
    def rename(self, newName: str) -> 'self':
        attrLockState = self.isLocked
        self.lock(False) if attrLockState else None
        
        try:
            cmds.renameAttr(self.fullPath, newName)
            return Attribute(self._node, newName).lock(attrLockState)
        except:
            om2.MGlobal.displayWarning('Cannot modify the default attribute names of the object')
            self.lock(attrLockState)
            return self    
            
    def connections(self, **kwargs):
        nodes = cmds.listConnections(self.fullPath, scn=True, **kwargs) or []
        if not nodes:
            return 
        
        # -------------------------------------------------------------------
        from cmdk.dg.depNode import DepNode
        from cmdk.dag.dagNode import DagNode
        
        if any(key in kwargs and kwargs[key] for key in ['plugs', 'p']):
            # return [Attribute(nodeName=DepNode(node.split('.')[0]), '.'.join(node.split('.')[1:])) for node in nodes]
            return [DepNode(nodeName=node.split('.')[0])['.'.join(node.split('.')[1:])] for node in nodes]
        else:
            return [DagNode(nodeName=node) if omUtils.isDagNode(node) else DepNode(nodeName=node) for node in nodes]
            
    
    # ------------------------------------------------------------------------
    def __call__(self, *args, **kwargs):
        return self.get(*args, **kwargs)
    
    def __invert__(self):
        self.disconnect(True)
        self.disconnect(False)
            
