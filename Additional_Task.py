import sqlite3
from datetime import datetime, timedelta

DATABASE_NAME = 'security_logger.db'


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.execute("PRAGMA foreign_keys = ON")
    except sqlite3.Error as e:
        print(f"Помилка підключення до БД: {e}")
    return conn


def create_tables(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS EventSources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                location TEXT,
                type TEXT
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS EventTypes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type_name TEXT UNIQUE NOT NULL,
                severity TEXT
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS SecurityEvents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                source_id INTEGER,
                event_type_id INTEGER,
                message TEXT,
                ip_address TEXT,
                username TEXT,
                FOREIGN KEY (source_id) REFERENCES EventSources(id),
                FOREIGN KEY (event_type_id) REFERENCES EventTypes(id)
            );
        """)
        conn.commit()
        print("Таблиці успішно створені або вже існують.")
    except sqlite3.Error as e:
        print(f"Помилка при створенні таблиць: {e}")


def populate_event_types(conn):
    event_types_data = [
        ("Login Success", "Informational"),
        ("Login Failed", "Warning"),
        ("Port Scan Detected", "Warning"),
        ("Malware Alert", "Critical")
    ]
    try:
        cursor = conn.cursor()
        cursor.executemany("INSERT OR IGNORE INTO EventTypes (type_name, severity) VALUES (?, ?)", event_types_data)
        conn.commit()
        print("Початкові дані для EventTypes успішно внесені.")
    except sqlite3.Error as e:
        print(f"Помилка при внесенні даних до EventTypes: {e}")


def populate_test_data(conn):
    try:
        cursor = conn.cursor()
        event_sources_data = [
            ("Firewall_Main_Office", "192.168.1.1", "Firewall"),
            ("WebServer_Prod_01", "10.0.0.5", "Web Server"),
            ("IDS_Sensor_DMZ", "172.16.0.10", "IDS"),
            ("Workstation_Admin", "192.168.1.100", "Workstation")
        ]
        cursor.executemany("INSERT OR IGNORE INTO EventSources (name, location, type) VALUES (?, ?, ?)",
                           event_sources_data)

        cursor.execute("SELECT id, type_name FROM EventTypes")
        event_types_map = {name: id for id, name in cursor.fetchall()}

        cursor.execute("SELECT id, name FROM EventSources")
        event_sources_map = {name: id for id, name in cursor.fetchall()}

        security_events_data = [
            (
            datetime(2025, 6, 2, 10, 0, 0).strftime("%Y-%m-%d %H:%M:%S"), event_sources_map.get("Firewall_Main_Office"),
            event_types_map.get("Login Failed"), "Failed login attempt for user 'admin'", "103.22.14.5", "admin"),
            (datetime(2025, 6, 1, 10, 30, 0).strftime("%Y-%m-%d %H:%M:%S"), event_sources_map.get("WebServer_Prod_01"),
             event_types_map.get("Login Success"), "User 'john_doe' logged in successfully", "192.168.1.55",
             "john_doe"),
            (datetime(2025, 6, 1, 11, 0, 0).strftime("%Y-%m-%d %H:%M:%S"), event_sources_map.get("IDS_Sensor_DMZ"),
             event_types_map.get("Port Scan Detected"), "Port scan detected from 45.67.89.12 on ports 1-1024",
             "45.67.89.12", None),
            (datetime(2025, 5, 30, 14, 22, 0).strftime("%Y-%m-%d %H:%M:%S"), event_sources_map.get("WebServer_Prod_01"),
             event_types_map.get("Malware Alert"), "Malware 'Generic.Trojan' detected in /tmp/upload.php", "10.0.0.5",
             "www-data"),
            (
            datetime(2025, 6, 2, 10, 1, 0).strftime("%Y-%m-%d %H:%M:%S"), event_sources_map.get("Firewall_Main_Office"),
            event_types_map.get("Login Failed"), "Failed login attempt for user 'root'", "103.22.14.5", "root"),
            (
            datetime(2025, 6, 2, 10, 2, 0).strftime("%Y-%m-%d %H:%M:%S"), event_sources_map.get("Firewall_Main_Office"),
            event_types_map.get("Login Failed"), "Failed login: user 'guest', bad password", "202.54.1.20", "guest"),
            (datetime(2025, 5, 31, 9, 0, 0).strftime("%Y-%m-%d %H:%M:%S"), event_sources_map.get("Workstation_Admin"),
             event_types_map.get("Login Success"), "Admin 'superuser' logged in.", "192.168.1.100", "superuser"),
            (datetime(2025, 5, 29, 16, 0, 0).strftime("%Y-%m-%d %H:%M:%S"), event_sources_map.get("WebServer_Prod_01"),
             event_types_map.get("Login Failed"), "Too many failed login attempts for 'web_api_user' from 11.22.33.44",
             "11.22.33.44", "web_api_user"),
            (datetime(2025, 6, 2, 0, 5, 0).strftime("%Y-%m-%d %H:%M:%S"), event_sources_map.get("IDS_Sensor_DMZ"),
             event_types_map.get("Malware Alert"), "Critical alert: Ransomware signature detected. IP: 10.0.0.15",
             "10.0.0.15", None),
            (
            datetime(2025, 6, 2, 8, 15, 0).strftime("%Y-%m-%d %H:%M:%S"), event_sources_map.get("Firewall_Main_Office"),
            event_types_map.get("Login Failed"), "Failed login attempt for user 'testuser'", "103.22.14.5", "testuser"),
            (
            datetime(2025, 6, 2, 8, 16, 0).strftime("%Y-%m-%d %H:%M:%S"), event_sources_map.get("Firewall_Main_Office"),
            event_types_map.get("Login Failed"), "Failed login attempt for user 'testuser2'", "103.22.14.5",
            "testuser2"),
            (
            datetime(2025, 6, 2, 8, 17, 0).strftime("%Y-%m-%d %H:%M:%S"), event_sources_map.get("Firewall_Main_Office"),
            event_types_map.get("Login Failed"), "Failed login attempt for user 'testuser3'", "103.22.14.5",
            "testuser3"),
            (
            datetime(2025, 6, 2, 8, 18, 0).strftime("%Y-%m-%d %H:%M:%S"), event_sources_map.get("Firewall_Main_Office"),
            event_types_map.get("Login Failed"), "Failed login attempt for user 'testuser4'", "103.22.14.5",
            "testuser4"),
            (
            datetime(2025, 6, 2, 8, 19, 0).strftime("%Y-%m-%d %H:%M:%S"), event_sources_map.get("Firewall_Main_Office"),
            event_types_map.get("Login Failed"), "Failed login attempt for user 'testuser5'", "103.22.14.5",
            "testuser5"),
            (
            datetime(2025, 6, 2, 8, 20, 0).strftime("%Y-%m-%d %H:%M:%S"), event_sources_map.get("Firewall_Main_Office"),
            event_types_map.get("Login Failed"), "Failed login attempt for user 'testuser6'", "103.22.14.5",
            "testuser6"),
        ]
        cursor.executemany("""
            INSERT INTO SecurityEvents (timestamp, source_id, event_type_id, message, ip_address, username)
            VALUES (?, ?, ?, ?, ?, ?)
        """, security_events_data)

        conn.commit()
        print("Тестові дані для EventSources та SecurityEvents успішно внесені.")
    except sqlite3.Error as e:
        print(f"Помилка при внесенні тестових даних: {e}")
    except KeyError as e:
        print(f"Помилка: Не знайдено ID для джерела або типу події: {e}. Перевірте назви в тестових даних.")


def register_event_source(conn, name, location, type_val):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO EventSources (name, location, type) VALUES (?, ?, ?)", (name, location, type_val))
        conn.commit()
        print(f"Джерело подій '{name}' успішно зареєстровано. ID: {cursor.lastrowid}")
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        print(f"Помилка: Джерело подій з назвою '{name}' вже існує.")
    except sqlite3.Error as e:
        print(f"Помилка при реєстрації джерела подій: {e}")
    return None


def register_event_type(conn, type_name, severity):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO EventTypes (type_name, severity) VALUES (?, ?)", (type_name, severity))
        conn.commit()
        print(f"Тип події '{type_name}' успішно зареєстровано. ID: {cursor.lastrowid}")
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        print(f"Помилка: Тип події з назвою '{type_name}' вже існує.")
    except sqlite3.Error as e:
        print(f"Помилка при реєстрації типу події: {e}")
    return None


def record_security_event(conn, source_id, event_type_id, message, ip_address=None, username=None):
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO SecurityEvents (timestamp, source_id, event_type_id, message, ip_address, username)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (current_timestamp, source_id, event_type_id, message, ip_address, username))
        conn.commit()
        print(f"Подія безпеки успішно записана. ID: {cursor.lastrowid}")
        return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        print(f"Помилка цілісності даних при записі події: {e}. Перевірте існування source_id та event_type_id.")
    except sqlite3.Error as e:
        print(f"Помилка при записі події безпеки: {e}")
    return None


def get_login_failed_last_24_hours(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM EventTypes WHERE type_name = 'Login Failed'")
        login_failed_type = cursor.fetchone()
        if not login_failed_type:
            print("Тип події 'Login Failed' не знайдено.")
            return []
        login_failed_type_id = login_failed_type[0]

        twenty_four_hours_ago = (datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            SELECT se.timestamp, es.name as source_name, se.message, se.ip_address, se.username
            FROM SecurityEvents se
            JOIN EventSources es ON se.source_id = es.id
            WHERE se.event_type_id = ? 
            AND se.timestamp >= ?
            ORDER BY se.timestamp DESC
        """, (login_failed_type_id, twenty_four_hours_ago))
        events = cursor.fetchall()
        print(f"\n--- Події 'Login Failed' за останні 24 години ({len(events)}) ---")
        for event in events:
            print(
                f"{event[0]} | Джерело: {event[1]} | IP: {event[3]} | Користувач: {event[4]} | Повідомлення: {event[2]}")
        return events
    except sqlite3.Error as e:
        print(f"Помилка при отриманні подій 'Login Failed': {e}")
        return []


def detect_bruteforce_ips(conn, failed_attempts_threshold=5, time_window_hours=1):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM EventTypes WHERE type_name = 'Login Failed'")
        login_failed_type = cursor.fetchone()
        if not login_failed_type:
            print("Тип події 'Login Failed' не знайдено.")
            return []
        login_failed_type_id = login_failed_type[0]

        time_window_ago = (datetime.now() - timedelta(hours=time_window_hours)).strftime("%Y-%m-%d %H:%M:%S")

        query = f"""
            SELECT ip_address, COUNT(id) as failed_count
            FROM SecurityEvents
            WHERE event_type_id = ?
            AND timestamp >= ?
            AND ip_address IS NOT NULL
            GROUP BY ip_address
            HAVING COUNT(id) > ?
            ORDER BY failed_count DESC
        """
        cursor.execute(query, (login_failed_type_id, time_window_ago, failed_attempts_threshold))
        suspicious_ips = cursor.fetchall()

        print(
            f"\n IP-адреси з > 5 невдалими спробами входу за останню годину. ({len(suspicious_ips)}) ---")
        for ip_info in suspicious_ips:
            print(f"IP: {ip_info[0]}, Кількість спроб: {ip_info[1]}")
        return suspicious_ips
    except sqlite3.Error as e:
        print(f"Помилка при виявленні IP для brute-force: {e}")
        return []


def get_critical_events_last_week_by_source(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM EventTypes WHERE severity = 'Critical'")
        critical_type_ids_tuples = cursor.fetchall()
        if not critical_type_ids_tuples:
            print("Типи подій з серйозністю 'Critical' не знайдено.")
            return {}
        critical_type_ids = tuple([item[0] for item in critical_type_ids_tuples])

        placeholders = ', '.join('?' for _ in critical_type_ids)
        one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")

        query = f"""
            SELECT es.name as source_name, se.timestamp, et.type_name, se.message, se.ip_address, se.username
            FROM SecurityEvents se
            JOIN EventSources es ON se.source_id = es.id
            JOIN EventTypes et ON se.event_type_id = et.id
            WHERE se.event_type_id IN ({placeholders})
            AND se.timestamp >= ?
            ORDER BY es.name, se.timestamp DESC
        """

        params = list(critical_type_ids)
        params.append(one_week_ago)
        cursor.execute(query, tuple(params))
        events = cursor.fetchall()

        grouped_events = {}
        for event in events:
            source_name = event[0]
            if source_name not in grouped_events:
                grouped_events[source_name] = []
            grouped_events[source_name].append(event[1:])

        print(f"\n Події 'Critical' за останній тиждень, згруповані за джерелом ({len(events)} всього) ---")
        for source, event_list in grouped_events.items():
            print(f"\nДжерело: {source} ({len(event_list)} подій)")
            for ev_data in event_list:
                print(
                    f"  {ev_data[0]} | Тип: {ev_data[1]} | IP: {ev_data[3]} | Користувач: {ev_data[4]} | Повідомлення: {ev_data[2]}")
        return grouped_events
    except sqlite3.Error as e:
        print(f"Помилка при отриманні 'Critical' подій: {e}")
        return {}


def find_events_by_keyword(conn, keyword):
    try:
        cursor = conn.cursor()
        search_term = f"%{keyword}%"
        cursor.execute("""
            SELECT se.timestamp, es.name as source_name, et.type_name as event_type, se.message, se.ip_address, se.username
            FROM SecurityEvents se
            JOIN EventSources es ON se.source_id = es.id
            JOIN EventTypes et ON se.event_type_id = et.id
            WHERE se.message LIKE ?
            ORDER BY se.timestamp DESC
        """, (search_term,))
        events = cursor.fetchall()
        print(f"\n Події, що містять '{keyword}' у повідомленні ({len(events)}) ---")
        for event in events:
            print(
                f"{event[0]} | Джерело: {event[1]} | Тип: {event[2]} | IP: {event[4]} | Користувач: {event[5]} | Повідомлення: {event[3]}")
        return events
    except sqlite3.Error as e:
        print(f"Помилка при пошуку подій за ключовим словом: {e}")
        return []


if __name__ == "__main__":
    conn = create_connection()
    if conn:
        create_tables(conn)
        populate_event_types(conn)
        # populate_test_data(conn)

        while True:
            print("\nСистема Логування Подій Безпеки:")
            print("1. Зареєструвати нове джерело подій")
            print("2. Зареєструвати новий тип подій")
            print("3. Записати нову подію безпеки")
            print("4. Показати 'Login Failed' за останні 24 години")
            print("5. Виявити IP-адреси з > 5 невдалих спроб входу за 1 годину")
            print("6. Показати 'Critical' події за останній тиждень (згруповані)")
            print("7. Знайти події за ключовим словом у повідомленні")
            print("0. Вийти")

            choice = input("Ваш вибір: ")

            if choice == '1':
                name = input("Введіть назву джерела: ")
                location = input("Введіть місцезнаходження/IP джерела: ")
                type_val = input("Введіть тип джерела (наприклад, Firewall, Web Server): ")
                register_event_source(conn, name, location, type_val)
            elif choice == '2':
                type_name = input("Введіть назву типу події: ")
                severity = input("Введіть серйозність (Informational, Warning, Critical): ")
                register_event_type(conn, type_name, severity)
            elif choice == '3':
                try:
                    source_id_str = input("Введіть ID джерела події (або назву джерела): ")
                    event_type_id_str = input("Введіть ID типу події (або назву типу): ")
                    message = input("Введіть повідомлення події: ")
                    ip_address = input("Введіть IP-адресу (або Enter, якщо немає): ") or None
                    username = input("Введіть ім'я користувача (або Enter, якщо немає): ") or None

                    final_source_id = None
                    if source_id_str.isdigit():
                        final_source_id = int(source_id_str)
                    else:
                        cursor = conn.cursor()
                        cursor.execute("SELECT id FROM EventSources WHERE name = ?", (source_id_str,))
                        res = cursor.fetchone()
                        if res:
                            final_source_id = res[0]
                        else:
                            print(f"Джерело з назвою '{source_id_str}' не знайдено.")

                    final_event_type_id = None
                    if event_type_id_str.isdigit():
                        final_event_type_id = int(event_type_id_str)
                    else:
                        cursor = conn.cursor()
                        cursor.execute("SELECT id FROM EventTypes WHERE type_name = ?", (event_type_id_str,))
                        res = cursor.fetchone()
                        if res:
                            final_event_type_id = res[0]
                        else:
                            print(f"Тип події з назвою '{event_type_id_str}' не знайдено.")

                    if final_source_id is not None and final_event_type_id is not None:
                        record_security_event(conn, final_source_id, final_event_type_id, message, ip_address, username)
                    else:
                        print("Не вдалося записати подію через невірні ID/назви джерела або типу.")

                except ValueError:
                    print("Невірний ID. Будь ласка, введіть число для ID.")
                except sqlite3.Error as e:
                    print(f"Помилка БД: {e}")

            elif choice == '4':
                get_login_failed_last_24_hours(conn)
            elif choice == '5':
                print("Виявлення IP-адрес з >5 невдалими спробами входу за останню 1 годину...")
                detect_bruteforce_ips(conn)
            elif choice == '6':
                get_critical_events_last_week_by_source(conn)
            elif choice == '7':
                keyword = input("Введіть ключове слово для пошуку: ")
                find_events_by_keyword(conn, keyword)
            elif choice == '0':
                print("Вихід з програми.")
                break
            else:
                print("Невірний вибір. Спробуйте ще раз.")

        conn.close()
    else:
        print("Не вдалося підключитися до бази даних.")