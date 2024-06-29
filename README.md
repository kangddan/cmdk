![Python version](https://img.shields.io/badge/MAYA-2024-blue?logo=aab) ![Python version](https://img.shields.io/badge/Python-3.10%2C3.11-_blue?logo=aab)


创建/添加
```python
import cmdk
node1 = cmdk.createDagNode('joint')
node2 = cmdk.createDepNode('network', 'metaNode')
# 添加一个或一组对象
node  = cmdk.add('pCube1')
nodes = cmdk.add(['pCube1', 'joint1', 'locator1'])
```
多种获取/设置属性方式 适应不同情况
```python
mathNode = cmdk.createDepNode('plusMinusAverage') 
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
node2 = cmdk.add('JNT')
node == node2       # Result: True #
cmdk.getCache()     # Result: {'03A1372E-4E6D-3787-FD4E-7597FEBE49BE': <DagNode joint 'JNT'>} #

# 强引用添加到缓存字典
nodes = [cmdk.createDepNode('network', 'metaNode_{}'.format(i)) for i in range(3)]
# 无引用时不添加缓存
for i in range(3):
    cmdk.createDepNode('network', 'metaNode_{}'.format(i))
# 删除全部缓存
cmdk.clearCache(); cmdk.getCache() # Result: {} #
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
matrix  = cmdk.add('pTorus1').getGlobalMatrix()             # 获取全局矩阵
vec     = cmdk.add('pCylinder1_str').getGlobalMatrix().off  # 从全局矩阵分解位移向量
vec     = cmdk.add('pCylinder1_str').getGlobalPos()         # 或者直接获取全局位置
# 使用*计算带位移的矩阵向量乘 不考虑左右乘顺序
# 使用%计算不带位移的矩阵向量乘
# matrix % vec 或者 vec % matrix, 此时乘法顺序有意义
vec2    = matrix * vec                                        
vec2    = vec    * matrix 
cmdk.add('pCylinder1').setGlobalPos(vec2)
```
```python
import cmdk

def alignObjectsCmdk():
    sel = cmdk.ls(sl=True)
    if not sel or len(sel) < 3: return
    startVec = sel[0].getGlobalPos(); endVec = sel[-1].getGlobalPos()
    # -------------------------------
    baseVec = [obj.getGlobalPos() for obj in sel[1:-1]]
    offset = (endVec - startVec) / (len(sel)-1)
    # -------------------------------
    newVec = [startVec, *[startVec + offset * (index + 1) for index, v in enumerate(baseVec)], endVec]
    # -------------------------------
    for index, obj in enumerate(sel):
        obj.setGlobalPos(newVec[index]) 
        
alignObjectsCmdk()

# --------------------------------------------------------------------------------------
import maya.cmds as cmds
import maya.api.OpenMaya as om2

def alignObjectsCmds():
    sel = cmds.ls(sl=True)
    if not sel or len(sel) < 3: return
    startVec = om2.MVector(cmds.xform(sel[0], q=True, t=True, ws=True))
    endVec   = om2.MVector(cmds.xform(sel[-1], q=True, t=True, ws=True))
    # -------------------------------
    baseVec = [om2.MVector(cmds.xform(obj, q=True, t=True, ws=True)) for obj in sel[1:-1]]
    offset = (endVec - startVec) / (len(sel)-1)
    # -------------------------------
    newVec = [startVec, *[startVec + offset * (index + 1) for index, v in enumerate(baseVec)], endVec]
    # -------------------------------
    for index, obj in enumerate(sel):
        cmds.xform(obj, t=newVec[index], ws=True)
    
alignObjectsCmds()
```
和cmds结合使用
```python
import maya.cmds as cmds
import cmdk

sel = [cmdk.add(i) for i in cmds.ls(sl=True)]
sel = cmdk.add(cmds.ls(sl=True))

for i in sel:
    print(i.fullPath)
    
# 调用str方法，或者显式调用节点字符串属性
cmds.rename(str(sel[0]), 'abc')
cmds.rename(sel[0].fullPath, 'abc')

print(sel[0].fullPath)
# Result: |abc #
```
字符串属性优先返回对象 元数据友好
```python
import cmdk
metaNode = cmdk.createDepNode('network', 'metaRoot')
metaNode.addAttr('metaChilds', dt='string', m=True)
for i in range(4):
    metaNode['metaChilds'][i].set(i, typ='string')

for i in range(2):
    node = cmdk.createDagNode('joint', 'testNode'+str(i))
    node.message >> metaNode.metaChilds[i]
metaNode.metaChilds.get()
# Result: [<DagNode joint 'testNode0'>, <DagNode joint 'testNode1'>, '2', '3'] #
```





