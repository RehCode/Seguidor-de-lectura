from PyQt5 import QtWidgets, QtCore, QtGui


class AddReadingDialog(QtWidgets.QDialog):
    def __init__(self, book, parent=None):
        super(AddReadingDialog, self).__init__(parent)

        ahora = QtCore.QDate.currentDate()
        self.fecha = QtWidgets.QDateEdit()
        self.fecha.setDate(ahora)
        self.capitulo = QtWidgets.QSpinBox()
        self.capitulo.setValue(book.chapters_complete)
        self.capitulo.setMaximum(book.chapters_total)
        self.capitulo.setMinimum(1)
        self.comentario = QtWidgets.QTextEdit()

        self.buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layoutForm = QtWidgets.QFormLayout()
        # layoutForm.addRow("Libro", self.libro)
        layoutForm.addRow("Fecha", self.fecha)
        layoutForm.addRow("Capitulo", self.capitulo)
        layoutForm.addRow("Comentario", self.comentario)

        layoutBotones = QtWidgets.QHBoxLayout()
        layoutBotones.addWidget(self.buttons)

        layoutPincipal = QtWidgets.QVBoxLayout()
        layoutPincipal.addLayout(layoutForm)
        layoutPincipal.addLayout(layoutBotones)

        self.setLayout(layoutPincipal)

        self.setWindowTitle("Registrar Lectura")
        self.setWindowIcon(QtGui.QIcon("icons/bookmark.png"))

    def valores(self):
        fecha = self.fecha.date()
        valores = {"fecha": fecha.toString("yyyy-MM-dd"), "comentario": self.comentario.toPlainText(), 
                    "capitulo": self.capitulo.value()}
        return valores

    def set_capitulo(self, capitulo):
        self.capitulo.setValue(capitulo)

    def set_capitulo_max(self, capitulo):
        self.capitulo.setMaximum(capitulo)
