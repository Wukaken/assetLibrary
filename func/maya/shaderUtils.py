from maya import cmds


def outputShaderConInfo():
    sgs = cmds.ls(type='shadingEngine')
    shaderConInfo = {}
    for sg in sgs:
        conObjs = cmds.sets(sg, q=1)
        if conObjs:
            objAttr = '%s.surfaceShader' % sg
            shaders = cmds.listConnections(objAttr, s=1, d=0)
            if shaders:
                shader = shaders[0]
                shaderConInfo[shader] = conObjs

    return shaderConInfo
