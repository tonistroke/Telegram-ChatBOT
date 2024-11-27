import sqlite3

conn = sqlite3.connect('soldorado.db')

cursor = conn.cursor()

sql_script_reserva = """CREATE TABLE IF NOT EXISTS reserva (
    reserva_id INTEGER PRIMARY KEY AUTOINCREMENT,
    reserva_usuario TEXT,
    reserva_num INTEGER UNIQUE NOT NULL,
    reserva_fecha TEXT NOT NULL,
    reserva_dias INTEGER NOT NULL
);
"""
cursor.execute(sql_script_reserva)


conn.commit()
conn.close()