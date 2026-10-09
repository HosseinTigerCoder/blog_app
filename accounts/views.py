from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from core.models import Post
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash,get_user_model
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from templated_mail.mail import BaseEmailMessage
from .forms import RegisterForm,CreatePost,PasswordResetForm,SetNewPasswordForm,ContactUsForm
from .models import Ticket,Reply
from .forms import TicketForm,ReplyForm,ProfileImage

User = get_user_model()

# Create your views here.

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # try:
            User.objects.create_user(username=form.cleaned_data['username'],
                                    email=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'])
            email_obj = BaseEmailMessage(template_name='email.html',context={'username':form.cleaned_data['username'],
                                                                             'email':form.cleaned_data['email'],})
            email_obj.send([form.cleaned_data['email']])
            return redirect('login')
            # except IntegrityError:
            #     form.add_error('username','این نام کاربری قبلا استفاده شده است.')
    else:
        form = RegisterForm()
    return render(request,'registration/register.html',{'form':form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)  # ✅ اینجا form ساخته میشه
        if form.is_valid():
            user = form.get_user()  # فرم خودش user رو میاره
            login(request, user)
            messages.success(request,'شما باموفقیت وارد شدید!')
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form':form})

def logout_user(request):
    logout(request)
    messages.error(request,'شما از سیستم خارج شدید.')
    return redirect('home')

@login_required
def profile_page(request):
    queryset = Post.objects.filter(author=request.user).order_by('-date_created')[:5]

    if request.method == 'POST':
        if 'submit_change_password' in request.POST:
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')

            if old_password and new_password and new_password2:
                if not request.user.check_password(old_password):
                    messages.error(request, 'رمز عبور فعلی اشتباه است')
                else:
                    if new_password == new_password2:
                        request.user.set_password(new_password)
                        request.user.save()   # 🔹 ذخیره تغییر پسورد
                        messages.success(request, 'پسورد با موفقیت تغییر کرد. دوباره وارد شوید.')
                        logout(request)       # 🔹 کاربر رو لاگ‌اوت کن
                        # update_session_auth_hash(request,request.user)
                        return redirect('login')
                    else:
                        messages.error(request, 'پسورد جدید با تکرار آن مطابقت ندارد.')
        elif 'submit-post' in request.POST:
            form = CreatePost(request.POST,request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                messages.success(request,'پست شما ذخیره شد.')
                return redirect('profile')
        elif 'set-profile-image' in request.POST:
            user = request.user
            profile_image = ProfileImage(request.POST,request.FILES,instance=user)
            if profile_image.is_valid():
                profile_image.save()
                messages.success(request,'عکس پروفایل با موفقیت تغییر کرد.')
                return redirect('profile')
        else:
            new_username = request.POST.get('new-username')
            user = request.user
            if not new_username:
                messages.error(request,'لطفا نام کاربری جدید را وارد کنید')
                return redirect('profile')
            if user.username == new_username:
                messages.warning(request,'این همان نام کاربری فعلی شماست')
                return redirect(reverse('profile') + '#changeusername')
            if User.objects.filter(username=new_username).exists():
                messages.error(request,'این نام کاربری موجود است')
                return redirect(reverse('profile') + '#changeusername')
            user.username = new_username
            user.save()
            messages.success(request, 'نام کاربری با موفقیت تغییر کرد.')
            return redirect('profile')  # مسیر دلخواه (مثلاً صفحه پروفایل)
    form = CreatePost()
    profile_image = ProfileImage()        

    context = {
        'profile_image': profile_image,
        'posts': queryset,
        'form': form,
    }
    return render(request, 'registration/profile.html', context)

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data['email']
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error('کاربر با این ایمیل وجود ندارد')
                return redirect('password_reset')
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            link = f"http://{request.get_host()}/accounts/reset/{uid}/{token}/"

            send_mail(
                'Reset password',
                f'سلام {user.username}, روی لینک زیر کلیک کنید \n {link}',
                None,
                [email]
            )
            messages.success(request, "لینک بازنشانی به ایمیل شما ارسال شد.")
            return redirect('password_reset')
    else:
        form = PasswordResetForm()
    return render(request,'registration/password-reset-form.html',{'form':form})

def set_new_password(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and default_token_generator.check_token(user,token):
        if request.method == 'POST':
            form = SetNewPasswordForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['new_password1'])
                user.save()
                messages.success(request,'رمز عبور شما با موفقیت تغییر کرد.')
                return redirect('login')
        else:
            form = SetNewPasswordForm()
        return render(request,'registration/set_new_password.html',{'form':form})
    else:
        messages.error('لینک نامعتبر است یا منقضی شده')
        return redirect('password_reset')
    
def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'پیام شما با موفقیت ارسال شد')
            return redirect('contact_us')
    else:
        return render(request,'registration/contact-us.html',{})

@login_required()
def ticket_list(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request,'ticket/ticket-list.html',{'tickets':tickets})

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('tickets')
    else:
        form = TicketForm()
    return render(request,'ticket/create-ticket.html',{'form':form})

def reply_ticket(request,pk):
    ticket = get_object_or_404(Ticket,pk=pk)
    replies = Reply.objects.filter(ticket=ticket)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.ticket = ticket
            reply.user = request.user
            reply.save()
            return redirect('ticket_detail',pk=pk)
    else:
        form = ReplyForm()
    return render(request,'ticket/detail.html',{'ticket':ticket,'replies':replies,'form':form})