from django.contrib import admin

# Register your models here.
from .models import User, Listing , Bids, Comments, Catagory

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bids)
admin.site.register(Catagory)
admin.site.register(Comments)