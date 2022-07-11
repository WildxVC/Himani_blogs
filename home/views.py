from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from home.models import Category, Post
from django.core.paginator import Paginator
from home.Forms import AddPostForm
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required



# Create your views here.
def home(request):
    title = "Home"
    allCategories = Category.objects.all()
    posts = Post.objects.all().order_by('-timestamp')
    carousalPosts = Post.objects.all().order_by('-views')[0:5]
    paginator = Paginator(posts,12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'allCategories' : allCategories,
        'posts' :page_obj, 
        'carousalPosts':carousalPosts, 
        'title' : title,
        }
    
    return render(request, "home.html",context)




def categories(request, category_slug):
    category_slug = category_slug
    title = category_slug
    page_number = request.GET.get('page',None)
    
    category = {}
    posts = Post.objects.all().order_by('-timestamp')
    if category_slug:
        if category_slug== 'More':
            category = Category.objects.all()[5:]
            posts = Post.objects.all().filter(cat_id__in = category).order_by('-timestamp')
        elif category_slug== 'All':
            category = Category.objects.all()
            posts = Post.objects.all().filter(cat_id__in = category).order_by('-timestamp')
        else:    
            category = Category.objects.filter(title=category_slug).first()
            # cat_id= category.cat_id
            if category:
                  posts = Post.objects.all().filter(cat_id= category.cat_id).order_by('-timestamp')
            
            
        
        paginator = Paginator(posts,12)
        page_obj = paginator.get_page(page_number)
        context = {
            'category_slug' : category_slug,
            'category': category,
            'posts': page_obj,
            'title' : title,
        }
        return render(request, 'category.html', context)
    
    paginator = Paginator(posts,12)
    page_obj = paginator.get_page(page_number)    
    context = {
        'category_slug' : category_slug,
        'category': category,
        'posts': page_obj,
        'title' : title,
    }
    return render(request, 'category.html', context)





def viewPost(request, slug):
    post= Post.objects.get(slug=slug)
    post.views += 1
    post.save()
    carousalPosts = Post.objects.all().order_by('-views')[0:5]
    context = {
        'post' : post,
        'carousalPosts': carousalPosts,
        'title' : "BlogPost | BrainsBrew",
    }
    return render(request, 'view_post.html',context)





def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        
        user = authenticate(request, username=username, password=password)

        # If user object is returned, log in and route to current page
        if user:
            login(request, user)
            messages.success(request,'You have been successfully logged in !')
            return render(request,"home.html")
        # Otherwise, throw an error on current page
        else:
            messages.error(request, 'Invalid credentials. Please try again !')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

    else:
        return render(request,"admin_login.html")



@login_required
def addPost(request):
    if request.method == "POST":
        form = AddPostForm(request.POST,request.FILES)
        if form.is_valid():
           
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(f"/")
    else:
        form = AddPostForm()
    return render(request,'add_post.html',{'form': form,'title' : "AddPost",})





def searchResult(request):
    query= request.GET.get('query')
    if len(query)>50 or len(query)<1:
        allPost= Post.objects.none()
    else:
        allPostTitle = Post.objects.filter(title__icontains=query)
        allPostContent = Post.objects.filter(desc__icontains=query)
        allPost = allPostTitle.union(allPostContent)
        
    context = {
        'allpost': allPost,
        'query':query,
        'title' : "Search",
        }
    
    if allPost.count()==0:
        messages.warning(request, 'No search results found ! Please refine your query.')
    return render(request, 'search_page.html',context)

def aboutView(request):
    return render(request, 'additional/about.html',{'title': "About Us | BrainsBrew"})

def privacyView(request):
    return render(request, 'additional/privacy.html',{'title': "Privacy Policy | BrainsBrew"})

def termsView(request):
    return render(request, 'additional/terms.html',{'title': "Terms & Conditions | BrainsBrew"})

