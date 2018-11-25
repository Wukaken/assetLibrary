from __future__ import with_statement

import os
import functools
import imp
import subprocess
import sys
import webbrowser


class PySide2Patcher(object):
    _core_to_qtgui = set([
        "QAbstractProxyModel",
        "QItemSelection",
        "QItemSelectionModel",
        "QItemSelectionRange",
        "QSortFilterProxyModel",
        "QStringListModel"
    ])


    @classmethod
    def _move_attributes(cls, dst, src, names):
        """
        Moves a list of attributes from one package to another.

        :param names: Names of the attributes to move.
        """
        for name in names:
            if not hasattr(dst, name):
                setattr(dst, name, getattr(src, name))

    @classmethod
    def _patch_QTextCodec(cls, QtCore):
        """
        Patches in QTextCodec.

        :param QTextCodec: The QTextCodec class.
        """
        original_QTextCodec = QtCore.QTextCodec

        class QTextCodec(original_QTextCodec):
            @staticmethod
            def setCodecForCStrings(codec):
                pass

        QtCore.QTextCodec = QTextCodec

    @classmethod
    def _fix_QCoreApplication_api(cls, wrapper_class, original_class):

        wrapper_class.CodecForTr = 0
        wrapper_class.UnicodeUTF8 = 1
        wrapper_class.DefaultCodec = wrapper_class.CodecForTr

        @staticmethod
        def translate(context, source_text, disambiguation=None, encoding=None, n=None):

            if n is not None:
                return original_class.translate(context, source_text, disambiguation, n)
            else:
                return original_class.translate(context, source_text, disambiguation)

        wrapper_class.translate = translate

    @classmethod
    def _patch_QCoreApplication(cls, QtCore):

        original_QCoreApplication = QtCore.QCoreApplication

        class QCoreApplication(original_QCoreApplication):
            pass
        cls._fix_QCoreApplication_api(QCoreApplication, original_QCoreApplication)
        QtCore.QCoreApplication = QCoreApplication

    @classmethod
    def _patch_QApplication(cls, QtGui):

        original_QApplication = QtGui.QApplication

        class QApplication(original_QApplication):
            def __init__(self, *args):
                original_QApplication.__init__(self, *args)
                QtGui.qApp = self

            @staticmethod
            def palette(widget=None):

                return original_QApplication.palette(widget)

        cls._fix_QCoreApplication_api(QApplication, original_QApplication)

        QtGui.QApplication = QApplication

    @classmethod
    def _patch_QAbstractItemView(cls, QtGui):

        original_QAbstractItemView = QtGui.QAbstractItemView

        class QAbstractItemView(original_QAbstractItemView):
            def __init__(self, *args):
                original_QAbstractItemView.__init__(self, *args)

                if hasattr(self, "dataChanged"):
                    original_dataChanged = self.dataChanged

                    def dataChanged(tl, br, roles=None):
                        original_dataChanged(tl, br)
                    self.dataChanged = lambda tl, br, roles: dataChanged(tl, br)

        QtGui.QAbstractItemView = QAbstractItemView

    @classmethod
    def _patch_QStandardItemModel(cls, QtGui):

        original_QStandardItemModel = QtGui.QStandardItemModel

        class SignalWrapper(object):
            def __init__(self, signal):
                self._signal = signal

            def emit(self, tl, br):
                self._signal.emit(tl, br, [])

            def __getattr__(self, name):
                return getattr(self._signal, name)

        class QStandardItemModel(original_QStandardItemModel):
            def __init__(self, *args):
                original_QStandardItemModel.__init__(self, *args)
                self.dataChanged = SignalWrapper(self.dataChanged)

        QtGui.QStandardItemModel = QStandardItemModel

    @classmethod
    def _patch_QMessageBox(cls, QtGui):

        button_list = [
            QtGui.QMessageBox.Ok,
            QtGui.QMessageBox.Open,
            QtGui.QMessageBox.Save,
            QtGui.QMessageBox.Cancel,
            QtGui.QMessageBox.Close,
            QtGui.QMessageBox.Discard,
            QtGui.QMessageBox.Apply,
            QtGui.QMessageBox.Reset,
            QtGui.QMessageBox.RestoreDefaults,
            QtGui.QMessageBox.Help,
            QtGui.QMessageBox.SaveAll,
            QtGui.QMessageBox.Yes,
            QtGui.QMessageBox.YesAll,
            QtGui.QMessageBox.YesToAll,
            QtGui.QMessageBox.No,
            QtGui.QMessageBox.NoAll,
            QtGui.QMessageBox.NoToAll,
            QtGui.QMessageBox.Abort,
            QtGui.QMessageBox.Retry,
            QtGui.QMessageBox.Ignore
        ]


        def _method_factory(icon, original_method):

            def patch(parent, title, text, buttons=QtGui.QMessageBox.Ok, defaultButton=QtGui.QMessageBox.NoButton):

                msg_box = QtGui.QMessageBox(parent)
                msg_box.setWindowTitle(title)
                msg_box.setText(text)
                msg_box.setIcon(icon)
                for button in button_list:
                    if button & buttons:
                        msg_box.addButton(button)
                msg_box.setDefaultButton(defaultButton)
                msg_box.exec_()
                return msg_box.standardButton(msg_box.clickedButton())

            functools.update_wrapper(patch, original_method)

            return staticmethod(patch)

        original_QMessageBox = QtGui.QMessageBox

        class QMessageBox(original_QMessageBox):

            critical = _method_factory(QtGui.QMessageBox.Critical, QtGui.QMessageBox.critical)
            information = _method_factory(QtGui.QMessageBox.Information, QtGui.QMessageBox.information)
            question = _method_factory(QtGui.QMessageBox.Question, QtGui.QMessageBox.question)
            warning = _method_factory(QtGui.QMessageBox.Warning, QtGui.QMessageBox.warning)

        QtGui.QMessageBox = QMessageBox

    @classmethod
    def _patch_QDesktopServices(cls, QtGui, QtCore):

        if hasattr(QtGui, "QDesktopServices"):
            return

        class QDesktopServices(object):

            @classmethod
            def openUrl(cls, url):
                if not isinstance(url, QtCore.QUrl):
                    url = QtCore.QUrl(url)

                if url.isLocalFile():
                    url = url.toLocalFile().encode("utf-8")

                    if sys.platform == "darwin":
                        return subprocess.call(["open", url]) == 0
                    elif sys.platform == "win32":
                        os.startfile(url)
                        return os.path.exists(url)
                    elif sys.platform.startswith("linux"):
                        return subprocess.call(["xdg-open", url]) == 0
                    else:
                        raise ValueError("Unknown platform: %s" % sys.platform)
                else:
                    try:
                        return webbrowser.open_new_tab(url.toString().encode("utf-8"))
                    except:
                        return False

            @classmethod
            def displayName(cls, type):
                cls.__not_implemented_error(cls.displayName)

            @classmethod
            def storageLocation(cls, type):
                cls.__not_implemented_error(cls.storageLocation)

            @classmethod
            def setUrlHandler(cls, scheme, receiver, method_name=None):
                cls.__not_implemented_error(cls.setUrlHandler)

            @classmethod
            def unsetUrlHandler(cls, scheme):
                cls.__not_implemented_error(cls.unsetUrlHandler)

            @classmethod
            def __not_implemented_error(cls, method):
                raise NotImplementedError(
                    "PySide2 and Toolkit don't support 'QDesktopServices.%s' yet. Please contact %s" %
                    (method.__func__, 'asdf@qq.com')
                )

        QtGui.QDesktopServices = QDesktopServices

    @classmethod
    def patch(cls, QtCore, QtGui, QtWidgets, PySide2):

        qt_core_shim = imp.new_module("PySide.QtCore")
        qt_gui_shim = imp.new_module("PySide.QtGui")


        cls._move_attributes(qt_gui_shim, QtWidgets, dir(QtWidgets))
        cls._move_attributes(qt_gui_shim, QtGui, dir(QtGui))


        cls._move_attributes(qt_gui_shim, QtCore, cls._core_to_qtgui)
        cls._move_attributes(qt_core_shim, QtCore, set(dir(QtCore)) - cls._core_to_qtgui)

        cls._patch_QTextCodec(qt_core_shim)
        cls._patch_QCoreApplication(qt_core_shim)
        cls._patch_QApplication(qt_gui_shim)
        cls._patch_QAbstractItemView(qt_gui_shim)
        cls._patch_QStandardItemModel(qt_gui_shim)
        cls._patch_QMessageBox(qt_gui_shim)
        cls._patch_QDesktopServices(qt_gui_shim, qt_core_shim)

        return qt_core_shim, qt_gui_shim
