from distutils.command.config import config
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from BlogApp.models import ContactUs,Post,BlogComment
from django.contrib import messages
from django.core.mail import send_mail
from .models import CustomUser
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from BlogApp.Password.generate_token import account_activation_token
from django.core.mail import EmailMessage



# Create your views here.
def baseloginlogout(request):
    return render(request,'BlogApp/baseloginlogout.html')

def basesignup(request):
    if request.method=='POST':
        fname=request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        mobile_no=request.POST['mobile']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        if pass1 != pass2:
            messages.error(request, 'password do not match')
            return redirect('basesignup')


        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            myuser = CustomUser.objects.create_user(email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.mobile_no=mobile_no
            myuser.is_active=False
            myuser.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('BlogApp/acc_active_email.html', {
                'user': myuser,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token':account_activation_token.make_token(myuser),
            })
            print(message)
            to_email = email
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.content_subtype = 'html'
            email.send()
            messages.success(request, "Please confirm your email address to complete the registration")
            return render(request, 'BlogApp/basesignup.html')
        else:
            messages.error(request, "please choose a unique user")
            return render(request, 'BlogApp/basesignup.html')


        #here User is a table conatin Admin interface in which we create the user
    else:
        return render(request,'BlogApp/basesignup.html')


def baselogin(request):
    if request.method == 'POST':
        email = request.POST.get('loginemail')
        password = request.POST.get('loginpassword')
        #to authenticate user and password  si valid or not djnago provide an inbuilt module autheticate,
        user=authenticate(email=email,password=password)#here we authenticate username and password
        print(user)
        if user is not None and user.is_active is True:#means user and password is  valid
            login(request,user)#means then user can login
            messages.success(request,'user login successfully')
            return redirect('home')
        elif user and user.is_active is False:
            messages.success(request,'Please Verify Your email')
            return render(request, 'BlogApp/baselogin.html')
        # elif user is None:
        #     messages.error(request,'Account does not exist')
        #     return render(request, 'BlogApp/baselogin.html')
        else:
            messages.error(request,'invalid email/password please try again')
            return render(request, 'BlogApp/baselogin.html')

    return render(request,'BlogApp/baselogin.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request,user)
        messages.success(request,'Thank you for your email confirmation. Now you can login your account.')
        return render(request,'BlogApp/baselogin.html')

    else:
        messages.error(request,'Activation link is invalid!')
        return render(request,'BlogApp/baselogin.html')

        
        


@login_required(login_url='/')
def home(request):
    post = Post.objects.all().order_by('-timestamp')[0]
    return render(request,'BlogApp/home.html',{'post':post})

@login_required(login_url='/')
def blog(request):
      post=Post.objects.all()
      return render(request,'BlogApp/blog.html',{'post':post})

@login_required(login_url='/')
def blogpost(request,slug):
    post=Post.objects.filter(slug=slug)
    comment=BlogComment.objects.filter(post__in=post)#it retrives comment according to the post and post will conatined in the post table but it gives reference to blogComment
    return render(request,'BlogApp/blogpost.html',{'post':post,'comment':comment})


@login_required(login_url='/')
def aboutus(request):
    return render(request,'BlogApp/aboutus.html')
    
@login_required(login_url='/')
def contactus(request):
    if request.method=='POST':
        name=request.POST['name']#here we provide value conatin in name attrbute in html form
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
    return render(request, 'BlogApp/contactus.html')

@login_required(login_url='/')
def searchpost(request):
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

@login_required(login_url='/')
def userlogout(request):
    #del request.session['uid']
    logout(request)#which persion is logged it logout
    messages.success(request,'user logout successfully')
    return redirect('baselogin')

@login_required(login_url='/')
def blogComment(request):
    if request.method=='POST':
        comment=request.POST.get('comment')
        user=request.user
        postsno=request.POST.get('postno')
        post=Post.objects.get(serialno=postsno)
        comment=BlogComment(comment=comment,user=user,post=post)
        comment.save()
        messages.success(request, "comment submit successfully")
        return redirect('blogpost',slug=post.slug)
    
    
@login_required(login_url='/')   
def changePassword(request):
    if request.method=='POST':
        old_password=request.POST['oldPassword']
        new_password=request.POST['newPassword']
        confirm_password=request.POST['confirmPassword']
        
        if new_password!=confirm_password:
            messages.error(request,"password does not match")
            return render(request,'BlogApp/change_password.html')
    
        user=CustomUser.objects.get(email=request.user.email)
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            messages.success(request,'Password Changed Successfully')
            return render(request, 'BlogApp/baselogin.html')

        else:
            messages.error(request,'Old Password is invalid please try again')
            return render(request,'BlogApp/change_password.html')
    return render(request,'BlogApp/change_password.html')
