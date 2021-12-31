from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from BlogApp.models import ContactUs,Post,BlogComment
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def baseloginlogout(request):
    return render(request,'BlogApp/baseloginlogout.html')

def basesignup(request):
    if request.method=='POST':
        username=request.POST['username']
        fname=request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if pass1 != pass2:
            messages.error(request, 'password do not match')
            return redirect('basesignup')


        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request, "your account has been sucessfully created now you can login")
            return render(request, 'BlogApp/basesignup.html')
        else:
            messages.error(request, "please choose a unique user")
            return render(request, 'BlogApp/basesignup.html')


        #here User is a table conatin Admin interface in which we create the user
    else:
        return render(request,'BlogApp/basesignup.html')


def baselogin(request):
    if request.method == 'POST':
        username = request.POST['loginname']
        password = request.POST['loginpasword']
        #to authenticate user and password  si valid or not djnago provide an inbuilt module autheticate,
        user=authenticate(username=username,password=password)#here we authenticate username and password
        if user is not None:#means user and password is  valid
            request.session['uid'] = request.POST['loginname']
            login(request,user)#means then user can login
            messages.success(request,'user login successfully')
            return redirect('home')
        else:
            messages.error(request,'invalid username and password please try again')
            return render(request, 'BlogApp/baselogin.html')

    return render(request,'BlogApp/baselogin.html')

def home(request):
    if request.session.has_key('uid') and request.method == "GET":
               post = Post.objects.all().order_by('-timestamp')[0]
               return render(request,'BlogApp/home.html',{'post':post})

def blog(request):
    if request.session.has_key('uid') and request.method == "GET":
      post=Post.objects.all()
      return render(request,'BlogApp/blog.html',{'post':post})
    else:
        return render(request, 'BlogApp/baselogin.html')

def blogpost(request,slug):
    if request.session.has_key('uid') and request.method == "GET":
     post=Post.objects.filter(slug=slug)
     comment=BlogComment.objects.filter(post__in=post)#it retrives comment according to the post and post will conatined in the post table but it gives reference to blogComment
     return render(request,'BlogApp/blogpost.html',{'post':post,'comment':comment})
    else:
        return render(request, 'BlogApp/baselogin.html')


def aboutus(request):
    if request.session.has_key('uid') and request.method == "GET":
        return render(request,'BlogApp/aboutus.html')
    else:
        return render(request, 'BlogApp/baselogin.html')

def contactus(request):
    if request.session.has_key('uid') and request.method=="GET":
        return render(request, 'BlogApp/contactus.html')
    elif request.method=='POST':
        name=request.POST[' name']#here we provide value conatin in name attrbute in html form
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
       #here we create a model object beacuse here we do not
        #use model based form conecpt here we make directly form in html and after post it come to save function
        if len(name)<3 or len(phone)<10:
            messages.error(request,'please fill the form correctly')
        else:
           contact = ContactUs(name=name, phone=phone, email=email, content=content)
           contact.save()
           messages.success(request,'form is submitted successfully')
           return render(request, 'BlogApp/contactus.html')
    else:
      return render(request,'BlogApp/baselogin.html')


def searchpost(request):
    if request.session.has_key('uid') and request.method == "GET":
     value = request.GET['query']

     if len(value) > 78:
        allpost=[]
     else:
        allposttitle = Post.objects.filter(title__icontains=value)
        allpostcontent=Post.objects.filter(content__icontains=value)
        allpostauthor=Post.objects.filter(author__icontains=value)
        allpost=allposttitle.union(allpostcontent,allpostauthor)
     if len(allpost) ==0:
         messages.warning(request,'no search is found please recheck query')

     return render(request, 'BlogApp/searchpost.html', {'allpost': allpost, 'query': value})
    else:
        return render(request, 'BlogApp/baselogin.html')





def sharebymail(request):
    if request.method=='POST':
        to=request.POST['to']
        subject=request.POST['subject']
        message=request.POST['message']
        postsno = request.POST.get('postno')
        post = Post.objects.get(serialno=postsno)
        send_mail(subject,message,'javashrm@gmail.com',[to],fail_silently=False)
        messages.success(request,'mail sent succeesfully')
        return redirect('blogpost',slug=post.slug)

def userlogout(request):
    #del request.session['uid']
    logout(request)#which persion is logged it logout
    messages.success(request,'user logout successfully')
    return redirect('baselogin')

def blogComment(request):
    if request.method=='POST' and request.session.has_key('uid'):
        comment=request.POST.get('comment')
        user=request.user
        postsno=request.POST.get('postno')
        post=Post.objects.get(serialno=postsno)
        comment=BlogComment(comment=comment,user=user,post=post)
        comment.save()
        messages.success(request, "comment submit successfully")
        return redirect('blogpost',slug=post.slug)