轻量级的 mayaPython wrapper
创建
```python
import cmdk
node1 = cmdk.createDagNode('joint', 'testNode1')
node2 = cmdk.createDepNode('network', 'metaNode')
# 添加一个或一组对象
node = cmdk.kNode('pCube1')
nodes = cmdk.kNode(['pCube1', 'joint1', 'locator1'])
```
多种获取/设置属性方式 适应不同情况
```python
mathNode = cmdk.createDepNode('plusMinusAverage', 'mathNode') 
mathNode.input3D[0].input3Dx.set(15) 
mathNode.input3D[0].input3Dx.get() 
mathNode['input3D[0].input3Dy']() 
mathNode['input3D[0].input3Dy'] = 3
```
连接
```python
node1.message >> node2.affectedBy[0] 
node1.message.connect(node2.affectedBy[0])
```
缓存单例模式 
```python
node3 = cmdk.kNode('testNode1')
id(node1) == id(node3)
# Result: True #
```
和cmds对比 
```python
import maya.api.OpenMaya as om2
import maya.cmds as cmds

m1 = om2.MMatrix(cmds.xform('pTorus1', q=True, m=True, ws=True))
v1 = om2.MVector(cmds.xform('pCylinder1_str', q=True, t=True, ws=True))
v2 = om2.MPoint(v1) * m1 
cmds.xform('pCylinder1', t=om2.MVector(v2), ws=True)

import cmdk

matrix  = cmdk.kNode('pTorus1').getGlobalMatrix()             # 获取全局矩阵
vec     = cmdk.kNode('pCylinder1_str').getGlobalMatrix().off  # 从全局矩阵分解位移向量
vec     = cmdk.kNode('pCylinder1_str').getGlobalPos()         # 或者直接获取全局位置

# 使用*相乘时 不考虑左右乘顺序, 会自动调用向量类的MPoint引用
# 不带位移的矩阵向量乘 在这里使用%
# matrix % vec 或者 vec % matrix, 这时乘法顺序是有意义的
vec2    = matrix * vec                                        
vec2    = vec    * matrix 
cmdk.kNode('pCylinder1').setGlobalPos(vec2)
```
和cmds结合使用
```python
import maya.cmds as cmds
import cmdk

sel = [cmdk.kNode(i) for i in cmds.ls(sl=True)]
sel = cmdk.kNode(cmds.ls(sl=True))

for i in sel:
    print(i.fullPath)
    
# 调用str方法，或者显式调用节点字符串属性
cmds.rename(str(sel[0]), 'abc')
cmds.rename(sel[0].fullPath, 'abc')

print(sel[0].fullPath)
# Result: |abc #
```





