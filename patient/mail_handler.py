from django.core.mail import send_mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client
import environ
import os

from patient.models import Patient



env = environ.Env()
# reading .env file
environ.Env.read_env()

def send_email_to_user(send_to, patient):
    subject = "[URGENT] SOS call"
    message = f'''
         <h1>Arogya Doot SOS Alert</h1><br>
         <p>An SOS call has been made by a patient.<br>
         Please contact the patient as soon as possible.<br><br>
         <b>Patient Details:-</b><br><br>
            <b>Name: </b>{patient.user.first_name}<br>
            <b>Phone: </b>{patient.phone}<br>
            <b>Allocated Bed no.:</b> {patient.allocated_bed.room_no}<br>
            <b>Floor No.:</b> {patient.allocated_bed.floor_no}<br>
            </p>
    '''

    msg = Mail(
        from_email='unisighttechnologies@gmail.com',
        to_emails=send_to,
        subject=subject,
        html_content=message
    )
    try:
        sg= SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response=sg.send(msg)
    except Exception as e:
        print(e)

def send_sms_to_user(phone, patient):
    try:
        account_sid = env('TWILIO_SID')
        auth_token = env('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token) 
        message = f'''Arogya Doot SOS Alert!! \n\nAn SOS call has been made by a patient. \nPlease contact the patient as soon as possible. \n\nPatient Details:- Name: {patient.user.first_name} \nPhone: {patient.phone} \nAllocated Bed no.: {patient.allocated_bed.room_no}\nFloor No.: {patient.allocated_bed.floor_no}'''

        message = client.messages \
                        .create(
                            body=message,
                            from_=env("TWILIO_PHONE_NO"),
                            to=phone
                        )

        print(message.sid)
    except Exception as e:
        print(e)