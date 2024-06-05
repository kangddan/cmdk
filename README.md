![Python version](https://img.shields.io/badge/MAYA-2024-blue?logo=aab) ![Python version](https://img.shields.io/badge/Python-3.10%2C3.11-_blue?logo=aab)


创建/添加
```python
import cmdk
node1 = cmdk.createDagNode('joint', 'testNode1')
node2 = cmdk.createDepNode('network', 'metaNode')
# 添加一个或一组对象
node  = cmdk.kNode('pCube1')
nodes = cmdk.kNode(['pCube1', 'joint1', 'locator1'])
```
多种获取/设置属性方式 适应不同情况
```python
mathNode = cmdk.createDepNode('plusMinusAverage', 'mathNode') 
mathNode.input3D[0].input3Dx.set(15) 
mathNode.input3D[0].input3Dx.get() 
mathNode['input3D[0].input3Dy']() 
mathNode['input3D[0].input3Dy'] = 3

joint = cmdk.createDagNode('joint', 'testJNT')
joint.message >> mathNode.input1D[0]
attrs = ['tx', 'worldMatrix[0]', 'message']
values = [joint[attr].get() for attr in attrs]
print(values)
# Result: [0.0,
# KMatrix(v1: (1.0, 0.0, 0.0); v2: (0.0, 1.0, 0.0); v3: (0.0, 0.0, 1.0); off: (0.0, 0.0, 0.0)),
# <DepNode plusMinusAverage 'mathNode'>] #
```
连接/断开
```python
node1.message >> node2.affectedBy[0] 
node1.message.connect(node2.affectedBy[0])

node2.affectedBy[0].disconnect()        # 断开output
node2.affectedBy[0].disconnect(False)   # 断开input
~node2.affectedBy[0]                    # 断开所有
```
缓存单例模式 
```python
node  = cmdk.createDagNode('joint', 'JNT')
node2 = cmdk.kNode('JNT')
node == node2       # Result: True #
node.getCache()     # Result: {'03A1372E-4E6D-3787-FD4E-7597FEBE49BE': <DagNode joint 'JNT'>} #

# 强引用添加到缓存字典
nodes = [cmdk.createDepNode('network', 'metaNode_{}'.format(i)) for i in range(3)]
# 无引用时不添加缓存
for i in range(3):
    cmdk.createDepNode('network', 'metaNode_{}'.format(i))
# 删除全部缓存
node.clearCache(); node.getCache() # Result: {} #
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
# 使用*计算带位移的矩阵向量乘 不考虑左右乘顺序
# 使用%计算不带位移的矩阵向量乘
# matrix % vec 或者 vec % matrix, 此时乘法顺序有意义
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
字符串属性优先返回对象
```python
import cmdk
metaNode = cmdk.createDepNode('network', 'metaRoot')
metaNode.addAttr('metaChilds', dt='string', m=True)
metaNode.metaChilds[0].set('aa', typ='string')
metaNode.metaChilds[1].set('bb', typ='string')
metaNode.metaChilds[2].set('cc', typ='string')
metaNode.metaChilds[3].set('dd', typ='string')

for i in range(2):
    node = cmdk.createDagNode('joint', 'testNode'+str(i))
    node.message >> metaNode.metaChilds[i]
metaNode.metaChilds.get()
# Result: [<DagNode joint 'testNode0'>, <DagNode joint 'testNode1'>, 'cc', 'dd'] #
```





