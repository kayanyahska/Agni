from django.db import models

# Create your models here.

class candidates(models.Model):
	c_name = models.CharField(max_length=100)
	#party = models.CharField(max_length=100)
	zipcode = models.CharField(max_length=100, blank=True)
	city = models.CharField(max_length=100)
	state = models.CharField(max_length=100)
