import sqlite3
from datetime import datetime

conn = sqlite3.connect("./data/data.db")
cursor = conn.cursor()

cursor.execute("select id, titulo, capitulos from libros where leyendo=1;")
data_libros = cursor.fetchall()
for row_libro in data_libros:
    cursor.execute("""select capitulo, max(fecha) as "Ultima fecha"
        from registro where idLibro=?;""", (row_libro[0],))
    registro = cursor.fetchone()

    if registro[0] is None:
        print(row_libro[1])
        print("Leyendo pero sin registro de lectura\n")
        continue

    ultima_fecha_reg = datetime.strptime(registro[1], '%Y-%m-%d')
    days = (datetime.now() - ultima_fecha_reg).days
    percent = registro[0] / row_libro[2]

    information = "{titulo} - leido hace {days} dias - {capitulo}/{totalcap}".format(
        titulo=row_libro[1], days=days, capitulo=registro[0], totalcap=row_libro[2])
    print(information)

    bar = "[{:▒<40}] {percent:.2%}\n".format('█' * int(percent * 40), percent=percent)
    print(bar)

conn.close()
input()
