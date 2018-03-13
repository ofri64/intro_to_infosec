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
        # self.english_letters = [chr(i) for i in range(ord('a'), ord('z')+1)] + [chr(i) for i in range(ord('A'), ord("Z")+1)]
        # self.english_punc = ["!", " ", "\"", "\'", "(", ")", ",", ".", "-", "?", ":"]
        # self.english_letter_frequency = {
        #     'a': 0.11682, 'b': 0.04434, 'c': 0.05238, 'd': 0.03174, 'e': 0.02799, 'f': 0.04027, 'g': 0.01642,
        #     'h': 0.042, 'i': 0.07294, 'j': 0.00511, 'k': 0.00456, 'l': 0.02415, 'm': 0.03826, 'n': 0.02284,
        #     'o': 0.07631, 'p': 0.04319, 'q': 0.00222, 'r': 0.02826, 's': 0.06686, 't': 0.15978, 'u': 0.01183,
        #     'v': 0.00824, 'w': 0.05497, 'x': 0.00045, 'y': 0.00763, 'z': 0.00045}

    def english_letter_proportion(self, plain_text):
        text_len = len(plain_text)
        letters_count = 0
        for char in plain_text:
            if char in self.english_letters:
                letters_count += 1
        letter_prop = float(letters_count) / text_len
        return letter_prop

    def plaintext_score(self, plaintext):
        """Scores a candidate plaintext string, higher means more likely."""
        # Return a number (int / long / float).
        # Please don't return complex numbers, that would be just annoying.
        raise NotImplementedError()

    def brute_force(self, cipher_text, key_length):
        """Breaks a Repeated Key Cipher by brute-forcing all keys."""
        # Return a string.
        max_score = -10000000 # need to change it
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
        return plain_text

    def smarter_break(self, cipher_text, key_length):
        """Breaks a Repeated Key Cipher any way you like."""
        # Return a string.

        raise NotImplementedError()

