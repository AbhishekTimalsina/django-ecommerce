from django.shortcuts import render, redirect
from django.views import View
from .forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from order.models import Order
# Create your views here.

class SignupView(View):

    def get(self,request):
        form = SignupForm()
        return render(request,'users/signup.html',{'form': form})

    
    def post(self,request):
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request,user)
            return redirect('/')

        return render(request, 'users/signup.html',{'form': form})

class LoginView(View):

    def get(self,request):
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self,request):
        form = LoginForm(request.POST)


        if form.is_valid():
           email = form.cleaned_data['email'] 
           password = form.cleaned_data['password'] 

           user = authenticate(request, email=email, password=password)

           if user is not None:
            login(request,user)
            return redirect('/')
           else:
            form.add_error(None,"Invalid email or password")

        return render(request, 'users/login.html', {'form': form})


class Logout(View):
    def post(self,request):
        logout(request)
        return redirect('login')

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'profile.html', {'orders': orders})