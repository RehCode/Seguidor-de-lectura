from PyQt5 import QtCore, QtGui, QtWidgets

class BookStatusWidget(QtWidgets.QWidget):
    def __init__(self, book, parent=None):
        super(BookStatusWidget, self).__init__(parent)

        self.book = book
        self.title = QtWidgets.QLabel(
            "Placeholder title")
        self.progress = QtWidgets.QProgressBar()
        self.progress.setValue(85)
        self.status_chapters = QtWidgets.QLabel("17/20")
        self.cover = QtWidgets.QLabel("")
        self.days = QtWidgets.QLabel("Leido hace 2 dias")

        # info book
        self.title.setText(self.book.title)
        self.title.setObjectName("titulo")
        self.cover.setPixmap(QtGui.QPixmap(self.book.cover_filename))
        self.show_progress()

        with open("./widgets/vistaStyle.css") as file:
            stl = file.read()
        self.setStyleSheet(stl)

        layout_progress = QtWidgets.QGridLayout()
        layout_progress.addWidget(self.title, 0, 1, 1, 3)
        layout_progress.addWidget(self.progress, 1, 1)
        layout_progress.addWidget(self.status_chapters, 1, 2)
        layout_progress.addWidget(self.days, 2, 1)

        self.setLayout(layout_progress)

    def update_book_chapters(self, chapters):

        self.book.chapters_complete = chapters
        self.show_progress()

    def show_progress(self):
        percent = self.book.chapters_complete / self.book.chapters_total
        self.progress.setValue(percent * 100)
        chapters = "{}/{}".format(self.book.chapters_complete,
                                  self.book.chapters_total)
        self.status_chapters.setText(chapters)
        self.days.setText("Leido hace {} dias".format(self.book.days))

