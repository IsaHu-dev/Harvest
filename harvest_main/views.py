from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages  # Import messages module
from .forms import UserForm
from .models import User

def registeration(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Account created successfully')  # Using messages after importing
            return redirect('registeration')  # Redirect to login page after successful registration
        else:
            print('Form is invalid')
            print(form.errors)
    else:
        form = UserForm()
    
    context = {
        'form': form
    }
    
    return render(request, 'accounts/register-user.html', context)
