import os
import tempfile
from maya import cmds


def screenShotCurrentPanel(outFile=''):
    if not outFile:
        outFile = tempfile.mktemp(suffix='.jpg').replace('\\', '/')

    curFrame = cmds.currentTime(q=1)
    outHeader = os.path.splitext(outFile)
    outPic = cmds.playblast(
        format='image', filename=outHeader, sequenceTime=0,
        clearCache=1, viewer=0, showOrnaments=1, fp=4,
        os=1, percent=100, compression="jpg", quality=100,
        st=curFrame, et=curFrame, wh=[960, 540])

    realOutPic = outPic.replace('####', '%04d' % curFrame)
    return realOutPic
