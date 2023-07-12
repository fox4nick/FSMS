from django.db import models

class MenuItem(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	image = models.ImageField(upload_to='menu_images/')
	category = models.ManyToManyField('Category', related_name='item')

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class OrderModel(models.Model):
	FULFILLED = "Fulfilled"
	DEFERRED = "Deferred"
	DENIED = "Denied"
	PENDING = "Pending"
	STATUS_CHOICES = [
		(FULFILLED, "Fulfilled"),
		(DEFERRED, "Deferred"),
		(DENIED, "Denied"),
		(PENDING, "Pending")
	]

	created_on = models.DateTimeField(auto_now_add=True)
	items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
	name = models.CharField(max_length=50, blank=True)
	email = models.CharField(max_length=50, blank=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

	def __str__(self):
		return f'Request: {self.created_on.strftime("%b %d %I: %M %p ")}'

class NewRequestModel(models.Model):
	FULFILLED = "Fulfilled"
	DEFERRED = "Deferred"
	DENIED = "Denied"
	PENDING = "Pending"
	STATUS_CHOICES = [
		(FULFILLED, "Fulfilled"),
		(DEFERRED, "Deferred"),
		(DENIED, "Denied"),
		(PENDING, "Pending")
	]

	created_on = models.DateTimeField(auto_now_add=True)
	snack = models.CharField(max_length=100, blank=True)
	argument = models.TextField(blank=True)
	link = models.TextField(blank=True)
	name = models.CharField(max_length=50, blank=True)
	email = models.CharField(max_length=50, blank=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

	def __str__(self):
		return f'Request: {self.created_on.strftime("%b %d %I: %M %p ")}'