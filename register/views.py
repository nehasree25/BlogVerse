from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login as auth_login, logout
from .forms import SignUp,Login,BlogForm
from .models import Blog
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request,'register/home.html')
def signup(request):
    if request.method == 'POST':
        form = SignUp(request.POST)
        if(form.is_valid()):
            obj=form.save()
            auth_login(request,obj)
            return HttpResponse("successfully registered")
    else:
        form = SignUp()
    return render(request,'register/signup.html',{'form':form})
def user_login(request):
    if request.method == 'POST':
        form = Login(request=request,data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            auth_login(request, user)
            return redirect('/allblogs/')
    else:
        form = Login()
    return render(request,'register/login.html',{'form':form})
def user_logout(request):
    logout(request)
    return redirect('/login/')
@login_required
def createBlog(request):
    if request.method=='POST':
        blog = BlogForm(request.POST)
        if blog.is_valid():
            blog = blog.save(commit=False)  # Don't save to DB yet
            blog.author = request.user  # Set the logged-in user as author
            blog.save()
            return redirect('/myblogs/')
    else:
        blog = BlogForm()
    return render(request,'register/createBlog.html',{'blog':blog})
@login_required
def allBlogs(request):
    blogs = Blog.objects.all()
    return render(request,'register/allBlogs.html',{'blogs':blogs})
@login_required
def delete_blog(request, id):
    blog = get_object_or_404(Blog, id=id)
    if request.method == 'POST':
        blog.delete()
        return redirect('/myblogs/')
    return render(request, 'register/deleteblog.html', {'blog': blog})
@login_required
def editblog(request,id):
    blog=get_object_or_404(Blog, id=id)
    if request.method == 'POST':
        form = BlogForm(request.POST,instance=blog)
        if form.is_valid():
            form.save()
            return redirect('/myblogs/')
    else:
        form = BlogForm(instance=blog)
    return render(request,'register/editblog.html', {'form':form})
@login_required
def myBlogs(request):
    blog=Blog.objects.filter(author=request.user) 
    return render(request,'register/myblogs.html',{'blog':blog})