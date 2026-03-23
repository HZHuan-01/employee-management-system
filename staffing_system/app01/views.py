from django.shortcuts import render, redirect


from app01 import models
from app01.models import Department
from app01.models import Employee
from django import forms


def department_list(request):
    info = request.session.get('info')
    if not info:
        return redirect('/login/')
    # queryset是一个可迭代对象 比list更高级 懒加载：只有用的时候才查
    # models是我的模块 Department是我模块中的表的映射 用objects工具 执行all
    print(request.session['info'])
    queryset = models.Department.objects.all()
    return render(request, 'department_list.html', {'queryset': queryset})


def department_add(request):
    if request.method == 'POST':
        models.Department.objects.create(title=request.POST['title'])
        return redirect('/department/list/')
    return render(request, "department_add.html")


def department_delete(request):
    # 这里的nid通过get获取
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect('/department/list/')



    # url传过来的路径参数nid需要函数接收
def department_edit(request, nid):
    if request.method == 'GET':
        data = models.Department.objects.filter(id=nid).first()
        return render(request, "department_edit.html", {'data': data})
    title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/department/list/')

def user_list(request):
    info = request.session.get('info')
    if not info:
    # 用python方法取
    # for i in queryset:
    #     print(i.id,
    #           i.name,
    #           i.password,
    #           i.age,
    #           i.account,
    #           # 格式化输出
    #           i.create_time.strftime('%Y-%m-%d'),
    #           #i.department是一个可迭代对象 django内置方法调出另一个表
    #           i.department.title,
    #           i.get_gender_display())
        return redirect('/login/')
    queryset = models.Employee.objects.all()
    print(request.session['info'])
    return render(request, "employee_list.html", {'queryset': queryset})

# 传统方法一个一个取 冗长 不安全
def user_add(request):
    if request.method == 'GET':
        queryset = models.Department.objects.all()
        return render(request, "employee_add.html", {"queryset": queryset})

    name = request.POST.get('user')
    password = request.POST.get('psw')
    age = request.POST.get('age')
    account = request.POST.get('ac')
    create_time = request.POST.get('ctime')
    gender = request.POST.get('gender')
    department_id = request.POST.get('dep')

    models.Employee.objects.create(name=name, password=password, age=age, account=account, create_time=create_time,
                                   gender=gender, department_id=department_id)
    return redirect('/user/list/')

# ModelForm基于数据库生成的表单 Form想要什么字段自己定义
class MyForm(forms.ModelForm):
    class Meta:
        # 用哪个表
        model = Employee
        # 用哪些字段
        fields = '__all__'
        # widgets = {
        # "name": forms.TextInput(attrs={'class': 'form-control'}),
        # "password": forms.PasswordInput(attrs={'class': 'form-control'}),
        # "age": forms.TextInput(attrs={'class': 'form-control'}),
        # "account": forms.NumberInput(attrs={'class': 'form-control'}),
        # "create_time": forms.TextInput(attrs={'class': 'form-control'}),
        # "gender": forms.Select(attrs={'class': 'form-control'}),
        # "department": forms.Select(attrs={'class': 'form-control'}),
        # }

    # *arg接收位置参数 **kwarg接收关键字参数
    # 不是必须的 用来自定义表单显示效果 初始化表单结构/样式
    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)
        # 这里的field是对象 fields.values是一个方法
        for field in self.fields.values():
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label}

def user_add_modelform(request):
    if request.method == 'GET':
        return render(request, "employee_add_modelform.html", {'form': MyForm()})  # 传入一个空表单
    # 实例化一个对象 这个对象长什么样在MyForm中描述了
    # 这里request.POST实际上是QueryDict类似字典的键值对数据 不是把表单传给form 而是用表单提交的数据创建一个表单对象
    # 所以说这个form是表单对象 form.field也是对象
    form = MyForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    else:
        return render(request, "employee_add_modelform.html", {'form': form})  # 同时将错误的form还回去

def user_edit(request, nid):
    # filter是筛选 但是结果统一还是一个queryset仍然需要first来取出其中的第一个对象
    # 可以用get方法但是如果id对应的不存在会报错 所以还是用filter筛选
    row_object = models.Employee.objects.filter(id=nid).first()
    if request.method == 'GET':
        # instance数据回显 提交的时候拿来更新
        form = MyForm(instance=row_object)
        return render(request, "employee_edit.html", {'form': form})
    # 加了instance才知道是更新 instance表示我要操作这个对象
    form = MyForm(request.POST, instance=row_object)
    if form.is_valid():
        # 默认提交用户上传的数据 如果想要在用户输入以外增加一些值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')
    # 如果校验不成功还是回到编辑页面显示错误
    return render(request, "employee_edit.html", {'form': form})  # 同时将错误的form还回去

def user_delete(request, nid):
    models.Employee.objects.filter(id=nid).delete()
    return redirect('/user/list/')

# 一个功能应该自己有表单类
class login_form(forms.ModelForm):
    class Meta:
        model = Employee
        fields = 'name','password'

    def __init__(self, *args, **kwargs):
        super(login_form, self).__init__(*args, **kwargs)
        # 这里的field是对象 fields.values是一个方法
        for field in self.fields.values():
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label}

def login(request):
    if request.method == 'GET':
        return render(request,"login.html", {'form':login_form()})
    form = login_form(request.POST)
    # form.is_valid做的事是检查字段是否存在 类型是否正确 按字符规则处理
    # 验证的是我login_form的规则 是表单合法性校验 不是业务逻辑校验
    if form.is_valid():
        # cleaned_data是 校验+转换+清洗
        name = form.cleaned_data.get('name')
        password = form.cleaned_data.get('password')
        # 判断库中是否有同时符合name和password的
        i = models.Employee.objects.filter(name=name, password=password).first()
        if i:
            # session本质是字典 这里赋值给info字典
            request.session['info'] = {"name":i.name,"id":i.id}
            return redirect('/index/')

    return render(request,"login.html", {'form':form ,'error': '用户账号或密码错误'})

def logout(request):
    request.session.clear()
    return redirect('/index/')

def register(request):
    return redirect('/user/add/modelform/')

def index(request):
    return render(request,"index.html")



















