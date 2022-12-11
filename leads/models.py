from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    project_name = models.CharField(max_length=50)
    organisation = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.CASCADE)
    agent = models.ForeignKey("Agent", on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email



def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    

post_save.connect(post_user_created_signal, sender=User)
    

    
    
#     phoned = models.BooleanField(default=False)
# #     source = models.CharField(choices=SOURCE_CHOICES, max_length=100)

# #     profile_picture = models.ImageField(blank=True, null=True)
# #     special_files = models.FileField(blank=True, null=True)

# # SOURCE_CHOICES = (
# #         ('Youtube', 'Youtube'),
# #         ('Google', 'Google'),
# #         ('Newsletter', 'Newsletter'),

# #     )
