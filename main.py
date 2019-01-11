import sys
import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
from widgets.reading import AddReadingDialog
from widgets.book import AddBookDialog
from widgets.bookStatus import BookStatusWidget
from model import DataBase, Book


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.database = DataBase()

        self.add_new_book_btn = QtWidgets.QPushButton("Agregar Nuevo Libro")
        self.add_new_book_btn.clicked.connect(self.add_book)
        self.add_new_book_btn.setIcon(QtGui.QIcon("icons/add.png"))

        self.remove_book_btn = QtWidgets.QPushButton("Remover Libro")
        self.remove_book_btn.clicked.connect(self.remove_book)
        self.remove_book_btn.setIcon(QtGui.QIcon("icons/delete.png"))
        
        self.add_reading_book_btn = QtWidgets.QPushButton("Agregar Lectura")
        self.add_reading_book_btn.setIcon(QtGui.QIcon("icons/change.png"))
        self.add_reading_book_btn.clicked.connect(self.add_reading_book)

        layout_buttons = QtWidgets.QHBoxLayout()
        layout_buttons.addWidget(self.add_new_book_btn)
        layout_buttons.addWidget(self.remove_book_btn)
        layout_buttons.addWidget(self.add_reading_book_btn)

        self.items = []
        self.customListWidget = QtWidgets.QListWidget()
        self.customListWidget.itemDoubleClicked.connect(self.register)
        self.reading_books = self.database.get_reading_books()
        for book in self.reading_books:
            bookStatusWidget = BookStatusWidget(book)
            self.items.append(bookStatusWidget)
            item = QtWidgets.QListWidgetItem(self.customListWidget)
            item.setSizeHint(bookStatusWidget.sizeHint())
            self.customListWidget.addItem(item)
            self.customListWidget.setItemWidget(item, bookStatusWidget)

        layoutPincipal = QtWidgets.QVBoxLayout()
        layoutPincipal.addWidget(self.customListWidget)
        layoutPincipal.addLayout(layout_buttons)
        self.setLayout(layoutPincipal)
        self.setMinimumSize(600, 400)

        self.setWindowTitle("Seguimiento de Lectura")
        self.setWindowIcon(QtGui.QIcon("icons/bookmark.png"))

    def add_book(self):
        dlg = AddBookDialog()
        if dlg.exec_():
            values = dlg.values()
            self.database.add_new_book(values["titulo"], values["objetivo"], values["fecha"], values["capitulos"])

    def remove_book(self):
        currentRow = self.customListWidget.currentRow()
        self.customListWidget.takeItem(currentRow)
        self.database.update_book_reading_state(0, self.reading_books[currentRow].id)
        self.reading_books.pop(currentRow)
        self.items.pop(currentRow)
    
    def add_reading_book(self):
        books = self.database.get_not_reading_books()
        items = []
        for book in books:
            items.append(book.title)
		
        item, ok = QtWidgets.QInputDialog.getItem(self, "Agregar libro para leer", 
         "Libro a leer", items, 0, False)
			
        if ok and item:
            for book in books:
                if book.title == item:
                    self.database.update_book_reading_state(1, book.id)
                    bookStatusWidget = BookStatusWidget(book)
                    self.items.append(bookStatusWidget)
                    self.reading_books.append(book)
                    item = QtWidgets.QListWidgetItem(self.customListWidget)
                    item.setSizeHint(bookStatusWidget.sizeHint())
                    self.customListWidget.addItem(item)
                    self.customListWidget.setItemWidget(item, bookStatusWidget)
                    break

    def register(self):
        currentRow = self.customListWidget.currentRow()
        dlg_register = AddReadingDialog(self.reading_books[currentRow])
        if dlg_register.exec_():
            valor = dlg_register.valores()
            self.items[currentRow].update_book_chapters(valor["capitulo"])
            self.database.add_reading(self.reading_books[currentRow], valor["fecha"], valor["capitulo"], valor["comentario"])

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
