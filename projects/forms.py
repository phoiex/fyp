from django import forms
from django.utils.text import slugify
from .models import Task
from .models import Project
from register.models import Company
from django.contrib.auth.models import User

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


class TaskRegistrationForm(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    assign = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    task_name = forms.CharField(max_length=80)
    task_description = forms.CharField(max_length=180, widget=forms.Textarea)
    status = forms.ChoiceField(choices=status)
    due = forms.ChoiceField(choices=due)
    due_date = forms.CharField(max_length=80)
    start_date = forms.CharField(max_length=80)

    class Meta:
        model = Task
        fields = '__all__'

    def save(self, commit=True):
        task = super(TaskRegistrationForm, self).save(commit=False)
        task.project = self.cleaned_data['project']
        task.task_name = self.cleaned_data['task_name']
        task.task_description = self.cleaned_data['task_description']
        task.status = self.cleaned_data['status']
        task.due = self.cleaned_data['due']
        task.due_date = self.cleaned_data['due_date']
        task.start_date = self.cleaned_data['start_date']
        if commit:
            task.save()
            task.assign.set(self.cleaned_data['assign'])
        return task

    def __init__(self, *args, **kwargs):
        super(TaskRegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
        self.fields['project'].widget.attrs['placeholder'] = 'Select Project'
        self.fields['task_name'].widget.attrs['placeholder'] = 'Enter Task Name'
        self.fields['task_description'].widget.attrs['placeholder'] = 'Enter Task Description'
        self.fields['status'].widget.attrs['placeholder'] = 'Select Status'
        self.fields['due'].widget.attrs['placeholder'] = 'Select Due Type'
        self.fields['due_date'].widget.attrs['placeholder'] = 'Enter Due Date'
        self.fields['start_date'].widget.attrs['placeholder'] = 'Enter Start Date'
        self.fields['assign'].widget.attrs['placeholder'] = 'Select Assignees'



class ProjectRegistrationForm(forms.ModelForm):
    name = forms.CharField(max_length=80)
    # slug = forms.SlugField('shortcut')
    assign = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    efforts = forms.DurationField()
    status = forms.ChoiceField(choices=status)
    dead_line = forms.DateField()
    company = forms.ModelChoiceField(queryset=Company.objects.all())
    complete_per = forms.FloatField(min_value=0, max_value=100)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Project
        fields = '__all__'


    def save(self, commit=True):
        Project = super(ProjectRegistrationForm, self).save(commit=False)
        Project.name = self.cleaned_data['name']
        Project.efforts = self.cleaned_data['efforts']
        Project.status = self.cleaned_data['status']
        Project.dead_line = self.cleaned_data['dead_line']
        Project.company = self.cleaned_data['company']
        Project.complete_per = self.cleaned_data['complete_per']
        Project.description = self.cleaned_data['description']
        Project.slug = slugify(str(self.cleaned_data['name']))
        Project.save()
        assigns = self.cleaned_data['assign']
        for assign in assigns:
            Project.assign.add((assign))

        if commit:
            Project.save()

        return Project


    def __init__(self, *args, **kwargs):
        super(ProjectRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Project Name'
        self.fields['efforts'].widget.attrs['class'] = 'form-control'
        self.fields['efforts'].widget.attrs['placeholder'] = 'Efforts'
        self.fields['status'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['placeholder'] = 'Status'
        self.fields['dead_line'].widget.attrs['class'] = 'form-control'
        self.fields['dead_line'].widget.attrs['placeholder'] = 'Dead Line, type a date'
        self.fields['company'].widget.attrs['class'] = 'form-control'
        self.fields['company'].widget.attrs['placeholder'] = 'Company'
        self.fields['complete_per'].widget.attrs['class'] = 'form-control'
        self.fields['complete_per'].widget.attrs['placeholder'] = 'Complete %'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['placeholder'] = 'Type here the project description...'
        self.fields['assign'].widget.attrs['class'] = 'form-control'

from django import forms
from .models import Task
from django.contrib.auth.models import User  




from django import forms
from .models import ProjectDetails

from django import forms
from .models import ProjectDetails

class ProjectDetailsForm(forms.ModelForm):
    class Meta:
        model = ProjectDetails
        fields = ['project', 'problem_statement', 'project_objectives', 'project_scope', 'goals', 'assumptions', 'constraints']
        widgets = {
            'problem_statement': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'placeholder': 'Please describe the problem your project aims to solve.'}),
            'project_objectives': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'placeholder': 'List the key objectives of the project.'}),
            'project_scope': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'placeholder': 'Define the boundaries and limitations of the project.'}),
            'goals': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'placeholder': 'Specify the desired outcomes or goals of the project.'}),
            'assumptions': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'placeholder': 'State any assumptions made during the planning of the project.'}),
            'constraints': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'placeholder': 'List the constraints or limitations of the project.'}),
        }  










from django import forms
from .models import Project, Task, ProjectDetails
from django import forms
from .models import Project, Task, ProjectDetails

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'assign', 'slug', 'efforts', 'status', 'dead_line', 'company', 'complete_per', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'assign': forms.Select(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project shortcut'}),
            'efforts': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Efforts (e.g., 30 00:00:00)'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'dead_line': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'company': forms.Select(attrs={'class': 'form-control'}),
            'complete_per': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the project...'}),
        }

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'task_name', 
            'assign', 
            'status', 
            'due', 
            'task_description', 
            'start_date', 
            'due_date'
        ]
        widgets = {
            'task_name': forms.TextInput(attrs={
                'class': 'form-control font-weight-bold', 
                'placeholder': 'Task name'
            }),
            'assign': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'due': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'task_description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Task description', 
                'rows': 3
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
        }



class ProjectDetailsFormedit(forms.ModelForm):
    class Meta:
        model = ProjectDetails
        fields = ['problem_statement', 'project_objectives', 'project_scope', 'goals', 'assumptions', 'constraints']
        widgets = {
            'problem_statement': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the problem statement...'}),
            'project_objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter project objectives...'}),
            'project_scope': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter project scope...'}),
            'goals': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter project goals...'}),
            'assumptions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter project assumptions...'}),
            'constraints': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter project constraints...'}),
        }


# forms.py
from django import forms
from .models import ProjectedInfo

class ProjectedInfoForm(forms.ModelForm):
    class Meta:
        model = ProjectedInfo
        fields = [
            'project',
            'business_process', 'user_requirements', 'non_functional_requirements',
            'user_roles_permissions', 'system_integration', 'technical_architecture',
            'data_management', 'ui_interaction_design', 'security_compliance',
            'acceptance_criteria', 'project_budget', 'project_timeline', 'risk_management',
            'post_deployment_support', 'legal_compliance', 'extra_information'
        ]
        widgets = {
            'business_process': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}),
            'user_requirements': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}),
            'non_functional_requirements': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}),
            'user_roles_permissions': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}),
            'system_integration': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}),
            'technical_architecture': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}),
            'data_management': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}),
            'ui_interaction_design': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}),
            'security_compliance': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}),
            'acceptance_criteria': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}),
            'project_budget': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}),
            'project_timeline': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}),
            'risk_management': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}),
            'post_deployment_support': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}),
            'legal_compliance': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}),
            'extra_information': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}),
        }
from django import forms
from .models import Planner

class PlannerForm(forms.ModelForm):
    class Meta:
        model = Planner
        fields = ['plannerid', 'teams_id']
