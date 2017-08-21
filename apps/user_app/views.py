# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import HttpResponse, render, redirect
from .models import User, Item
from django.contrib import messages

def index(request):
	return render(request, 'user_app/index.html')

def main(request):
	return render(request, 'user_app/index.html')
	#return redirect('/success')

def register(request):
	errors=User.objects.RegValid(request.POST)
	print errors, type(errors)

	if type(errors)==dict:
		for field, error in errors.iteritems():
			messages.error(request, error, extra_tags=field)
		return redirect('/main')
	request.session['id']=errors
	messages.success(request, "You are registered!")
	return redirect('/dashboard')	
	
def login(request):
	errors=User.objects.LoginValid(request.POST)
	print errors, type(errors)
	if type(errors) ==dict:
		for field, error in errors.iteritems():
			messages.error(request, error, extra_tags=field)
		return redirect('/main')
	request.session['id']=errors
	messages.success(request, "You are logged in!")
	return redirect('/dashboard')
# Create your views here.

def logout(request):
	request.session.clear()
	return redirect('/')

def dashboard(request):
	try:
		request.session['id']
	except:
		return redirect('/')
	context = {
		'users': User.objects.all(),
		'main_user': User.objects.get(id = request.session['id']),
		'items': Item.objects.all(),
		'my_items': Item.objects.filter(users__id = request.session['id']),
		'all_items': Item.objects.filter(all_users__id = request.session['id']),

	}
	return render(request, 'user_app/dashboard.html', context)

	
def delete(request, item_id):
	Item.objects.get(id=item_id).delete()
	return redirect('/dashboard')

def remove(request, item_id):
	Item.objects.exclude(id=item_id)
	return redirect('/dashboard')


def create(request):
	errors = Item.objects.ItemValid(request.POST, request.session['id'])
	if type(errors) == dict:
		for field, error in errors.iteritems():
			messages.error(request, error, extra_tags=field)
		return redirect('/create_form')
	request.session['item_id']=errors
	return redirect('/dashboard')

def create_form(request):
	return render(request, 'user_app/create.html')

def update(request, item_id):
	errors=Item.objects.WishValid(request.POST, item_id, request.session['id'])
	return redirect('/dashboard')

def display(request, item_id):
	context = {
		'items': Item.objects.get(id=item_id),
		'others': User.objects.filter(items_wished__id=item_id)

	}
	return render(request, 'user_app/wishlist.html', context)


