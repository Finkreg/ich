# signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Task

@receiver(pre_save, sender=Task)
def notify_status_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # новая задача, не отправляем уведомление

    previous = Task.objects.get(pk=instance.pk)

    # Проверка: статус изменился и не совпадает с последним уведомленным
    if instance.status != previous.status and instance.status != previous.last_notified_status:
        subject = f"Изменение статуса задачи: {instance.title}"
        message = f"Задача '{instance.title}' изменила статус на '{instance.get_status_display()}'."
        recipient = instance.owner.email

        # Вместо реальной отправки — выводим в консоль
        print(f"\n📧 Email to {recipient}:\nSubject: {subject}\nMessage: {message}\n")

        # Обновляем поле last_notified_status
        instance.last_notified_status = instance.status
