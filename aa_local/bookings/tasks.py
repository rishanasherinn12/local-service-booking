from celery import shared_task
from django.core.mail import send_mail, get_connection
from django.conf import settings


@shared_task
def send_booking_confirmation_email(email, service, date, time):

    subject = "Booking Confirmed"

    message = f"""
    Hello,

    Your booking has been successfully confirmed.

    Service : {service}
    Date    : {date}
    Time    : {time}

    Thank you for choosing LocalServe.

    Regards,
    LocalServe Team
    """.strip()

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