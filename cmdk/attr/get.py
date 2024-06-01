import maya.cmds as cmds
import maya.api.OpenMaya as om2
import cmdk.dg.omUtils as omUtils

class GetAttribute(object):
    
    def __init__(self, nodeName: str, attrName: str):
        self.nodeName = nodeName
        self.attrName = attrName
    
    @property    
    def fullPath(self):
        return '{}.{}'.format(self.nodeName, self.attrName)
        
    @property
    def name(self):
        return self.fullPath.split('.')[-1].split('[')[0]
        
    @property    
    def isMulti(self) -> bool:
        if cmds.getAttr(self.fullPath, s=True) > 1:
            return True
            
        _isMulti= cmds.attributeQuery(self.name, node=self.nodeName, multi=True)
        return ']' != self.fullPath[-1] and  _isMulti
        
    # -----------------------------------------------------------
    @property
    def isMessage(self) -> bool:
        return cmds.getAttr(self.fullPath, typ=True) == 'message'
    
        
    # message -----------------------------------------------------------------------------------------------
    @property
    def messageData(self):
        from cmdk.dg.depNode  import DepNode
        from cmdk.dag.dagNode import DagNode
        if self.isMulti:
            nodes = cmds.listConnections(self.fullPath) or []
            return [DagNode(node) if omUtils.isDagNode(node) else DepNode(node) for node in nodes]
            
        nodes = cmds.listConnections(self.fullPath, s=False) or cmds.listConnections(self.fullPath, d=False)
        if nodes is None:
            return
        return DagNode(nodes[0]) if omUtils.isDagNode(nodes[0]) else DepNode(nodes[0])
        
        
        
    #  -----------------------------------------------------------------------------------------------
    def run(self):
        if self.isMessage:
            return self.messageData
        
        return cmds.getAttr(self.fullPath)
            
        
        
if __name__ == '__main__':
    a = GetAttribute('joint1', 'tx'); a.run()


#cmds.getAttr('sb.boundingBoxMin', typ=True) 




'''
cmds.attributeQuery('target', node='blendMatrix1', multi=True)
cmds.getAttr('{}.{}'.format('blendMatrix1', 'target[0]'), s=True)
cmds.listAttr('{}.{}'.format('blendMatrix1', 'target[0]'), multi=True)
'''

        




