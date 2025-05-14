from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


status = (
    ('1', 'Stuck'),
    ('2', 'Working'),
    ('3', 'Done'),
)

due = (
    ('1', 'On Due'),
    ('2', 'Overdue'),
    ('3', 'Done'),
)

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField('shortcut', blank=True)
    assign = models.ManyToManyField(User)
    efforts = models.DurationField()
    status = models.CharField(max_length=7, choices=status, default=1)
    dead_line = models.DateField()
    company = models.ForeignKey('register.Company', on_delete=models.CASCADE)
    complete_per = models.FloatField(max_length=2, validators = [MinValueValidator(0), MaxValueValidator(100)])
    description = models.TextField(blank=True)

    add_date = models.DateField(auto_now_add=True)
    upd_date = models.DateField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return (self.name)


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assign = models.ManyToManyField(User)
    task_name = models.CharField(max_length=80)
    status = models.CharField(max_length=7, choices=status, default=1)
    due = models.CharField(max_length=7, choices=due, default=1)

    class Meta:
        ordering = ['project', 'task_name']

    def __str__(self):
        return(self.task_name)
    


class ProjectDetails(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)  # 通过外键连接Project
    problem_statement = models.TextField()  # 问题陈述
    project_objectives = models.TextField()  # 项目目标
    project_scope = models.TextField()  # 项目范围
    goals = models.TextField()  # 项目目标
    assumptions = models.TextField()  # 假设
    constraints = models.TextField()  # 约束

    def __str__(self):
        return f"Project Details for {self.project.name}"
    


from django.db import models

class ProjectedInfo(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)  # 通过外键连接Project
    
    business_process = models.TextField(blank=True, null=True)  # 允许为空
    user_requirements = models.TextField(blank=True, null=True)  # 允许为空
    non_functional_requirements = models.TextField(blank=True, null=True)  # 允许为空
    user_roles_permissions = models.TextField(blank=True, null=True)  # 允许为空
    system_integration = models.TextField(blank=True, null=True)  # 允许为空
    technical_architecture = models.TextField(blank=True, null=True)  # 允许为空
    data_management = models.TextField(blank=True, null=True)  # 允许为空
    ui_interaction_design = models.TextField(blank=True, null=True)  # 允许为空
    security_compliance = models.TextField(blank=True, null=True)  # 允许为空
    acceptance_criteria = models.TextField(blank=True, null=True)  # 允许为空
    project_budget = models.TextField(blank=True, null=True)  # 允许为空
    project_timeline = models.TextField(blank=True, null=True)  # 允许为空
    risk_management = models.TextField(blank=True, null=True)  # 允许为空
    post_deployment_support = models.TextField(blank=True, null=True)  # 允许为空
    legal_compliance = models.TextField(blank=True, null=True)  # 允许为空
    extra_information = models.TextField(blank=True, null=True)  # 允许为空

    def __str__(self):
        return f"Projected Info for {self.project.name}"

