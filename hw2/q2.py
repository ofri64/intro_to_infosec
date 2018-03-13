from q2_atm import ATM, ServerResponse
import itertools
import math

NUM_DIGITS_PIN = 4


def convert_digits_array_to_int(digits_array):
    num = 0
    exp = len(digits_array) - 1
    for d in digits_array:
        num += 10**exp * d
        exp -= 1
    return num


def create_all_possible_PIN():
    codes = list(itertools.product(range(10), repeat=NUM_DIGITS_PIN))
    return codes


def extract_PIN(encrypted_PIN):
    """Extracts the original PIN string from an encrypted PIN."""
    # Return an integer.
    original_PIN = None
    possible_PIN_codes = create_all_possible_PIN()
    atm = ATM()
    for p in possible_PIN_codes:
        int_PIN = convert_digits_array_to_int(p)
        current_encrypted_PIN = atm.encrypt_PIN(int_PIN)
        if current_encrypted_PIN == encrypted_PIN:
            original_PIN = int_PIN
            break
    return original_PIN


def extract_credit_card(encrypted_credit_card):
    """Extracts a credit card number string from its ciphertext."""
    # Return an integer.
    enc_exp = 3L
    credit_card = math.pow(encrypted_credit_card, 1./3)
    return int(str(credit_card)[:-2])  # Have to avoid lost of precision cast from float/double to int/long types


def forge_signature():
    """Forge a server response that passes verification."""
    # Return a ServerResponse instance.
    raise NotImplementedError()
