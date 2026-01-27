from celery import shared_task
import logging


logger = logging.getLogger(__name__)




@shared_task
def send_welcome_email(user_data):
    # Logic to send a welcome email to the user with the given user_id
    logger.info(f"Sending welcome email {user_data['email']} to user with ID: {user_data['id']}")
    # TODO: Implement actual email sending logic here
    return f"Welcome {user_data['email']} email sent."