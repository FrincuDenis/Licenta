import threading

import mariadb
db_lock = threading.Lock()
def conectare_bd(host, user, password, database):
  try:
    return mariadb.connect(
      host=host,
      user=user,
      password=password,
      database=database
    )
  except mariadb.OperationalError as e:
    print(f"Eroare la conectare: {e}")
    return None


def reconnect_if_needed(func):
  def wrapper(*args, **kwargs):
    self = args[0]
    try:
      return func(*args, **kwargs)
    except mariadb.Error as err:
      if err.errno in [mariadb.constants.ER.CON_COUNT_ERROR,
                       mariadb.constants.ER.NOT_CONNECTED,
                       mariadb.constants.ER.SERVER_SHUTDOWN,
                       mariadb.constants.ER.CR_SERVER_LOST,
                       mariadb.constants.ER.CR_SERVER_GONE_ERROR]:
        print("MariaDB connection lost. Reconnecting...")
        self.db_connection = conectare_bd(
          host="your_host",
          user="your_user",
          password="your_password",
          database="your_database"
        )
        return func(*args, **kwargs)
      else:
        raise

  return wrapper


@reconnect_if_needed
def adaugare_inregistrare(conexiune, tabel, valori):
  with db_lock:
    try:
      cursor = conexiune.cursor()
      coloane = ",".join(valori.keys())
      interogare = f"INSERT INTO {tabel} ({coloane}) VALUES ({','.join(['%s'] * len(valori))})"
      cursor.execute(interogare, list(valori.values()))
      conexiune.commit()
      cursor.close()
      print("Înregistrare adăugată cu succes!")
    except mariadb.OperationalError as e:
      print(f"Eroare la adăugare: {e}")

# Ștergere
def stergere_inregistrare(conexiune, tabel, conditie):
  with db_lock:
    try:
      cursor = conexiune.cursor()
      interogare = f"DELETE FROM {tabel} WHERE {conditie}"
      cursor.execute(interogare)
      conexiune.commit()
      cursor.close()
      print("Înregistrare ștearsă cu succes!")
    except mariadb.OperationalError as e:
      print(f"Eroare la ștergere: {e}")

# Actualizare
def actualizare_inregistrare(conexiune, tabel, setari, conditie):
  with db_lock:
    try:
      cursor = conexiune.cursor()
      coloane_valori = ",".join([f"{coloana} = %s" for coloana in setari.keys()])
      interogare = f"UPDATE {tabel} SET {coloane_valori} WHERE {conditie}"
      cursor.execute(interogare, list(setari.values()))
      conexiune.commit()
      cursor.close()
      print("Înregistrare actualizată cu succes!")
    except mariadb.OperationalError as e:
      print(f"Eroare la actualizare: {e}")

# Selectare (citire)
def selectare_inregistrari(connection, table, conditie=None):
  with db_lock:
    try:
      cursor = connection.cursor()
      query = f"SELECT * FROM {table}"
      if conditie:
        query += f" WHERE {conditie}"
      cursor.execute(query)
      results = cursor.fetchall()
      cursor.close()
      return results
    except Exception as e:
      print(f"Database query error: {e}")
      return []
