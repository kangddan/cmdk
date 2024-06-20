from cmdk.attr.kMatrix import KMatrix
from cmdk.attr.kVector import KVector
import maya.cmds as cmds
import maya.api.OpenMaya as om2
from cmdk.dg.depNode import DepNode

class DagNode(DepNode):
    
    def __init__(self, nodeType :str = '', nodeName :str = ''):
        super().__init__(nodeType, nodeName)
    
    def delete(self):
        '''
        When there are too many children, a recursion error is triggered
        You should directly use cmdk.delete()
        '''
        try:
            children = self.children
            if children:
                for c in children:
                    c.delete()
        except RecursionError:
            super().delete()
        else:
            super().delete()

      
    def setVisibility(self, Value):
        if self.exists():
            cmds.setAttr('{0}.visibility'.format(self.fullPath), Value)
                    
    def show(self):
        self.setVisibility(True)
        
    def hide(self):
        self.setVisibility(False)

    @property
    def shape(self):
        '''
        return: [DagNode(shape), ...] or []
        '''
        return [DagNode(shape) 
        for shape in cmds.listRelatives(self.fullPath, s=True, f=True, ni=True) 
        or []]
        '''
        @property
        def shapeData(self):
            #return SplineData(self)
            pass
        
        @shapeData.setter
        def shapeData(self, data):
            #SplineData(self, data)
            pass
        '''
        
    @property
    def children(self):
        
        children = []
        '''
        shapePaths = [shape.fullPath for shape in self.shape] 
        '''
        for child in cmds.listRelatives(self.fullPath, c=True, f=True, ni=True) or []:
            '''
            We have implemented the __eq__ method in depNode, so we can compare instances by their long names
            If the long names are the same, it returns True
            '''
            if child not in self.shape:
                children.append(DagNode(child))    
                
        return children
        
    @property
    def allChildren(self):
        return [DagNode(child) 
                for child in cmds.listRelatives(self.fullPath, ad=True, f=True, ni=True) 
                or []]
    
    @property
    def parent(self):
        parent = cmds.listRelatives(self.fullPath, p=True, f=True)
        if parent:
            return DagNode(parent[0])
            
    @property
    def allParent(self):
        parents = []
        parent = self.parent
        while parent:
            parents.append(parent)
            parent = parent.parent
        return parents
        
    # --------------------------------------------------------
    
    def parentTo(self, item):
        cmds.parent(self.fullPath, str(item))
        
    def parentToWorld(self):
        cmds.parent(self.fullPath, w=True)
        
    def unGroup(self):
        parent = self.parent
        children = self.children
        
        if not children:
            return
        for child in children:
            if parent: child.parentTo(parent.fullPath)
            else: child.parentToWorld()

    def moveTo(self, item, **kwargs):
        cmds.matchTransform(self.fullPath, str(item), **kwargs)
        
    # --------------------------------------------------------
    def getGlobalMatrix(self) -> KMatrix:
        return KMatrix(cmds.xform(self.fullPath, q=True, m=True, ws=True))
        
    def setGlobalMatrix(self, matrix: KMatrix):
        if isinstance(matrix, (KMatrix, list, tuple, om2.MMatrix)):
            cmds.xform(self.fullPath, m=[*matrix], ws=True)
            
    def getLocalMatrix(self) -> KMatrix:
        return KMatrix(cmds.xform(self.fullPath, q=True, m=True, ws=False))
        
    def setLocalMatrix(self, matrix: KMatrix):
        if isinstance(matrix, (KMatrix, list, tuple, om2.MMatrix)):
            cmds.xform(self.fullPath, m=[*matrix], ws=False)
            
    def getGlobalPos(self) -> KVector:
        return KVector(cmds.xform(self.fullPath, q=True, t=True, ws=True))
    
    def setGlobalPos(self, vactor):
        if isinstance(vactor, (KVector, list, tuple, om2.MVector)):
            cmds.xform(self.fullPath, t=[*vactor], ws=True)
    
    def getLocalPos(self) -> KVector:
        return KVector(cmds.xform(self.fullPath, q=True, t=True, ws=False))
        
    def setLocalPos(self, vactor):
        if isinstance(vactor, (KVector, list, tuple, om2.MVector)):
            cmds.xform(self.fullPath, t=[*vactor], ws=False)
        
if __name__ == '__main__':    
    node = DagNode('', 'joint2') 
    #node.shape[0].delete()






