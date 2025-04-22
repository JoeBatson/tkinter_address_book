import sqlite3


def connect_db():
    conn = sqlite3.connect("address_book.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS name_address(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    first_name TEXT, 
                    last_name TEXT, 
                    address TEXT, 
                    city TEXT, 
                    state TEXT)''')

    conn.commit()
    conn.close()


def insert_data(first_name, last_name, address, city, state):
    conn = sqlite3.connect("address_book.db")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO name_address (first_name, last_name, address, city, state) VALUES (?, ?, ?, ?, ?)', (first_name, last_name, address, city, state))
    conn.commit()
    conn.close()


def get_all_entries():
    conn = sqlite3.connect("address_book.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM name_address ORDER BY first_name ASC;")
    results = cursor.fetchall()

    conn.close()
    return results


def search_entries(first_name=None, last_name=None):
    conn = sqlite3.connect("address_book.db")
    cursor = conn.cursor()

    query = "SELECT * FROM name_address WHERE 1=1"
    params = []

    if first_name:
        query += " AND first_name LIKE ?"
        params.append(f"%{first_name}%")

    if last_name:
        query += " AND last_name LIKE ?"
        params.append(f"%{last_name}%")

    cursor.execute(query, params)
    results = cursor.fetchall()
    return results


def edit_address(id, new_info):
    conn = sqlite3.connect("address_book.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE name_address SET first_name = ?, last_name = ?, address = ?, City = ?, state = ? WHERE id = ?", (*new_info, id)) 
    conn.commit()
    conn.close()


def delete_address(entry_id):
    conn = sqlite3.connect("address_book.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM name_address WHERE id = ?", (entry_id,))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    connect_db()