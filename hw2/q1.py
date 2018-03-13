import itertools
import math


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

    def __init__(self):
        """Initializes BreakerAssistant object, Used to define object attribute for plaintext score"""
        self.english_letters_frequency = {
            'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702, 'f': 0.02228, 'g': 0.02015,
            'h': 0.06094, 'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025, 'm': 0.02406, 'n': 0.06749,
            'o': 0.07507, 'p': 0.01929, 'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056, 'u': 0.02758,
            'v': 0.00978, 'w': 0.0236, 'x': 0.0015, 'y': 0.01974, 'z': 0.00074}

    def _text_letters_proportion(self, plain_text):
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
        return -self._chi_square_statistical(plaintext)

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

    def smarter_break(self, cipher_text, key_length):
        """Breaks a Repeated Key Cipher any way you like."""
        # Return a string.

        raise NotImplementedError()

# rp = RepeatedKeyCipher(key=[50, 179])
# b = BreakerAssistant()
# m = "Hello my name is Dagi. statistically this text must be long unless there is a chance the method won't work well"
# enc = rp.encrypt(m)
# print enc
# dec = b.brute_force(enc, 2)
# print dec
