import maya.cmds as cmds
import maya.api.OpenMaya as om2
import cmdk.dg.omUtils as omUtils
from cmdk.attr.get import GetAttribute

        
class Attribute(object):
    def __init__(self, node, attr):
        self.node = node
        self.attr = attr
    
    # --------------------------------------------------------------------
    
    def __getattr__(self, attr):
        return self.__dict__.get(attr, Attribute(self.node, '{0}.{1}'.format(self.attr, attr)))
        
    def __getitem__(self, index):
        return Attribute(self.node, '{0}[{1}]'.format(self.attr, index))
        
    def __setitem__(self, index, value):
        self.__getitem__(index).set(value)
            
    def __repr__(self):
        return '<{}.{}>'.format(Attribute, self.fullPath)
    
    def __str__(self):
        return self.fullPath
        
    def __lshift__(self, other):
        other.connect(self)
        
    def __rshift__(self, other):
        self.connect(other)
    
    def __call__(self, *args, **kwargs):
        return self.get(*args, **kwargs)
    # ---------------------------------------------------------------------
    @property
    def type(self) -> str:
        return cmds.getAttr(self.fullPath, typ=True)
    @property
    def path(self) -> str:
        return self.fullPath.split("|")[-1]
    @property    
    def fullPath(self) -> str:
        return '{}.{}'.format(self.node.fullPath, self.attr)
    @property
    def name(self) -> str:
        return '{}.{}'.format(self.node.name, self.attr)
        
    
    def get(self, *args, **kwargs):
        
        if not self.exists(): 
            return om2.MGlobal.displayError('Invalid Attribute: {}'.format(self.fullPath))
        
        return GetAttribute(self.node.fullPath, self.attr).run()
        """
        # message -----------------------------------------------------------------
        if Attribute.isMessage(self.attr, self.node.fullPath):
            from cmdk.dg.depNode import DepNode
            from cmdk.dag.dagNode import DagNode
            
            if Attribute.isMessage(self.attr, self.node.fullPath, multi=True): # is multi attr
                nodes = cmds.listConnections(self.fullPath) or []
                return [DagNode(node) if omUtils.isDagNode(node) else DepNode(node) for node in nodes]
                
            # ---------------------------------------------------    
            # nodes = cmds.listConnections(self.fullPath, s=False)     # input message
            # if nodes is None: 
            #     nodes = cmds.listConnections(self.fullPath, d=False) # output message
            #     if nodes is None: 
            #         return
            nodes = cmds.listConnections(self.fullPath, s=False) or cmds.listConnections(self.fullPath, d=False)
            if not nodes:
                return
            return DagNode(nodes[0]) if omUtils.isDagNode(nodes[0]) else DepNode(nodes[0])
        # message -----------------------------------------------------------------
        
        '''
        Determine if the attr is a multi attr and return the current index length of the multi attr
        Although it's a bit strange, it works :)
        '''
        length = cmds.getAttr(self.fullPath, s=True)
        isMulti = self.query(m=True)
        
        if isMulti and length == 0:
            return
        
        elif not isMulti and length == 1:
            value = cmds.getAttr(self.fullPath, *args, **kwargs)
            return value
            
            '''
            node.attr[0].get() -> node.attr.get()
            Note that self.query() has converted the indexed attr into a multi-attr at this moment, 
            making isMulti == True. Therefore, the attr we are querying at this time is the indexed attr !
            '''
        elif isMulti and length == 1:  
            try:
                value = cmds.getAttr(self.fullPath, *args, **kwargs)
            except:
                '''
                Note the compound attributes of the plusMinusAverage node. 
                We might need to add a try block to make it work correctly
                
                input3D
                --input3D[0]
                ----input3Dx
                '''
                #value = cmds.getAttr('{0}[{1}]'.format(self.fullPath, 0), *args, **kwargs)
                value = cmds.getAttr(self.fullPath, *args, **kwargs)
            return value
            
        elif isMulti and length >= 2:
            values = [cmds.getAttr('{0}[{1}]'.format(self.fullPath, index), *args, **kwargs) for index in range(length)]
            return values
            
        '''
        try:
            value = cmds.getAttr(self.fullPath, *args, **kwargs)
            return value
        except:
            values = [cmds.getAttr('{0}[{1}]'.format(self.fullPath, index), *args, **kwargs) for index in range(length)]
            return values[0] if len(values) == 1 else values
        '''
        """
               
    def set(self, *args, **kwargs):
        if not self.exists(): 
            return om2.MGlobal.displayWarning('Invalid Attribute: {}'.format(self.fullPath))
        attrLockState = self.isLocked
        self.lock(False) if attrLockState else None
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
        
        if not (self.exists() and other.exists()):
            invalidAttr = self.fullPath if not self.exists() else other.fullPath
            return om2.MGlobal.displayWarning('Invalid Attribute: {}'.format(invalidAttr))
            
        if cmds.isConnected(self.fullPath, other.fullPath): # already connected
            return self
        else:
            try:
                cmds.connectAttr(self.fullPath, other.fullPath, f=True)
                return self
            except:
                om2.MGlobal.displayWarning('Attribute Type Error')
                
    def disconnect(self):
        pass
            
    # -----------------------------------------------------------------    
    def exists(self):
        return True if cmds.objExists(self.fullPath) else False
        
        
    def query(self, **kwargs):
        '''
        attributeQuery cannot query attributes with indices, 
        '''
        _attrName = self.attr.split('.')[-1].split('[')[0]
        return cmds.attributeQuery(_attrName, node=self.node.fullPath, **kwargs)
        
    def delete(self):
        self.lock(False)
        
        if not self.exists():
            return om2.MGlobal.displayWarning('Invalid Attribute')
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
            return Attribute(self.node, newName).lock(attrLockState)
        except:
            om2.MGlobal.displayWarning('Parameter Error')
            self.lock(attrLockState)
            return self    
            