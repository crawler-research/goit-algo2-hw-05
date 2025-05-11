import hashlib

class BloomFilter:
    def __init__(self, num_hashes=3):
        self.size = 1000
        self.bit_array = [0] * 1000
        self.num_hashes = num_hashes
        
    def _hash(self, item, seed):
        if isinstance(item, str):
            item = item.encode('utf-8')
        elif not isinstance(item, bytes):
            item = str(item).encode('utf-8')
        
        h = hashlib.md5(item)
        h.update(str(seed).encode('utf-8'))
        return int(h.hexdigest(), 16) % self.size
    
    def add(self, item):
        for i in range(self.num_hashes):
            index = self._hash(item, i)
            self.bit_array[index] = 1
    
    def check(self, item):
        for i in range(self.num_hashes):
            index = self._hash(item, i)
            if self.bit_array[index] == 0:
                return False
        return True

def check_password_uniqueness(bloom_filter, passwords):
    """Check the uniqueness of passwords using a Bloom filter"""
    results = {}
    
    for password in passwords:
        if not password:
            results[password] = "некоректний"
            continue
            
        if bloom_filter.check(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom_filter.add(password)
            
    return results

if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")