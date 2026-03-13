from celery import shared_task
from django.core.mail import send_mail, get_connection
from django.conf import settings

print("EMAIL USER:", settings.EMAIL_HOST_USER)
print("EMAIL PASS:", settings.EMAIL_HOST_PASSWORD[:5])

@shared_task
def send_booking_confirmation_email(email, service, date, time):

    subject = "Booking Confirmed"

    message = f"""
Your booking is confirmed.

Service: {service}
Date: {date}
Time: {time}

Thank you for choosing LocalServe.
"""

    connection = get_connection(
        backend="django.core.mail.backends.smtp.EmailBackend",
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        connection=connection,
        fail_silently=False,
    )