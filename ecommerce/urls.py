
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # account route
    path('account/', include('accounts.urls')),
    # api route
    path('api/', include('api.urls')),
]
