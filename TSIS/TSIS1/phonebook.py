import json
import csv
from connect import get_connection

def execute_query(query, params=(), fetch=True):
    conn = get_connection()
    if not conn: return None
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if fetch:
                result = cur.fetchall()
                conn.commit()
                return result
            conn.commit()
    except Exception as e:
        print(f"Database Error: {e}")
    finally:
        conn.close()

def add_new_contact():
    name = input("Enter Name: ")
    email = input("Enter Email: ")
    birthday = input("Enter Birthday (YYYY-MM-DD) or blank: ").strip() or None
    
    group_name = input("Enter Group (e.g., Family, Work) or blank: ").strip() or None 
    
    phone = input("Enter Phone Number: ")
    p_type = input("Phone Type (home, work, mobile): ").lower()
    
    conn = get_connection()
    if not conn: return
    try:
        with conn.cursor() as cur:
            group_id = None
            if group_name:
                cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET name=EXCLUDED.name RETURNING id", (group_name,))
                group_id = cur.fetchone()[0]

            cur.execute("INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s, %s, %s, %s) RETURNING id", 
                        (name, email, birthday, group_id))
            contact_id = cur.fetchone()[0]
            
            cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)", 
                        (contact_id, phone, p_type))
            
            conn.commit()
            print(f"Contact '{name}' added successfully!")
    except Exception as e: 
        print(f"Failed to add contact: {e}")
    finally: 
        conn.close()
        
def delete_contact():
    name = input("Enter the name of the contact to delete: ")
    execute_query("DELETE FROM contacts WHERE name = %s", (name,), fetch=False)
    print(f"Deleted {name}.")

def paginated_view():
    limit, offset = 3, 0
    sort_by = "c.name"
    group_filter = None

    while True:
        query = """
            SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type 
            FROM contacts c 
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
        """
        params = []
        if group_filter:
            query += " WHERE g.name ILIKE %s"
            params.append(f"%{group_filter}%")
            
        query += f" ORDER BY {sort_by} LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        results = execute_query(query, tuple(params))
        
        print(f"\n--- PAGE {(offset//limit) + 1} (Sorted by: {sort_by}) ---")
        if not results: 
            print("No records found.")
        else:
            for r in results:
                print(f"Name: {r[0]} | Email: {r[1]} | Bday: {r[2]} | Group: {r[3]} | Phone: {r[4]} ({r[5]})")
                
        action = input("\n[n]ext, [p]rev, [s]ort, [f]ilter group, [c]lear filter, [q]uit: ").lower()
        if action == 'n': offset += limit
        elif action == 'p' and offset >= limit: offset -= limit
        elif action == 's':
            sort_opt = input("Sort by (1) Name, (2) Birthday: ")
            if sort_opt == '1': sort_by = "c.name"
            elif sort_opt == '2': sort_by = "c.birthday"
            offset = 0
        elif action == 'f':
            group_filter = input("Enter group name to filter by: ")
            offset = 0
        elif action == 'c':
            group_filter = None
            offset = 0
        elif action == 'q': break

def search_contacts_db():
    term = input("Search by name, email, or phone: ")
    results = execute_query("SELECT * FROM search_contacts(%s)", (term,))
    if results:
        for r in results: print(f"Found: {r[0]} | Email: {r[1]} | Phone: {r[2]} ({r[3]})")
    else: print("No matches.")

def export_to_json():
    query = """
        SELECT c.name, c.email, TO_CHAR(c.birthday, 'YYYY-MM-DD'), g.name, 
               COALESCE(json_agg(json_build_object('phone', p.phone, 'type', p.type)) FILTER (WHERE p.phone IS NOT NULL), '[]')
        FROM contacts c LEFT JOIN groups g ON c.group_id = g.id LEFT JOIN phones p ON c.id = p.contact_id GROUP BY c.id, g.name;
    """
    rows = execute_query(query)
    data = [{"name": r[0], "email": r[1], "birthday": r[2], "group": r[3], "phones": r[4]} for r in rows] if rows else []
    with open("contacts.json", 'w') as f: json.dump(data, f, indent=4)
    print("Exported to contacts.json")

def import_from_json():
    filename = input("Enter JSON filename (e.g., contacts.json): ")
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return

    conn = get_connection()
    if not conn: return
    cur = conn.cursor()

    for entry in data:
        name = entry.get('name')
        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        existing = cur.fetchone()
        
        if existing:
            choice = input(f"Contact '{name}' exists. (s)kip or (o)verwrite? ").lower()
            if choice == 's': continue
            else: cur.execute("DELETE FROM contacts WHERE id = %s", (existing[0],))
        
        group_name = entry.get('group')
        group_id = None
        if group_name:
            cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET name=EXCLUDED.name RETURNING id", (group_name,))
            group_id = cur.fetchone()[0]

        cur.execute("INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s, %s, %s, %s) RETURNING id",
                    (name, entry.get('email'), entry.get('birthday'), group_id))
        c_id = cur.fetchone()[0]

        for p in entry.get('phones', []):
            cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)", 
                        (c_id, p.get('phone'), p.get('type')))

    conn.commit()
    cur.close()
    conn.close()
    print("JSON Import finished.")

def main_menu():
    while True:
        print("\n--- ASKAR'S PHONEBOOK ---")
        print("1. Add Contact")
        print("2. View / Sort / Filter Contacts")
        print("3. Search (PL/pgSQL)")
        print("4. Export JSON")
        print("5. Import JSON")
        print("6. Delete Contact")
        print("7. Quit")
        
        choice = input("Option: ")
        if choice == '1': add_new_contact()
        elif choice == '2': paginated_view()
        elif choice == '3': search_contacts_db()
        elif choice == '4': export_to_json()
        elif choice == '5': import_from_json()
        elif choice == '6': delete_contact()
        elif choice == '7': break

if __name__ == "__main__":
    main_menu()