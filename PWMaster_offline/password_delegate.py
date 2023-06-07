from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QStyledItemDelegate

class PasswordDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.password_editing = {}

    def displayText(self, value, locale):
        if self.password_editing.get(value, False):
            return value
        else:
            return "******"

    def createEditor(self, parent, option, index):
        editor = super().createEditor(parent, option, index)
        if isinstance(editor, QLineEdit):
            self.password_editing[index.data()] = True
        return editor

    def setEditorData(self, editor, index):
        text = index.model().data(index, Qt.DisplayRole)
        if isinstance(editor, QLineEdit):
            editor.setText(text)
        else:
            super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if isinstance(editor, QLineEdit):
            self.password_editing[index.data()] = False
            model.setData(index, editor.text(), Qt.EditRole)
        else:
            super().setModelData(editor, model, index)
