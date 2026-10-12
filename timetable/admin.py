from django.contrib import admin
from .models import Teacher, Room, Availability


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "capacity")
    search_fields = ("name",)


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = (
        "day", "teacher", "room",
        "start_time", "end_time", "available"
    )
    list_filter = ("day", "available", "teacher", "room")
    ordering = ("day", "start_time")

    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)