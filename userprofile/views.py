from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.http import  HttpResponse
from .forms import UserLoginForm, UserRegisterForm
from .models import  Profile
from .forms import ProfileForm

# 用户验证.
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)#POST请求方式需要添加requeset.POST参数
        print(user_login_form.is_valid())
        # print(user_login_form.cleaned_data)
        if user_login_form.is_valid():
            # .cleaned_data 清洗出合法数据 没有()
            data =  user_login_form.cleaned_data
            # 检验账号、密码是否正确匹配数据库中的某个用户
            # 如果均匹配则返回这个 user 对象
            user = authenticate(username = data['username'],password = data['password'])
            if user:
                # 将用户数据保存在 session 中，即实现了登录动作
                login(request,user)
                return redirect('article:article_list')
            else:
                return HttpResponse("用户名或密码输入有误，请重新输入！")
        else:
            return HttpResponse('账号或mima不合法')
    elif request.method == 'GET':
        user_login_form = UserLoginForm()#get 请求没有request.POST
        context = {
            'user_login_form':user_login_form,
        }
        return render(request,'login.html',context=context)
    else:
        return HttpResponse("请求方式有误")


#用户退出
def user_logout(request):
    logout(request)
    return redirect('article:article_list')


#用户注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data = request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            #设置密码
            new_user.set_password(user_register_form.cleaned_data.get('password'))
            new_user.save()
            #保存数据后立即登录并返回博客列表页面
            login(request,new_user)
            return redirect('article:article_list')
        else:
            return HttpResponse('注册表单输入有误，请重新输入')
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {
            'form':user_register_form,
        }
        return render(request,'register.html',context=context)
    else:
        return HttpResponse("请使用GET或POST请求数据")




#用户信息的删除
@login_required(login_url='/user/login')
def user_delete(request,id):
    if request.method == 'POST':
        user = User.objects.get(id = id)
        if request.user ==user:
            logout(request)
            user.delete()
            return redirect('article:article_list')
        else:
            return HttpResponse("你没有操作的权限")
    else:
        return HttpResponse("仅接受post请求。")





# 编辑用户信息
@login_required(login_url='/user/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)
    # user_id 是 OneToOneField 自动生成的字段
    #修改前
    #profile = Profile.objects.get(user_id=id)
    #修改后
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        # 验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse("你没有权限修改此用户信息。")

        #profile_form = ProfileForm(data=request.POST)
        profile_form = ProfileForm(request.POST,request.FILES)
        if profile_form.is_valid():
            # 取得清洗后的合法数据
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            # 添加在 profile.bio = profile_cd['bio'] 后面‘
            if 'avatar' in request.FILES:#类似字典查询键
                profile.avatar = profile_cd['avatar']
            # 如果 request.FILES 存在文件，则保存
            profile.save()
            # 带参数的 redirect()
            return redirect("userprofile:user_edit", id=id)
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")

    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = { 'profile_form': profile_form, 'profile': profile, 'user': user }
        return render(request, 'edit.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")

