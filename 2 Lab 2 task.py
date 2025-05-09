import hashlib

def generate_file_hashes(*file_paths):
    hash_dict = {}

    for file_path in file_paths:
        try:
            with open(file_path, 'rb') as file:
                sha256_hash = hashlib.sha256()
                for byte_block in iter(lambda: file.read(4096), b""):
                    sha256_hash.update(byte_block)
                hash_dict[file_path] = sha256_hash.hexdigest()
        except FileNotFoundError:
            print(f" Файл {file_path} не знайдено.")
        except IOError:
            print(f" Помилка при читанні файлу {file_path}.")

    return hash_dict

file_hashes = generate_file_hashes('/Applications/PyCharm CE.app/Contents/apache_logs.txt')
print(file_hashes)