轻量级的 mayaPython wrapper

` import cmdk`
# 创建
` node1 = cmdk.createDagNode('joint', 'testNode1')`

`node2 = cmdk.createDepNode('network', 'metaNode') ` 

# 多种获取/设置属性方式 适应不同情况
`node1.attr.worldMatrix[0].get() `

`node1.attr['worldMatrix'][0].get() `

`mathNode = cmdk.createDepNode('plusMinusAverage', 'mathNode') `

`mathNode.attr.input3D[0].input3Dx.set(15) `

`mathNode.attr.input3D[0].input3Dx.get() `


`mathNode.attr['input3D[0].input3Dy']() `

`mathNode.attr['input3D[0].input3Dy'] = 3 `


# 连接
`node1.attr.message >> node2.attr.affectedBy[0] ` 

`node1.attr.message.connect(node2.attr.affectedBy[0]) ` 

# 缓存单例模式 

`node3 = cmdk.kNode('testNode1')` 

`id(node1) == id(node3) ` 

`# Result: True # ` 




