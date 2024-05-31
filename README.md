轻量级的 mayaPython wrapper

` import cmdk`
# create node
` node1 = cmdk.createDagNode('joint', 'testNode1')`

`node2 = cmdk.createDepNode('network', 'metaNode') ` 

# get attr
`node1.attr.worldMatrix[0].get() `

`node1.attr['worldMatrix'][0].get() `


# connect attr
`node1.attr.message >> node2.attr.affectedBy[0] ` 

`node1.attr.message.connect(node2.attr.affectedBy[0]) ` 
