from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from .models import checklist

# Create your views here.

def home (request):
    if request.method == 'POST':
         task = request.POST.get('task')
         new_checklist = checklist(user=request.user, checklist_name=task)
         new_checklist.save()
         all_checklists = checklist.objects.filter(user=request.user).values('checklist_name')
         checklist_data = list(all_checklists)
         return JsonResponse({'checklists': checklist_data})

def json(request):
    all_checklists = checklist.objects.filter(user=request.user).values('checklist_name')
    checklist_data = list(all_checklists)
    return JsonResponse({'checklists': checklist_data})

    all_checklists = checklist.objects.filter(user=request.user)
    context = {
         'checklists' : all_checklists
    }
    return render(request, 'accounts/todo.html', context)




def register(request):
     if request.method == 'POST':
          username = request.POST.get('username')
          email = request.POST.get('email')
          password = request.POST.get('password')

          if len(password) < 3:
               messages.error(request, 'Password is too short')
               return redirect('register')
          
          get_all_users_by_username = User.objects.filter(username=username)
          if get_all_users_by_username:
               messages.error(request, 'Username already exists')
               return redirect('register')

          new_user = User.objects.create_user(username=username, email=email, password=password)
          new_user.save()

          messages.success(request, 'User successfully created, login now')
          return redirect('login')


     return render(request, 'accounts/register.html', {})

def loginpage(request):
      if request.method == 'POST':
           username = request.POST.get('uname')
           password = request.POST.get('pass')

           validate_user = authenticate(username=username, password=password)
           if validate_user is not None:
                login(request, validate_user)
                return redirect('home-page')
           else:
                messages.error(request, 'Error user does not exist')
                return redirect('login')

      return render(request, 'accounts/login.html', {})

def DeleteTask(request, name):
     get_checklist = checklist.objects.get(user=request.user, checklist_name=name)
     get_checklist.delete()
     return redirect('home-page')

def Update(request, name):
     pass