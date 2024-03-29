from django.shortcuts import render,get_object_or_404,redirect
from django.http  import HttpResponse,HttpResponseRedirect
from .models import Image,Profile, Comment, Like
from django.contrib.auth.decorators import login_required
from .forms import CommentForm, AddPostForm
from django.contrib.auth import login, authenticate

# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    posts = Image.objects.all().order_by('-id')
    users = Profile.objects.all()
    # Images = Image.objects.all().order_by('-id')
    form = CommentForm()
    if request.method == 'POST':  
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            commentt = form.save(commit=False)
            commentt.user = request.POST.user
            commentt.save()
            return redirect('index')
            
    return render(request, 'all-temps/index.html',{"posts":posts,  "form":form, 'users':users})

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    posts = Image.objects.filter(user=current_user)
    profile = Profile.objects.filter(user_id=current_user.id)
    form = AddPostForm()
    if request.method == 'POST':
        form = AddPostForm(request.POST , request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
        redirect('profile')
    return render(request, 'all-temps/profile.html', {"posts": posts, "profile": profile, 'form':form})


def one_image(request, id):
    image = Image.objects.get(id=id)
    images_related = Image.objects.filter(
        user_id = image.user_id
    ).order_by('-posted_on')
    title = image.name

    if Image.objects.filter(id=id).exists():
        comments= Comment.objects.filter(image_id=id)
        return render(request, 'all-temps/image.html', {'image':image, 'comments':comments,'title':title, 'images':images_related})
    else:
        return redirect('/')

@login_required
def comments(request,image_id):
  form = CommentForm()
  image = Image.objects.filter(pk = image_id).first()
  if request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit = False)
      comment.user = request.user
      comment.image = image
      comment.save() 
  return redirect('index') 
 
def like_post(request):
    current_user = request.user
    
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        image = Image.objects.get(id=image_id)
        
        if current_user in image.liked.all():
            image.liked.add(current_user)
        else:
            image.liked.add(current_user)
            
        like,created = Like.objects.get_or_create(user=current_user,image_id=image_id)  
        
        if not created:
            if like.val == 'Like':
                like.val = 'Unlike'
                
        else:
                like.val = 'Like' 
                
        like.save()
    return redirect('index')  

def user_profile(request,user_id):
    user_profile = Profile.objects.filter(user_id = user_id).first()
    images = Image.objects.filter(user_id = user_id)

    return render(request, 'userprofile.html', {'user_profile':user_profile, 'images':images})     
  
def search_results(request):

    if 'posts' in request.GET and request.GET["posts"]:
        search_term = request.GET.get("posts")
        searched_posts = Image.search_by_name(search_term)
        message = search_term

        return render(request, 'all-temps/search.html',{"message":message,"posts": searched_posts})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all-temps/search.html',{"message":message})
        

