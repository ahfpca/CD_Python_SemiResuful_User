from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from apps.users.models import *
from django.contrib import messages

# Create your views here.
def index(request):
    users = User.objects.all()

    request.session.clear()            
    
    return render(request, 'users/index.html', { 'users': users })


def new(request):
    request.session['callMode'] = 0

    return render(request, 'users/edit.html')


def edit(request, id):
    if 'callMode' in request.session and request.session['callMode'] != 2:
        rec = User.objects.get(user_id = id)

        request.session['user_id'] = rec.user_id
        request.session['first_name'] = rec.first_name
        request.session['last_name'] = rec.last_name
        request.session['email'] = rec.email

    request.session['callMode'] = 1

    return render(request, 'users/edit.html')


def delete(request, id):
    # delete the record
    User.objects.get(user_id = id).delete()

    return redirect('/users')


def show(request, id):
    userRec = User.objects.get(user_id = id)

    return render(request, 'users/show.html', { 'user': userRec } )


def create(request):
    if request.method == 'POST':
        errors = User.objects.record_validator(request.POST)

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        if len(errors):
            for key, value in errors.items():
                messages.add_message(request, level = 40, message = value, extra_tags = key)
                request.session['first_name'] = first_name
                request.session['last_name'] = last_name
                request.session['email'] = email
            return redirect('/users/new')
        else:
            ret = User.objects.create(first_name = first_name, last_name = last_name, email = email)
            if ret.user_id > 0:
                request.session.clear()
            else:
                messages.add_message(request, level = 40, message = "Something went wrong! Record didn't save.", extra_tags = 'error')
                return redirect('/users/new')

    return redirect('/users')


def update(request):
    if request.method == 'POST':
        errors = User.objects.record_validator(request.POST)
        #print("=======> POST:", request.POST)
        
        user_id = request.POST['user_id']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']

        if len(errors):
            for key, value in errors.items():
                messages.add_message(request, level = 40, message = value, extra_tags = key)
                request.session['first_name'] = first_name
                request.session['last_name'] = last_name
                request.session['email'] = email
                request.session['callMode'] = 2 # Do not load from database (in edit function)
                
            return redirect(f'/users/{user_id}/edit')
        else:
            rec = User.objects.get(user_id = user_id)
            rec.first_name = first_name
            rec.last_name = last_name
            rec.email = email
            rec.save()

            request.session.clear()

    return redirect('/users')
