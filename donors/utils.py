import random
from django.core.mail import send_mail

otp_store = {}  # Store OTPs temporarily, consider using Redis or DB for production

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_to_email(email):
    otp = generate_otp()
    otp_store[email] = otp
    send_mail(
        subject="Your OTP for RaktKan Registration",
        message=f"Your OTP is: {otp}",
        from_email="raktkan@example.com",
        recipient_list=[email],
        fail_silently=False,
    )
    return otp
