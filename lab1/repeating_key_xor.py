import base64
from single_byte_xor import SingleByteXorAttacker


class RepeatingKeyXor:
    @staticmethod
    def encrypt(text_b: bytearray, key_b: bytearray):
        text_b = text_b[:]
        for i in range(len(text_b)):
            text_b[i] ^= key_b[i % len(key_b)]
        return text_b

    @staticmethod
    def decrypt(encrypted_text_b: bytearray, key_b: bytearray):
        return RepeatingKeyXor.encrypt(encrypted_text_b, key_b)


class RepeatingKeyXorAttacker:
    @staticmethod
    def attack(encrypted_text):
        encrypted_text_b = bytearray.fromhex(encrypted_text)
        for key in RepeatingKeyXorAttacker.get_possible_keys(encrypted_text_b):
            print(f"Key: {key.decode(errors='replace')}")
            print(f"Decrypted text: {RepeatingKeyXor.decrypt(encrypted_text_b, key).decode(errors='replace')}")

    @staticmethod
    def get_possible_keys(encrypted_text_b: bytearray):
        key_length = RepeatingKeyXorAttacker.get_key_length(encrypted_text_b)
        possible_keys = []

        for i in range(0, key_length):
            message_part = bytearray([letter for j, letter in enumerate(encrypted_text_b) if j % key_length == i])
            message_part_possible_keys = SingleByteXorAttacker.get_possible_keys(message_part)
            new_possible_keys = []
            for part_key in message_part_possible_keys:
                for key in possible_keys:
                    new_key = key[:]
                    new_key.append(part_key)
                    new_possible_keys.append(new_key)
                if not possible_keys:
                    new_key = [part_key]
                    new_possible_keys.append(new_key)
            possible_keys = new_possible_keys
        return [bytearray(key) for key in possible_keys]

    @staticmethod
    def get_key_length(encrypted_text_b: bytearray):
        coincidence_indexes = {}

        for key_length in range(1, len(encrypted_text_b)):
            cmp_text = []
            cmp_text.extend(encrypted_text_b[-key_length:])
            cmp_text.extend(encrypted_text_b[:len(encrypted_text_b) - key_length])
            matches = 0
            for i in range(0, len(encrypted_text_b)):
                if encrypted_text_b[i] == cmp_text[i]:
                    matches += 1
            coincidence_indexes[key_length] = matches / len(encrypted_text_b)

        max_index = 0
        key_length = -1

        for key, value in coincidence_indexes.items():
            if value > max_index and key < 10:
                max_index = value
                key_length = key
        return key_length
