from django.contrib import admin
# unregister group
from django.contrib.auth.models import Group
# unregister group
admin.site.unregister(Group)

# import user and profile class to register on admin panel
from accounts.models import User, Profile

admin.site.register(User)
admin.site.register(Profile)
