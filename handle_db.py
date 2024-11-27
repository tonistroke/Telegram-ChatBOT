import sqlite3
conn = sqlite3.connect('soldorado.db')

import sqlite3

# Crear nueva reserva
def db_new_reserva(usuario, fecha, dias):
    conn = sqlite3.connect('soldorado.db')
    cursor = conn.cursor()

    # Generando reserva_num
    cursor.execute("SELECT MAX(reserva_id) FROM reserva")
    last_id = cursor.fetchone()[0]

    if last_id is None:
        num = 1  # First entry, reserva_num starts from 1
    else:
        num = last_id + 1  # Increment the last reserva_id to generate reserva_num

    # Insertando datos a la BD
    cursor.execute("""
        INSERT INTO reserva (reserva_usuario, reserva_num, reserva_fecha, reserva_dias)
        VALUES (?, ?, ?, ?)
    """, (usuario, num, fecha, dias))

    conn.commit()
    conn.close()

# Mostrar reserva con numero de reserva
def db_check_reserva(reserva_num):
    # Connect to the SQLite database
    conn = sqlite3.connect('soldorado.db')
    cursor = conn.cursor()
    
    # Query the reserva table for the given reserva_num
    cursor.execute("SELECT reserva_num, reserva_fecha, reserva_dias FROM reserva WHERE reserva_num = ?", (reserva_num,))

    # Fetch the result
    reserva = cursor.fetchone()

    # Check if the reservation exists
    if reserva:
        # Print the reservation details
        return f"Numero de reserva: {reserva[0]}", f"Fecha de la reserva: {reserva[1]}", f"Dias reservados: {reserva[2]}"
    else:
        return "No se encontro ninguna reserva con el numero ingresado.", "", ""
    
    conn.close()

# Eliminar reserva
def db_delete_reserva():
    conn = sqlite3.connect('soldorado.db')
    cursor = conn.cursor()
    cursor.execute("DELETE * FROM reserva WHERE reserva_num = ?")

    conn.commit()
    conn.close()

# Check todas las reservas
def check_db():
    conn = sqlite3.connect('soldorado.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reserva")

    reservas = cursor.fetchall()
    
    # PRINT TABLE
    for reserva in reservas:
        print(f"Reserva ID: {reserva[0]}")
        print(f"Reserva Number: {reserva[1]}")
        print(f"Reserva Fecha: {reserva[2]}")
        print(f"Reserva Dias: {reserva[3]}")
        print('-' * 20)

    conn.close()


# Ejemplo de uso. Insert a new reserva
db_new_reserva("toto", '2024-11-21', 6)
check_db()

"""
Uso de db_check_reserva()
reserva_num, reserva_fecha, reserva_dias = db_check_reserva(1)

print(reserva_num)
print(reserva_fecha)
print(reserva_dias)
"""
