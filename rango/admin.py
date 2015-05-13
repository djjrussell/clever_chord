from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile
from rango.models import Favorites
from rango.models import Note
from rango.models import Type





admin.site.register(UserProfile)
# Add in this class to customized the Admin Interface


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Update the registeration to include this customised interface
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page)
admin.site.register(Favorites)
admin.site.register(Note)
admin.site.register(Type)




