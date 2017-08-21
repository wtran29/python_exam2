# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re, bcrypt
import datetime
USERNAME_REGEX=re.compile(r'^[A-Za-z0-9]\w+$')
NAME_REGEX=re.compile(r'^[A-Za-z]+\s+[A-Za-z]\w+$')

class UserManager(models.Manager):
	def RegValid(self, postData):
		errors ={}
		if len(postData['name'])< 3:
			errors['name']="Name must be at least 3 characters!"
		elif not re.match(NAME_REGEX, postData['name']):
			errors['name']="Must have first and last name"
		

		if len(postData['user_name'])< 3:
			errors['username']="Name must be at least 3 characters!"

		if len(postData['password'])<8:
			errors['password']="Password must be at least 8 characters!"
		elif postData['password']!=postData['confirm']:
			errors['confirm']="Password is not valid"

		if not re.match(USERNAME_REGEX, postData['user_name']):
			errors['user_name'] = "Invalid username"

		if len(postData['hired']) < 1:
			errors['hired'] = "Enter hire date"

		# if postData['depart'] and postData['arrival']:
		# 	depart = datetime.datetime.strptime(postData['depart'],"%Y-%m-%d")
		# 	arrival = datetime.datetime.strptime(postData['arrival'],"%Y-%m-%d")
		# 	today_def = datetime.date.today() #format given '2008-11-22 19:53:42'
		# 	today = datetime.datetime(today_def.year, today_def.month, today_def.day) #changes it to '2008-11-22'
		

		# 	if depart < today:
		# 		errors['depart'] = "The date cannot be in the past"


		# 	if depart > arrival:
		# 		errors['arrival'] = "Arrival date cannot be set before the departure date" 

		# 	if arrival < today:
		# 		errors['arrival'] = "The date cannot be in the future"


		try: 
			postData['hired']
			hire = datetime.datetime.strptime(postData['hired'], "%Y-%m-%d")
			today = datetime.date.today()
			today_ref = datetime.datetime(today.year, today.month, today.day)

			if hired > today_ref:
				errors['hired'] = "Please enter correct hire date"

		except:
			pass

		try:
			User.objects.get(user_name = postData['user_name'])
			errors['duplicate'] = "Username taken"

		except:
			pass

		if len(errors) == 0:
			hash1 = bcrypt.hashpw((postData['password'].encode()),bcrypt.gensalt(5))

			new_user=User.objects.create(
				name=postData['name'],
				user_name=postData['user_name'],
				password=hash1,
				hired = postData['hired']
				
			)
			return new_user.id
		return errors


	def LoginValid(self,postData):
		errors={}
		try:
			user=User.objects.get(user_name=postData['user_name'])
			if not bcrypt.checkpw(postData['password'].encode(),user.password.encode()):
				errors['password']="User Name/Password incorrect"
		except:
			errors['loginerror'] = "Incorrect login info"
		if errors:
			return errors
		return user.id

class ItemManager(models.Manager):
	def ItemValid(self, postData, id):
		errors = {}
		if len(postData['name']) < 3:
			errors['name'] = "Enter Item"

		if errors:
			return errors

		item=Item.objects.create(
			name = postData['name'],
			users = User.objects.get(id=id),
		)

		return item.id

	def WishValid(self, postData, item_id, id):
		user=User.objects.get(id=id)
		add=Item.objects.get(id=item_id).all_users.add(user)
		return add

class User(models.Model):
	name = models.CharField(max_length=255)
	user_name = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	hired = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()
#Create your models here.
class Item(models.Model):
	name = models.CharField(max_length=255)
	users = models.ForeignKey(User, related_name="items") #user can wish for many items
	all_users =models.ManyToManyField(User, related_name="items_wished") #users can wish for many items, same items can be wished by many users
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = ItemManager()
