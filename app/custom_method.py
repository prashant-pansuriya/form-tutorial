""" custom method """
import math, random

# OTP generate
def generate_otp(no_of_digit):
    """otp generate"""
    digits = "0123456789"
    return "".join(
        [digits[math.floor(random.random() * 10)] for _ in range(no_of_digit)]
    )
