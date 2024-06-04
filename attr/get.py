import maya.cmds as cmds
import maya.api.OpenMaya as om2
import cmdk.dg.omUtils as omUtils
from cmdk.attr.kMatrix import KMatrix
from cmdk.attr.kVector import KVector

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
        
    # attr types -----------------------------------------------------------
    def queryType(self, _type) -> bool:
        return cmds.getAttr(self.fullPath, typ=True) == _type
        
    @property
    def isMessage(self) -> bool:
        return self.queryType('message')
        
    @property
    def isString(self) -> bool:
        return self.queryType('string')
        
    @property
    def isCompoundAttr(self) -> bool:
        return self.queryType('TdataCompound')
        
    @property
    def isVector(self) -> bool:
        pass
        
    @property
    def isMatrix(self) -> bool:
        pass
        
    @property
    def isQuaternion(self) -> bool:
        pass
        

    #  attr datas ---------------------------------------------------------------------------------------------    

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
        
    @property
    def stringData(self):
        '''
        The string attribute and the information attribute are very similar
        The node's message attribute can be connected with the string attribute
        so it will preferentially return the connected object rather than the string
        '''
        _messageData = self.messageData
        if _messageData: 
            return _messageData
        # ------------------------------
        return cmds.getAttr(self.fullPath) # get string 
        
    @property
    def compoundAttrData(self):
        subAttr = cmds.listAttr(self.fullPath, multi=True) or []
        _compoundAttrData = []
        for attr in subAttr:
            a = GetAttribute(self.nodeName, attr)
            if a.isMessage:
                data = a.messageData
            elif a.isString:
                data = a.stringData
            elif a.isCompoundAttr:
                continue
                #data = None    
            else:
                data = cmds.getAttr('{}.{}'.format(self.nodeName, attr))
                    
            _compoundAttrData.append(data)
            
        return _compoundAttrData
            
    #  -----------------------------------------------------------------------------------------------
    def run(self, *args, **kwargs):
        if self.isMessage:
            return self.messageData
        elif self.isString:
            return self.stringData
        elif self.isCompoundAttr:
            return self.compoundAttrData
        
            
        return cmds.getAttr(self.fullPath, *args, **kwargs)
            
        
        
if __name__ == '__main__':
    a = GetAttribute('blendMatrix1', 'target'); a.run()


#cmds.getAttr('sb.boundingBoxMin', typ=True) 

'''
cmds.attributeQuery('target', node='blendMatrix1', multi=True)
cmds.getAttr('{}.{}'.format('blendMatrix1', 'target[0]'), s=True)
cmds.listAttr('{}.{}'.format('blendMatrix1', 'target[0]'), multi=True)
'''

        




