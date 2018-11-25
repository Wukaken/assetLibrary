from maya import cmds


def outputCtrlNames():
    ctrls = cmds.ls('_ctrl', type='transform')
    return ctrls
