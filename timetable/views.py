from django.shortcuts import render
from .models import Availability, Teacher, Room


def timetable_view(request):
    slots = Availability.objects.select_related(
        "teacher", "room"
    ).order_by("day", "start_time")

    day = request.GET.get("day", "")
    status = request.GET.get("status", "")
    search = request.GET.get("search", "").strip()
    resource_type = request.GET.get("type", "")

    if day:
        slots = slots.filter(day=day)

    if status == "available":
        slots = slots.filter(available=True)
    elif status == "occupied":
        slots = slots.filter(available=False)

    if search:
        slots = slots.filter(
            teacher__name__icontains=search
        ) | slots.filter(room__name__icontains=search)

    if resource_type == "teacher":
        slots = slots.filter(teacher__isnull=False)
    elif resource_type == "room":
        slots = slots.filter(room__isnull=False)

    return render(request, "timetable/index.html", {
        "slots": slots,
        "selected_day": day,
        "selected_status": status,
        "search": search,
        "resource_type": resource_type,
        "days": Availability.DAYS,
        "teachers": Teacher.objects.all(),
        "rooms": Room.objects.all(),
    })