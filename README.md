轻量级的 mayaPython wrapper
# 创建
```python
 import cmdk

node1 = cmdk.createDagNode('joint', 'testNode1')
node2 = cmdk.createDepNode('network', 'metaNode')
```
# 多种获取/设置属性方式 适应不同情况
```python
mathNode = cmdk.createDepNode('plusMinusAverage', 'mathNode') 
mathNode.input3D[0].input3Dx.set(15) 
mathNode.input3D[0].input3Dx.get() 
mathNode['input3D[0].input3Dy']() 
mathNode['input3D[0].input3Dy'] = 3
```
# 连接
```python
node1.message >> node2.affectedBy[0] 
node1.message.connect(node2.affectedBy[0])
```
# 缓存单例模式 
```python
node3 = cmdk.kNode('testNode1')
id(node1) == id(node3)
# Result: True #
```
# 和cmds对比 
```python
import maya.api.OpenMaya as om2
import maya.cmds as cmds

m1 = om2.MMatrix(cmds.xform('pTorus1', q=True, m=True, ws=True))
v1 = om2.MVector(cmds.xform('pCylinder1_str', q=True, t=True, ws=True))
v2 = om2.MPoint(v1) * m1 
cmds.xform('pCylinder1', t=om2.MVector(v2), ws=True)

import cmdk

matrix  = cmdk.kNode('pTorus1').getGlobalMatrix()             # get global matrix
vec     = cmdk.kNode('pCylinder1_str').getGlobalMatrix().off  # get global pos
vec2    = matrix * vec                                        # or vec * matrix  带位移的矩阵向量乘 不考虑左乘右乘顺序
cmdk.kNode('pCylinder1').setGlobalPos(vec2)
```





