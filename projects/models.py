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
    task_description= models.CharField(max_length=180)
    status = models.CharField(max_length=7, choices=status, default=1)
    due = models.CharField(max_length=7, choices=due, default=1)
    due_date= models.CharField(max_length=80)
    start_date= models.CharField(max_length=80)

    class Meta:
        ordering = ['project', 'task_name']

    def __str__(self):
        return(self.task_name)
    


class ProjectDetails(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)  # Connecting Projects via foreign keys
    problem_statement = models.TextField()
    project_objectives = models.TextField()
    project_scope = models.TextField()
    goals = models.TextField()
    assumptions = models.TextField()
    constraints = models.TextField()

    def __str__(self):
        return f"Project Details for {self.project.name}"
    


from django.db import models

class ProjectedInfo(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)  # Connecting Projects via foreign keys
    
    business_process = models.TextField(blank=True, null=True)
    user_requirements = models.TextField(blank=True, null=True)
    non_functional_requirements = models.TextField(blank=True, null=True)
    user_roles_permissions = models.TextField(blank=True, null=True)
    system_integration = models.TextField(blank=True, null=True)
    technical_architecture = models.TextField(blank=True, null=True)
    data_management = models.TextField(blank=True, null=True)
    ui_interaction_design = models.TextField(blank=True, null=True)
    security_compliance = models.TextField(blank=True, null=True)
    acceptance_criteria = models.TextField(blank=True, null=True)
    project_budget = models.TextField(blank=True, null=True)
    project_timeline = models.TextField(blank=True, null=True)
    risk_management = models.TextField(blank=True, null=True)
    post_deployment_support = models.TextField(blank=True, null=True)
    legal_compliance = models.TextField(blank=True, null=True)
    extra_information = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Projected Info for {self.project.name}"

from django.db import models
from django.contrib.auth.models import User

class Planner(models.Model):
    plannerid = models.CharField(max_length=100, blank=True, null=True)
    teams_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.plannerid or "Unnamed Planner"
