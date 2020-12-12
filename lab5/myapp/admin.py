from django.contrib import admin
from myapp.models import User, SensitiveData

admin.site.register(User)
admin.site.register(SensitiveData)
