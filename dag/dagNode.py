import maya.cmds as cmds
import maya.api.OpenMaya as om2
from cmdk.dg.depNode import DepNode

class DagNode(DepNode):
    
    def __init__(self, nodeName :str = '', nodeType :str = ''):
        #super(DagNode, self).__init__(nodeName, nodeType)
        super().__init__(nodeName, nodeType)
        
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
            
    # --------------------------------------------------------
    def moveTo(self, item, **kwargs):
        cmds.matchTransform(self.fullPath, str(item), **kwargs)
    
        
        
# if __name__ == '__main__':
#     testNode = DagNode('pCube1')
#     testNode2 = DagNode('pSphere1')

#     testNode.parentTo(testNode2)
#     testNode.attr.addAttr('metaParent', at='message')
#     testNode.attr.metaParent.delete()




