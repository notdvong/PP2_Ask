import csv
from connect import get_connection, setup_database

def import_from_csv(filename):
    conn = get_connection()
    if not conn: return

    try:
        cur = conn.cursor()
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader) 
            
            for row in reader:
                cur.execute(
                    "INSERT INTO contacts (first_name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING", 
                    (row[0], row[1])
                )
        conn.commit()
        print(f"Successfully imported contacts from {filename}")
        cur.close()
    except FileNotFoundError:
        print(f"Error: Could not find file {filename}")
    except Exception as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

def insert_contact(name, phone):
    conn = get_connection()
    if not conn: return

    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO contacts (first_name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()
        print(f"Contact '{name}' added successfully!")
        cur.close()
    except Exception as e:
        print(f"Error adding contact (Phone might already exist): {e}")
    finally:
        conn.close()

def update_contact(old_name, new_name, new_phone):
    conn = get_connection()
    if not conn: return

    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE contacts SET first_name = %s, phone = %s WHERE first_name = %s", 
            (new_name, new_phone, old_name)
        )
        if cur.rowcount > 0:
            conn.commit()
            print(f"Contact '{old_name}' updated successfully!")
        else:
            print("Contact not found.")
        cur.close()
    except Exception as e:
        print(f"Error updating contact: {e}")
    finally:
        conn.close()

def query_contacts(search_type, search_term):
    conn = get_connection()
    if not conn: return

    try:
        cur = conn.cursor()
        if search_type == "name":
            cur.execute("SELECT first_name, phone FROM contacts WHERE first_name ILIKE %s", (f"%{search_term}%",))
        elif search_type == "phone":
            cur.execute("SELECT first_name, phone FROM contacts WHERE phone LIKE %s", (f"{search_term}%",))
        else:
            print("Invalid search type.")
            return

        results = cur.fetchall()
        if results:
            print("\n--- Search Results ---")
            for row in results:
                print(f"Name: {row[0]} | Phone: {row[1]}")
            print("----------------------\n")
        else:
            print("No contacts found.")
        cur.close()
    except Exception as e:
        print(f"Error querying contacts: {e}")
    finally:
        conn.close()

def delete_contact(search_term):
    conn = get_connection()
    if not conn: return

    try:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM contacts WHERE first_name = %s OR phone = %s", 
            (search_term, search_term)
        )
        if cur.rowcount > 0:
            conn.commit()
            print("Contact deleted successfully.")
        else:
            print("No matching contact found to delete.")
        cur.close()
    except Exception as e:
        print(f"Error deleting contact: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    setup_database() 
    
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Add from CSV")
        print("2. Add Contact manually")
        print("3. Update Contact")
        print("4. Search Contacts")
        print("5. Delete Contact")
        print("6. Exit")
        
        choice = input("Select an option (1-6): ")
        
        if choice == '1':
            import_from_csv('contacts.csv')
            
        elif choice == '2':
            name = input("Enter First Name: ")
            phone = input("Enter Phone Number: ")
            insert_contact(name, phone)
            
        elif choice == '3':
            old_name = input("Enter the current First Name of the contact to update: ")
            new_name = input("Enter NEW First Name: ")
            new_phone = input("Enter NEW Phone Number: ")
            update_contact(old_name, new_name, new_phone)
            
        elif choice == '4':
            s_type = input("Search by 'name' or 'phone' prefix?: ").strip().lower()
            term = input("Enter search term: ")
            query_contacts(s_type, term)
            
        elif choice == '5':
            term = input("Enter the exact name OR phone number to delete: ")
            delete_contact(term)
            
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")