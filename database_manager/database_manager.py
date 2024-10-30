import os
import sqlite3

# Creating the folder (Klasörün oluşturulması)
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"{directory}  folder created (klasörü oluşturuldu).")
    else:
        print(f"{directory} folder already exists. (klasörü zaten mevcut.)")

# Set the path to the database file (Veritabanı dosyasının yolunu ayarlayın)
def get_db_path(directory, db_name='animals.db'):
    return os.path.join(directory, db_name)

# Database and table creation (Veritabanı ve tablo oluşturma)
def setup_database(directory):
    db_path = get_db_path(directory)

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute('''
        CREATE TABLE IF NOT EXISTS animals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hayvan_cinsi TEXT NOT NULL,
            hayvan_adi TEXT NOT NULL,
            sahip_adi TEXT NOT NULL,
            telefon_no TEXT NOT NULL,
            UNIQUE(hayvan_adi, sahip_adi)
        )
        ''')

        conn.commit()
        conn.close()
        print(f"database (Veritabanı) '{db_path}' created (oluşturuldu.)")
    except sqlite3.OperationalError as e:
        print(f"Could not create database (Veritabanı oluşturulamadı): {e}")

#Adding data to the database (Veritabanına veri ekleme)
def insert_data(directory, hayvan_cinsi, hayvan_adi, sahip_adi, telefon_no):
    db_path = get_db_path(directory)

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        try:
            c.execute('''
            INSERT INTO animals (hayvan_cinsi, hayvan_adi, sahip_adi, telefon_no)
            VALUES (?, ?, ?, ?)
            ''', (hayvan_cinsi, hayvan_adi, sahip_adi, telefon_no))
            conn.commit()
            print("Data added successfully (Veri başarıyla eklendi).")
        except sqlite3.IntegrityError:
            print(f"Data already exists (Veri zaten mevcut:) {hayvan_adi} - {sahip_adi}")

        conn.close()
    except sqlite3.OperationalError as e:
        print(f"Failed to insert data: (Veri eklenemedi:) {e}")

# Querying data in the database (Veritabanındaki verileri sorgulama)
def read_database(directory):
    db_path = get_db_path(directory)

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute('SELECT * FROM animals')
        rows = c.fetchall()

        conn.close()

        print("Database content: (Veritabanı içeriği:)")
        for row in rows:
            print(row)
    except sqlite3.OperationalError as e:
        print(f"Failed to query data: (Veri sorgulanamadı:) {e}")

# Delete data from database (Veritabanından veri silme)
def delete_data(directory, hayvan_adi, sahip_adi):
    db_path = get_db_path(directory)

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute('''
        DELETE FROM animals WHERE hayvan_adi = ? AND sahip_adi = ?
        ''', (hayvan_adi, sahip_adi))
        conn.commit()

        if c.rowcount > 0:
            print(f"{hayvan_adi} and (ve) {sahip_adi} Data matching was successfully deleted (ile eşleşen veri başarıyla silindi.)")
        else:
            print(f"{hayvan_adi} and (ve) {sahip_adi} No data matching was found. (ile eşleşen veri bulunamadı.)")

        conn.close()
    except sqlite3.OperationalError as e:
        print(f"Data could not be deleted:(Veri silinemedi:) {e}")

# Update data in the database (Veritabanındaki verileri güncelleme)
def update_data(directory, old_hayvan_adi, old_sahip_adi, new_hayvan_cinsi, new_hayvan_adi, new_sahip_adi, new_telefon_no):
    db_path = get_db_path(directory)

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute('''
        UPDATE animals
        SET hayvan_cinsi = ?, hayvan_adi = ?, sahip_adi = ?, telefon_no = ?
        WHERE hayvan_adi = ? COLLATE NOCASE AND sahip_adi = ? COLLATE NOCASE
        ''', (new_hayvan_cinsi, new_hayvan_adi, new_sahip_adi, new_telefon_no, old_hayvan_adi, old_sahip_adi))
        conn.commit()

        if c.rowcount > 0:
            print(f"{old_hayvan_adi} and (ve) {old_sahip_adi} The data matching was successfully updated. (ile eşleşen veri başarıyla güncellendi.)")
        else:
            print(f"{old_hayvan_adi} and (ve) {old_sahip_adi} No data matching was found. (ile eşleşen veri bulunamadı.)")

        conn.close()
    except sqlite3.OperationalError as e:
        print(f"Failed to update data:(Veri güncellenemedi:) {e}")

# Querying a specific animal in the database (Veritabanında belirli bir hayvanı sorgulama)
def search_animal_by_name(directory, hayvan_adi):
    db_path = get_db_path(directory)

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        c.execute('SELECT * FROM animals WHERE hayvan_adi = ? COLLATE NOCASE', (hayvan_adi,))
        matching_rows = c.fetchall()

        conn.close()

        return matching_rows
    except sqlite3.OperationalError as e:
        print(f"database error: (Veritabanı hatası:) {e}")
        return []

# Ana program
if __name__ == "__main__":
    directory = 'database'

    # Create folder (Klasörü oluştur)
    create_directory(directory)

    # Create database and table (Veritabanı ve tabloyu oluştur)
    setup_database(directory)

    # Operation selection from the user (Kullanıcıdan işlem seçimi)
    while True:
        print("\n1. Add data (Veri ekle)")
        print("2. List Data (Verileri listele)")
        print("3. delete data (Veri sil)")
        print("4. Update Data (Veri güncelle)")
        print("5. Search for animals (Hayvan ara)")
        print("6. Exit(Çıkış)")
        choice = input("Choose an action: (Bir işlem seçin:) ")

        if choice == '1':
            hayvan_cinsi = input("enter the animal breed (Hayvan cinsini girin:) ")
            hayvan_adi = input("Enter animal name: (Hayvan adını girin:) ")
            sahip_adi = input("Enter owner name (Sahip adını girin:) ")
            telefon_no = input("Enter phone number: (Telefon numarasını girin:) ")
            insert_data(directory, hayvan_cinsi, hayvan_adi, sahip_adi, telefon_no)

        elif choice == '2':
            read_database(directory)

        elif choice == '3':
            hayvan_adi = input("Enter the animal name you want to delete: (Silmek istediğiniz hayvan adını girin:) ")
            sahip_adi = input("Enter the name of the owner you want to delete: (Silmek istediğiniz sahibin adını girin:) ")
            delete_data(directory, hayvan_adi, sahip_adi)

        elif choice == '4':
            old_hayvan_adi = input("Enter the old pet name you want to update: (Güncellemek istediğiniz eski hayvan adını girin:) ")
            old_sahip_adi = input("Enter the name of the previous owner you want to update: (Güncellemek istediğiniz eski sahibin adını girin:) ")
            new_hayvan_cinsi = input("Enter the new animal breed: (Yeni hayvan cinsini girin:) ")
            new_hayvan_adi = input("Enter new pet name: (Yeni hayvan adını girin:) ")
            new_sahip_adi = input("Enter the new owner's name: (Yeni sahibin adını girin:) ")
            new_telefon_no = input("Enter the new phone number: (Yeni telefon numarasını girin:) ")
            update_data(directory, old_hayvan_adi, old_sahip_adi, new_hayvan_cinsi, new_hayvan_adi, new_sahip_adi, new_telefon_no)

        elif choice == '5':
            hayvan_adi = input("Enter the animal name you want to search for: (Aramak istediğiniz hayvan adını girin:) ")
            results = search_animal_by_name(directory, hayvan_adi)
            if results:
                for row in results:
                    print(row)
            else:
                print(f"{hayvan_adi} The animal named could not be found. (adlı hayvan bulunamadı.)")

        elif choice == '6':
            break

        else:
            print("Invalid selection. Please try again. (Geçersiz seçim. Lütfen tekrar deneyin.)")
