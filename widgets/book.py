from PyQt5 import QtWidgets, QtCore, QtGui


class AddBookDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AddBookDialog, self).__init__(parent)

        self.titulo = QtWidgets.QLineEdit()
        self.objetivo = QtWidgets.QLineEdit()
        ahora = QtCore.QDate.currentDate()
        self.fecha = QtWidgets.QDateEdit()
        self.fecha.setDate(ahora)
        self.capitulos = QtWidgets.QSpinBox()
        self.capitulos.setMaximum(99999)
        self.capitulos.setMinimum(1)


        self.buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layoutBotones = QtWidgets.QHBoxLayout()
        layoutBotones.addWidget(self.buttons)

        layoutForm = QtWidgets.QFormLayout()
        layoutForm.addRow("Titulo", self.titulo)
        layoutForm.addRow("Objetivo", self.objetivo)
        layoutForm.addRow("Fecha", self.fecha)
        layoutForm.addRow("Capitulos", self.capitulos)

        layoutPincipal = QtWidgets.QVBoxLayout()
        layoutPincipal.addLayout(layoutForm)
        layoutPincipal.addLayout(layoutBotones)

        self.setLayout(layoutPincipal)

        self.setWindowTitle("Agregar libro")
        self.setWindowIcon(QtGui.QIcon("icons/book_add.png"))

    def values(self):
        fecha = self.fecha.date()
        values = {"titulo": self.titulo.text(), "objetivo": self.objetivo.text(), 
                    "fecha": fecha.toString("yyyy-MM-dd"), "capitulos": self.capitulos.value()}
        return values

    def cancelarSalir(self):
        QtWidgets.QApplication.instance().quit()
