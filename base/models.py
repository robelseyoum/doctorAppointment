from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from django.conf import settings
from decimal import Decimal


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.TextField(blank=True)
    is_admin = models.IntegerField(default=0)
    phone = models.CharField(max_length=250, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    sex = models.TextField(blank=True)
    role=models.TextField(blank=True)
    dob = models.DateField(null=True, blank=True)

class Patient(models.Model):
    user = models.ForeignKey('auth.User')
    creation_date = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    category_name=models.TextField(blank=True)


class Doctor(models.Model):
    user = models.ForeignKey('auth.User')
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, related_name='patient_appointment')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField(null=True, blank=True)
    appointment = models.DateTimeField()
    is_notified=models.BooleanField(default=False)

class Treatment(models.Model):
    patient = models.ForeignKey(Patient, related_name='patient_treatment')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField(null=True, blank=True)
    treatment = models.CharField(max_length=250, null=True, blank=True)
    treatment_for = models.CharField(max_length=250, null=True, blank=True)
    dnote = models.CharField(max_length=250, null=True, blank=True)
    appointment=models.ForeignKey(Appointment, related_name='appointment_id')

class Schedule(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField(null=True, blank=True)
    note = models.CharField(max_length=250, null=True, blank=True)

class Feedback(models.Model):
    patient = models.ForeignKey(Patient, related_name='patient_feedback')
    creation_date = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField()