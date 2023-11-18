import logging

from twilio.rest import Client
from decouple import config

# Set up Twilio credentials
account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
twilio_number = config('TWILIO_NUMBER')

client = Client(account_sid, auth_token)

# configure logger
logging.basicConfig(filename="logs/csb.log", encoding='utf-8', format="%(asctime)s %(levelname)s: %(name)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)
logger = logging.getLogger(__name__)


# send message to user
def send_msg(receiver_no, msg):
    try:
        message = client.messages.create(
            from_ = f"whatsapp:{twilio_number}",
            body = msg,
            to = f"whatsapp:{receiver_no}"
        )
        
        logger.info(f"Message sent to {receiver_no}: {message.body}\n")
        print("Message sent")
        
    except Exception as e:
        logger.error(f"Error sending message to {receiver_no}: {e}")
        print("Message not sent")