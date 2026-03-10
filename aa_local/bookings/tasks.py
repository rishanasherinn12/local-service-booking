# from celery import shared_task
# from django.core.mail import send_mail
# from django.conf import settings


# @shared_task
# def send_booking_email(email, service, date, time):

#     subject = "Booking Request Received"

#     message = f"""
# Hello,

# Your booking request has been received.

# Service: {service}
# Date: {date}
# Time: {time}

# Our team will assign a professional shortly.

# Thank you for choosing our service.
# """

#     send_mail(
#         subject,
#         message,
#         settings.DEFAULT_FROM_EMAIL,
#         [email],
#         fail_silently=False,
#     )