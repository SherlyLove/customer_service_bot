from fastapi import FastAPI, Form, Depends, Request
from decouple import config
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from twilio.twiml.messaging_response import MessagingResponse

# internal imports
from utils import send_msg, logger, store_conversation
from models import Conversation, SessionLocal

# create the FastAPI instance
csb = FastAPI()


# common variables
company_name = config("COMPANY_NAME")

# create a dependency function that will create a new database session for each request
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
        
# Root webhook
@csb.get("/")
async def index():
    return {"msg": "Successfully set up"}


# /message webhook
@csb.post("/message")
async def reply(request: Request, Body = Form(), db: Session = Depends(get_db)):
    # get data from incoming request
    data = await request.form()
    
    # Extract name and phone number 
    user_name = data['ProfileName'].split("whatsapp:")[-1]
    user_number = data['From'].split("whatsapp:")[-1]
    
    logger.info(f"Sending response to {user_name}: {user_number}")
    
    response = f"Welcome to {company_name}, {user_name}. How may we help you today?"
    
    # store conversation in database
    store_conversation(db, user_number, response, Body)
        
    send_msg(user_number, response)
    
    return "Success"