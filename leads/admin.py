from django.contrib import admin
from .models import Lead, User, Agent, UserProfile

# Register your models here.

admin.site.register(Lead)
admin.site.register(User)
admin.site.register(Agent)
admin.site.register(UserProfile)


