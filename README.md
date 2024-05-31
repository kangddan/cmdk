轻量级的 mayaPython wrapper

` import cmdk`
# 创建
` node1 = cmdk.createDagNode('joint', 'testNode1')`

`node2 = cmdk.createDepNode('network', 'metaNode') ` 

# 获取属性
`node1.attr.worldMatrix[0].get() `

`node1.attr['worldMatrix'][0].get() `

# 连接
`node1.attr.message >> node2.attr.affectedBy[0] ` 

`node1.attr.message.connect(node2.attr.affectedBy[0]) ` 

# 缓存单例模式 

`node3 = cmdk.kNode('testNode1')` 

`id(node1) == id(node3) ` 

`# Result: True # ` 




