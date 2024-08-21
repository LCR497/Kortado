import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Document
from datetime import datetime

logger = logging.getLogger('user_actions')

@receiver(post_save, sender=Document)
def log_document_save(sender, instance, created, **kwargs):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if created:
        logger.info(f"{current_time} - Document created: {instance.title} by user {instance.user.username}")
    else:
        logger.info(f"{current_time} - Document updated: {instance.title} by user {instance.user.username}")

@receiver(post_delete, sender=Document)
def log_document_delete(sender, instance, **kwargs):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f"{current_time} - Document deleted: {instance.title} by user {instance.user.username}")
