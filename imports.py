import time

import csv
import psycopg2
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, text
from sqlalchemy.orm import scoped_session, sessionmaker

from db import db


contador = 0

with open('books.csv', newline='', encoding='utf-8') as csvbooks:
    reader_csv = csv.reader(csvbooks)
    next(reader_csv, None) # Para saltar de linea que son las llaves
    for row in reader_csv:

        contador += 1  # Incrementar el contador de fila actual
        isbn, title, author, year = row # Son los nombres de las llaves del archivo CSV

        # Se hace un ciclo con try catch, para validar los errores (PORQUE EL RENDER SE CAE A CADA RATO)
        # Hasta que el ciclo sea "sucess = True seguirá en el ciclo"
        success = False
        while not success:
            try:
                # Se inserta los nombres de los autores en la bd, si no existe aún se retorna su author_id(llave primaria de la tabla authors)
                # pero si existe no hace nada y retiene el error
                query = text("INSERT INTO authors (name) VALUES (:name) ON CONFLICT DO NOTHING RETURNING author_id ")
                author_id = db.execute(query,{"name": author}).fetchone()

                # Si el autor está en la base de datos, se hace una consulta para poder obtener su author_id (llave primaria de la tabla authors)
                if author_id is None:
                    print("Es none")
                    query2 = text("SELECT author_id FROM authors WHERE (name = :author)")
                    author_id = db.execute(query2, {"author": author}).fetchone()

                # Ahora se insertan los datos del libro y a luego de insertarlos se retorna su book_id(llave primaria de book)
                query3 = text("INSERT INTO book (ISBN, title, year) VALUES (:ISBN, :title, :year) RETURNING book_id")
                book_id = db.execute(query3,{"ISBN": isbn, "title": title, "year": year}).fetchone()

                # Ahora se insertan el author_id y el book_id de la tabla que relaciona a las tablas authors y book
                query4 = text("INSERT INTO authors_books (author_id, book_id) VALUES (:author_id, :book_id)")
                db.execute(query4,{"author_id": author_id[0], "book_id": book_id[0]}) # Como se había obtenido mediante el fetchone de los insert son tuplas por lo que se pone la posición 0 

                db.commit()
                print(f'Importe No. {contador}.')
                success = True
                
            except Exception as e:
                print(f"Error: {e}. Reintentando...") # Imprime el error
                db.rollback() # Deshacer el insert de la fila
                time.sleep(5) # Se espera 5 segundos para volver a intentar
                
    db.close()




