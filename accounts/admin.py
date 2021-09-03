from django.contrib import admin

# import user and profile class to register on admin panel
from accounts.models import User, Profile

admin.site.register(User)
admin.site.register(Profile)
