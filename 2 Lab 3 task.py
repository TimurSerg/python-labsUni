def filter_ips(input_file_path, output_file_path, allowed_ips):
    ip_count = {}

    try:
        with open(input_file_path, 'r') as input_file:
            for line in input_file:
                parts = line.split()
                if parts:
                    ip = parts[0]
                    if ip in allowed_ips:
                        ip_count[ip] = ip_count.get(ip, 0) + 1

        with open(output_file_path, 'w') as output_file:
            for ip, count in ip_count.items():
                output_line = f"{ip} - {count}\n"
                output_file.write(output_line)
                print(output_line.strip())

        print(f"Результати записано в {output_file_path}")

    except FileNotFoundError:
        print(f" Файл {input_file_path} не знайдено.")
    except IOError as e:
        print(f" Помилка при записі в файл {output_file_path}: {e}")


allowed_ips = ['83.149.9.216', '93.114.45.13']
filter_ips('/Applications/PyCharm CE.app/Contents/apache_logs.txt',
           '/Users/timursergeev/PycharmProjects/python-labsUni/output_ips.txt', allowed_ips)