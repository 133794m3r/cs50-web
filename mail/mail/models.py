from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
\tpass


class Email(models.Model):
\tuser = models.ForeignKey("User", on_delete=models.CASCADE, related_name="emails")
\tsender = models.ForeignKey("User", on_delete=models.PROTECT, related_name="emails_sent")
\trecipients = models.ManyToManyField("User", related_name="emails_received")
\tsubject = models.CharField(max_length=255)
	body = models.TextField(blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	read = models.BooleanField(default=False)
	archived = models.BooleanField(default=False)

	def serialize(self):
		return {
			"id": self.id,
			"sender": self.sender.email,
			"recipients": [user.email for user in self.recipients.all()],
			"subject": self.subject,
			"body": self.body,
			"timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p"),
			"read": self.read,
			"archived": self.archived
		}
