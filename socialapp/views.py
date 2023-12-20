from typing import Any
from django.utils import timezone
from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.views.generic import FormView,CreateView,TemplateView,View,UpdateView,DetailView,ListView
from socialapp.forms import UserRegistrationForm,LoginForm,UserProfileForm,PostForm,CommemtForm,StoryForm
from socialapp.models import UserProfile,Posts,Stories
from socialapp.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib import messages

# Create your views here.
decs=[login_required,never_cache]

class SignupView(CreateView):
    template_name="register.html"
    form_class=UserRegistrationForm
    
    def get_success_url(self):
        return reverse("signin")
    
    
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
        messages.error(request,"faild to login invalid credentilas")
        return render(request,"login.html",{"form":form})

@method_decorator(decs,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    form_class=PostForm
    model=Posts
    context_object_name="data"
    
    def get_success_url(self):
        return reverse("index")
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
    def get_queryset(self):
        bloked_profile=self.request.user.profile.block.all()
        bloked_profile_id=[pr.user.id for pr in bloked_profile]
        print(bloked_profile_id)
        qs=Posts.objects.all().exclude(user__id__in=bloked_profile_id).order_by("-created_date")
        return qs
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        cureent_date=timezone.now()
        context["stories"]=Stories.objects.filter(expiry_date__gte=cureent_date)
        return context 

@method_decorator(decs,name="dispatch")        
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

@method_decorator(decs,name="dispatch") 
class ProfileDetailView(DetailView):
    template_name="profile_detail.html"
    model=UserProfile
    context_object_name="data"

@method_decorator(decs,name="dispatch")     
class ProfileListView(View):
    def get(self,request,*args,**kwargs):
        qs=UserProfile.objects.all().exclude(user=request.user)
        return render(request,"profile_list.html",{"data":qs})
 
@method_decorator(decs,name="dispatch")    
class FollowView(View):
    def post(self,request,*args,**kwargs):
        print(request.POST)
        id=kwargs.get("pk")
        profile_obj=UserProfile.objects.get(id=id)
        action=request.POST.get("action")
        if action=="follow":
            request.user.profile.following.add(profile_obj)
        elif action=="unfollow":
            request.user.profile.following.remove(profile_obj)
           
        
        return redirect("index")

@method_decorator(decs,name="dispatch")     
class PostLikeView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post_obj=Posts.objects.get(id=id)
        action=request.POST.get("action")
        if action=="like":
            post_obj.liked_by.add(request.user)
        elif action=="unlike":
            post_obj.liked_by.remove(request.user)
            
        return redirect("index")

@method_decorator(decs,name="dispatch") 
class CommentView(CreateView):
    template_name="index.html"
    form_class=CommemtForm
    
    def get_success_url(self):
        return reverse("index")
    
    def form_valid(self, form):
        form.instance.user=self.request.user
        id=self.kwargs.get("pk")
        post_obj=Posts.objects.get(id=id)
        form.instance.post=post_obj   
        return super().form_valid(form)

@method_decorator(decs,name="dispatch")     
class ProfileBlockView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        profile_obj=UserProfile.objects.get(id=id)
        action=request.POST.get("action")
        if action=="block":
            request.user.profile.block.add(profile_obj)
        elif action=="unblock":
            request.user.profile.block.remove(profile_obj)
        return redirect("index")

@method_decorator(decs,name="dispatch") 
class ProfileUpdateView(UpdateView):
    template_name="profile_add.html"
    form_class=UserProfileForm
    model=UserProfile
    
    def get_success_url(self):
        return reverse("index")

@method_decorator(decs,name="dispatch") 
class StorieCreateView(View):
    
    def post(self,request,*args,**kwargs):
        form=StoryForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect("index")
        return redirect("index")

@method_decorator(decs,name="dispatch")     
class StoryDetailView(DetailView):
    template_name="story.html"
    model=Stories
    context_object_name="data"