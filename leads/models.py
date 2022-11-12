from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass



class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    project_name = models.CharField(max_length=50)
    Agent = models.ForeignKey("Agent", on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.email
    

    
    
#     phoned = models.BooleanField(default=False)
# #     source = models.CharField(choices=SOURCE_CHOICES, max_length=100)

# #     profile_picture = models.ImageField(blank=True, null=True)
# #     special_files = models.FileField(blank=True, null=True)

# # SOURCE_CHOICES = (
# #         ('Youtube', 'Youtube'),
# #         ('Google', 'Google'),
# #         ('Newsletter', 'Newsletter'),

# #     )
