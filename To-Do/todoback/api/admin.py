from django.contrib import admin
from .models import Person, Task, Tag
from django.contrib.auth.admin import UserAdmin

@admin.register(Person)
class PersonAdmin(UserAdmin):
    model = Person
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('personnal_img', 'wallpaper_img', 'birth_date')}),
    )


admin.site.register(Task)
admin.site.register(Tag)
