import mariadb
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

# Adăugare
def adaugare_inregistrare(conexiune, tabel, valori):
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
def selectare_inregistrari(conexiune, tabel, coloane="*", conditie=None):
  try:
    cursor = conexiune.cursor()
    interogare = f"SELECT {coloane} FROM {tabel}"
    if conditie is not None:
      interogare += f" WHERE {conditie}"
    cursor.execute(interogare)
    rezultate = cursor.fetchall()
    cursor.close()
    return rezultate
  except mariadb.OperationalError as e:
    print(f"Eroare la selectare: {e}")
    return None