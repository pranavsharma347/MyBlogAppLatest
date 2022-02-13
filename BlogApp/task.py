from celery import shared_task
from django.core.mail import send_mail
from django.core.mail import EmailMessage



@shared_task()
def share_by_mail(mail_data):
    send_mail(mail_data['subject'],mail_data['message'],mail_data['email'],[mail_data['to']],fail_silently=False)
    
    
    
@shared_task()
def signup_mail(mail_subject,message,to_email):
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.content_subtype = 'html'
    email.send()
    