import itertools


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
        self.likely_plaintext_marks = self.create_likely_plaintext_marks()

    def create_likely_plaintext_marks(self):
        # Add plausible/frequent marks
        likely_plaintext_marks = ["!", " ", "\"", "\'", "(", ")", ",", ".", "-", "?", ":"]
        # for i in range(48, 58):
        #     # Add the numbers 0-9
        #     likely_plaintext_marks.append(chr(i))
        for i in range(65, 91):
            # Add english letters
            upper_case = chr(i)
            lower_case = upper_case.lower()
            likely_plaintext_marks.append(upper_case)
            likely_plaintext_marks.append(lower_case)
        return likely_plaintext_marks

    def plaintext_score(self, plaintext):
        """Scores a candidate plaintext string, higher means more likely."""
        # Return a number (int / long / float).
        # Please don't return complex numbers, that would be just annoying.
        text_len = len(plaintext)
        num_likely_marks = 0
        for char in plaintext:
            if char in self.likely_plaintext_marks:
                num_likely_marks += 1
        score = float(num_likely_marks) / text_len
        return score

    def brute_force(self, cipher_text, key_length):
        """Breaks a Repeated Key Cipher by brute-forcing all keys."""
        # Return a string.
        max_score = 0
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
            if dec_score == 1:
                print "An option:" + dec_text
        return plain_text

    def smarter_break(self, cipher_text, key_length):
        """Breaks a Repeated Key Cipher any way you like."""
        # Return a string.

        raise NotImplementedError()

# b = BreakerAssistant()
# print b.plaintext_score("\xc6\xc9u\xd0v\x14\xe2\xcf\xc5\xf5\x1eZ\x10Yd\xd3")

text_to_enc = "dagiel my dear boy"
c = RepeatedKeyCipher(key=[44, 202])
encrypted_text = c.encrypt(text_to_enc)
print encrypted_text
b = BreakerAssistant()
print b.brute_force(encrypted_text, key_length=2)

