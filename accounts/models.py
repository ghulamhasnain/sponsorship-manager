from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserInfo(models.Model):
	user = models.OneToOneField(User,on_delete=models.PROTECT, related_name='user_info')
	email_to = models.CharField(max_length=1000)

	def __str__(self):
		return self.user.username

User.profile = property(lambda u: UserInfo.objects.get_or_create(user=u)[0])