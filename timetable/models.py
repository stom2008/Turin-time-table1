from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField(default=30)

    def __str__(self):
        return self.name


class Availability(models.Model):
    DAYS = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE,
        null=True, blank=True
    )
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE,
        null=True, blank=True
    )
    day = models.IntegerField(choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    available = models.BooleanField(default=True)

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError(
                    "End time must be after start time."
                )

            conflicts = Availability.objects.filter(
                day=self.day,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time,
            ).exclude(pk=self.pk)

            if self.teacher_id and conflicts.filter(
                teacher_id=self.teacher_id
            ).exists():
                raise ValidationError(
                    "Teacher is already booked at this time."
                )

            if self.room_id and conflicts.filter(
                room_id=self.room_id
            ).exists():
                raise ValidationError(
                    "Room is already occupied at this time."
                )

    def __str__(self):
        return f"{self.day}: {self.start_time}-{self.end_time}"