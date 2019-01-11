import sqlite3

tabla_libros = """CREATE TABLE IF NOT EXISTS libros (
                id integer PRIMARY KEY,
                titulo text NOT NULL,
                objetivo text,
                fecha text NOT NULL,
                capitulos integer NOT NULL,
                leyendo BOOLEAN DEFAULT (1),
                comentario TEXT
                );"""

tabla_registro = """CREATE TABLE IF NOT EXISTS registro (
                id integer PRIMARY KEY,
                idLibro integer NOT NULL,
                fecha text NOT NULL,
                capitulo integer,
                comentario TEXT,
                FOREIGN KEY (idLibro) REFERENCES libros (id)
                );"""


def create_databse():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(tabla_libros)
    cursor.execute(tabla_registro)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    cmd = input("Create database? (y/n): ")
    if cmd.lower() == "y":
        create_databse()
