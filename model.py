import sys
import sqlite3
from datetime import datetime

class DataBase():
    def __init__(self):
        self.conn = sqlite3.connect("./data/data.db")
        self.cursor = self.conn.cursor()

    def get_reading_books(self):
        reading_books = []
        self.cursor.execute(
            "select id, titulo, capitulos from libros where leyendo=1")
        cont = 1
        for row_libro in self.cursor.fetchall():
            self.cursor.execute("""select capitulo, fecha from registro where idLibro=? order by id desc limit 1;""", (row_libro[0],))
            registro = self.cursor.fetchone()

            if registro is None:
                chapters_complete = 0
                days = 0
            else:
                chapters_complete = registro[0]
                ultima_fecha_reg = datetime.strptime(registro[1], '%Y-%m-%d')
                days = (datetime.now() - ultima_fecha_reg).days

            cover_filename = "cover{}".format(cont)
            if cont <= 3:
                cont += 1
            if cont >= 4:
                cont = 3
            reading_books
            reading_books.append(
                Book(row_libro[0], row_libro[1], row_libro[2], chapters_complete, days, cover_filename))
            reading_books.sort(key=lambda book: book.days, reverse=True)

        return reading_books
    
    def get_not_reading_books(self):
        not_reading = []
        self.cursor.execute(
            "select id, titulo, capitulos, leyendo from libros where leyendo=0;"
        )

        for row_libro in self.cursor.fetchall():
            not_reading.append(
                Book(row_libro[0], row_libro[1], row_libro[2], reading=row_libro[3])
            )
        return not_reading
    
    def add_reading(self, book, fecha, capitulo, comentario):
        self.cursor.execute("""
            INSERT INTO registro (idLibro, fecha, capitulo, comentario) VALUES (?, ?, ?, ?)""",
                       (book.id, fecha, capitulo, comentario))
        self.conn.commit()
    
    def add_new_book(self, titulo, objetivo, fecha, capitulos):
        self.cursor.execute("""
        INSERT INTO libros (titulo, objetivo, fecha, capitulos) VALUES (?, ?, ?, ?)""",
                   (titulo, objetivo, fecha, capitulos))
        self.conn.commit()

    def update_book_reading_state(self, reading, idBook):

        if reading == True:
            reading = 1
        if reading == False:
            reading = 0

        self.cursor.execute("""
            UPDATE libros set leyendo=? where id=?""",
                       (reading, idBook))
        self.conn.commit()
    
    def get_total_days_reading(self, idBook):
        """ Return total days from date of the first registry to the last """
        self.cursor.execute("select fecha from registro where idLibro=? order by id asc limit 1;", (idBook,))
        first_date = self.cursor.fetchone()
        if first_date == None:
            return 0
        first_date = datetime.strptime(first_date[0], '%Y-%m-%d')
        self.cursor.execute("select fecha from registro where idLibro=? order by id desc limit 1;", (idBook,))
        last_date = self.cursor.fetchone()
        last_date = datetime.strptime(last_date[0], '%Y-%m-%d')
        days = (last_date - first_date).days
        return days


class Book():
    def __init__(self, id, title, chapters_total, chapters_complete=0, days=0, cover_filename="cover1", reading=True):
        self.id = id
        self.title = title
        self.cover_filename = cover_filename
        self.chapters_total = chapters_total
        self.chapters_complete = chapters_complete

        if reading == 1:
            self.reading = True
        elif reading == 0:
            self.reading = False
        else:
            self.reading = reading

        self.days = days

    def __repr__(self):
        return "#{}-{}".format(self.id, self.title)

    def add_chapters(self):
        self.chapters_complete += 1
        if self.chapters_complete > self.chapters_total:
            self.chapters_complete = self.chapters_total


if __name__ == "__main__":
        database = DataBase()

        print("Reading books")
        print(" Id | Days | Title\n")
        for book in database.get_reading_books():
            days = database.get_total_days_reading(book.id)
            template = "{id:>3} | {days:>4} | {title}"
            print(template.format(id=book.id, days=days, title=book.title))

        print("\n\nNot reading books")
        print(" Id | Days | Title\n")
        for book in database.get_not_reading_books():
            days = database.get_total_days_reading(book.id)
            template = "{id:>3} | {days:>4} | {title}"
            print(template.format(id=book.id, days=days, title=book.title))
