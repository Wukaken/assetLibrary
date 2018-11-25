import pySide2Patcher


def _import_module_by_name(parent_module_name, module_name):

    module = None
    try:
        module = __import__(parent_module_name, globals(), locals(), [module_name])
        module = getattr(module, module_name)
    except Exception as e:
        pass
    return module


try:
    import PySide2
    from PySide2 import QtCore, QtGui, QtWidgets
    QtCore, QtGui = pySide2Patcher.PySide2Patcher.patch(QtCore, QtGui, QtWidgets, PySide2)
    QtNetwork = _import_module_by_name("PySide2", "QtNetwork")
    QtWebKit = _import_module_by_name("PySide2.QtWebKitWidgets", "QtWebKit")
except:
    import PySide
    QtGui = _import_module_by_name("PySide", "QtGui")
    QtCore = _import_module_by_name("PySide", "QtCore")
