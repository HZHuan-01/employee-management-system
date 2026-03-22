from django.db import models


class Department(models.Model):
    """部门表"""
    title = models.CharField(max_length=20, verbose_name="Department Title")
    def __str__(self):
        return self.title


class Employee(models.Model):
    """职员表"""
    name = models.CharField(max_length=20, verbose_name="姓名")
    password = models.CharField(max_length=20, verbose_name="密码")
    age = models.IntegerField(verbose_name="年龄")
    # DecimalField可以表示更精确的小数 不过要用 max_digits=, decimal_places= 加以限定 默认值设为0
    account = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="余额")
    create_time = models.DateTimeField(verbose_name="入职时间")
    # 不能是字符串1
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    # 级联删除
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="部门")
    # 删除后置空
    # depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)



