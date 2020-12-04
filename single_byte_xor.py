class SingleByteXor:
    @staticmethod
    def encrypt(text_b: bytearray, key_b: int):
        text_b = text_b[:]
        for i in range(len(text_b)):
            text_b[i] ^= key_b
        return text_b

    @staticmethod
    def decrypt(encrypted_text_b: bytearray, key_b: int):
        return SingleByteXor.encrypt(encrypted_text_b, key_b)


class SingleByteXorAttacker:
    FREQUENCIES_ENG = {
        'a': 8.2, 'b': 1.5, 'c': 2.8, 'd': 4.3, 'e': 13, 'f': 2.2, 'g': 2, 'h': 6.1, 'i': 7, 'j': 0.15, 'k': 0.77,
        'l': 4, 'm': 2.4, 'n': 6.7, 'o': 7.5, 'p': 1.9, 'q': 0.095, 'r': 6, 's': 6.3, 't': 9.1, 'u': 2.8, 'v': 0.98,
        'w': 2.4, 'x': 0.15, 'y': 2, 'z': 0.074,
    }

    @staticmethod
    def attack(encrypted_text: str):
        encrypted_text_b = bytearray(encrypted_text.encode())
        for key in SingleByteXorAttacker.get_possible_keys(encrypted_text_b):
            print(f"Key: {bytearray([key]).decode(errors='replace')}")
            print(f"Decrypted text: {SingleByteXor.decrypt(encrypted_text_b, key).decode(errors='replace')}")

    @staticmethod
    def get_possible_keys(encrypted_text_b: bytearray):
        fitting_coefficient = 1000000
        possible_keys = []

        for key in range(0, 256):
            possible_decrypted_message = SingleByteXor.decrypt(encrypted_text_b, key)
            current_fitting_coefficient = SingleByteXorAttacker.get_fitting_coefficient(possible_decrypted_message)
            if current_fitting_coefficient < fitting_coefficient:
                fitting_coefficient = current_fitting_coefficient
                possible_keys.clear()
                possible_keys.append(key)
            elif current_fitting_coefficient == fitting_coefficient:
                possible_keys.append(key)
        return possible_keys

    @staticmethod
    def get_fitting_coefficient(text_b: bytearray):
        deviation_sum = 0
        for key, value in SingleByteXorAttacker.FREQUENCIES_ENG.items():
            letter_frequency = sum(int(letter == key.encode()[0]) * 100 / len(text_b) for letter in text_b)
            deviation_sum += abs(letter_frequency - value)

        return deviation_sum / len(SingleByteXorAttacker.FREQUENCIES_ENG.items())
