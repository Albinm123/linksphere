from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.views.generic import FormView,CreateView,TemplateView,View
from socialapp.forms import UserRegistrationForm,LoginForm

# Create your views here.

class SignupView(CreateView):
    template_name="register.html"
    form_class=UserRegistrationForm
    
    def get_success_url(self):
        return reverse("register")
    
    
    # def post(self,request,*args,**kwargs):
    #     form=UserRegistrationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("register")
    #     else:
    #         return render(request,"register.html",{"form":form})

class SigninView(FormView):
    template_name="login.html"
    form_class=LoginForm
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_obj=authenticate(request,username=uname,password=pwd)
            if user_obj:
                login(request,user_obj)
                print("success")
                return redirect("index")
            
        print("faild")
        return redirect(request,"login.html",{"form":form})


class IndexView(TemplateView):
    template_name="index.html"
    
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")