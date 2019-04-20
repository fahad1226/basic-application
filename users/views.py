from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, UserUpdate,ProfileUpdate
from django.contrib.auth.decorators import login_required

def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'congratulations {username}. your account has been created!you are now able to login')
            return redirect('login')
    else:

        form = RegistrationForm()

    return render(request,'register.html',{'form':form})

@login_required
def profile(request):

    return render(request,'profile.html')



def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdate(request.POST,instance=request.user)
        p_form = ProfileUpdate(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'your account has been updated successfully!')
            return redirect('profile')

    else:
        u_form = UserUpdate(instance=request.user)
        p_form = ProfileUpdate(instance=request.user.profile)
    context = {
        'u_form':u_form,
        'p_form':p_form
    }

    return render(request,'profile_update.html',context)
