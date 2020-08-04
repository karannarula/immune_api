from django.db import models
from decimal import Decimal
from django.utils.timezone import now
from datetime import timedelta

# Create your models here.




class Users(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	email = models.CharField(max_length=100, blank=False,unique=True)
	title = models.CharField(max_length=100, blank=True, default='')
	user_id = models.IntegerField(default=0)
	logged_in = models.BooleanField(default=False)

	def __str__ (self):
		return self.title

# class Meta:
# 	ordering = ('created')




class Location(models.Model):
	latitude = models.CharField(max_length=20, blank=False,default = 0.000)
	longitude = models.CharField(max_length=20, blank=False,default = 0.000)
	email_id = models.CharField(max_length=50,blank=False,default='')
	created = models.DateTimeField(default=now,blank=True)
	index = models.IntegerField(default=0)
	status_bit = models.IntegerField(default=0)
	name = models.CharField(max_length=20, blank=False,default = 0.000)
	#0--start  1 --- stop



class CalendarEvents(models.Model):
	event_id = models.TextField(blank=True, null=True,default='')
	created = models.DateTimeField(blank=True,default=now)
	lead_name = models.CharField(max_length=50,blank=False,default="",primary_key=True)
	lead_series = models.CharField(max_length=50,blank=False,default="")
	event_bit = models.SmallIntegerField(default=0,blank=False)