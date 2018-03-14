import itertools
import math
import string


class RepeatedKeyCipher(object):

    def __init__(self, key=[0, 0, 0, 0, 0]):
        """Initializes the object with a list of integers between 0 and 255."""
        assert all(0 <= k <= 255 and isinstance(k, (int, long)) for k in key)
        self.key = key

    def encrypt(self, plaintext):
        """Encrypts a given plaintext string and returns the ciphertext."""
        # Return a string, NOT an array of integers.
        key_len = len(self.key)
        cipher_text = ""
        for i in range(len(plaintext)):
            key_byte = self.key[i % key_len]
            plain_text_byte = ord(plaintext[i])
            cipher_text_byte = key_byte ^ plain_text_byte
            cipher_text += chr(cipher_text_byte)
        return cipher_text

    def decrypt(self, ciphertext):
        """Decrypts a given ciphertext string and returns the plaintext."""
        # Return a string, NOT an array of integers.
        return self.encrypt(ciphertext)


class BreakerAssistant(object):
    NON_PRINTABLE_PENALTY = 0.3

    def __init__(self):
        """Initializes BreakerAssistant object, Used to define object attribute for plaintext score"""
        self.english_letters_frequency = {
            'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702, 'f': 0.02228, 'g': 0.02015,
            'h': 0.06094, 'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025, 'm': 0.02406, 'n': 0.06749,
            'o': 0.07507, 'p': 0.01929, 'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056, 'u': 0.02758,
            'v': 0.00978, 'w': 0.0236, 'x': 0.0015, 'y': 0.01974, 'z': 0.00074}

    def _text_letters_proportion(self, plain_text):
        """Computed the distribution of english letters in a given text"""
        english_letters = [chr(i) for i in range(97,123)]
        text_frequency = {letter: 0 for letter in english_letters}
        text_len = len(plain_text)
        for char in plain_text:
            char_lowercase = char.lower()
            if char.lower() in text_frequency:
                text_frequency[char_lowercase] += 1
        text_frequency = {i[0]: float(i[1])/text_len for i in text_frequency.items()}
        return text_frequency


    def _chi_square_statistical(self, plain_text):
        """Compute the chi-square statistical value. for more details see q1c.txt"""
        english_freq = self.english_letters_frequency
        text_freq = self._text_letters_proportion(plain_text)
        # Compute chi square value - compare text distribution to expected one
        chi_square = 0
        for letter in english_freq.keys():
            letter_freq = english_freq[letter]
            text_letter_freq = text_freq[letter]
            freq_diff = letter_freq - text_letter_freq
            chi_square += math.pow(freq_diff, 2) / letter_freq
        return chi_square

    def plaintext_score(self, plaintext):
        """Scores a candidate plaintext string, higher means more likely."""
        # Return a number (int / long / float).
        # Please don't return complex numbers, that would be just annoying.
        penaly = 0 # Add penalty for non printable characters
        penalty = 0
        for char in plaintext:
            if char not in string.printable:
                penalty += BreakerAssistant.NON_PRINTABLE_PENALTY
        return -self._chi_square_statistical(plaintext) - penalty

    def brute_force(self, cipher_text, key_length):
        """Breaks a Repeated Key Cipher by brute-forcing all keys."""
        # Return a string.
        max_score = -100000
        plain_text = ""
        cipher = RepeatedKeyCipher()

        # enumerate over all possible keys using itertools
        for key in itertools.product(range(256), repeat=key_length):
            cipher.key = key
            dec_text = cipher.decrypt(cipher_text)
            dec_score = self.plaintext_score(dec_text)
            if dec_score > max_score:
                max_score = dec_score
                plain_text = dec_text
        return plain_text.lower()

    def _divide_cipher_by_key_byte(self, cipher_text, key_length):
        """Divide the text to n=key_length texts encrypted with the same byte.
        Enables us to perform statistical analysis for each byte separately"""
        key_byte_texts = ["" for i in range(key_length)]
        for i in range(len(cipher_text)):
            key_byte_texts[i % key_length] += cipher_text[i]
        return key_byte_texts

    def _concatenate_key_byte_decrypted(self, decrypted_key_byte_text, cipher_length, key_length):
        """Concatenate the encrypted texts by key byte together the create the decrypted text"""
        decrypted_text = ""
        num_round = 0
        byte = 0
        for i in range(cipher_length):
            decrypted_text += decrypted_key_byte_text[byte][num_round]
            byte = (byte + 1) % key_length
            if byte == 0:
                num_round += 1
        return decrypted_text

    def smarter_break(self, cipher_text, key_length):
        """Breaks a Repeated Key Cipher any way you like."""
        # Return a string.
        cipher_key_byte_texts = self._divide_cipher_by_key_byte(cipher_text, key_length)
        decrypted_key_byte_text = []

        # Perform "brute force" with the corresponding text for each byte in the key
        for text in cipher_key_byte_texts:
            decrypted_key_byte_text.append(self.brute_force(text, key_length=1))

        # Concatenate all the encrypted texts together
        decrypted_text = self._concatenate_key_byte_decrypted(decrypted_key_byte_text, len(cipher_text), key_length)
        return decrypted_text