from django.contrib import admin
from .models import User,AreaOfficer,Citizen,Contact,UserProfile
# Register your models here.
admin.site.register(User)
admin.site.register(AreaOfficer)
admin.site.register(Citizen)
admin.site.register(Contact)
admin.site.register(UserProfile)

