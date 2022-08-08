from django.db import models
from django.core.validators import *

# professors database
class Professor (models.Model):
    professor_id = models.CharField(max_length=10, unique=True, null=False)
    professor_name = models.CharField(max_length=30, null=False)

    def __str__(self):
        return '%s, %s' % (self.professor_name, self.professor_id)

# modules database
class Module (models.Model):
    module_code = models.CharField(max_length=4, unique=True, null=False)
    module_name = models.CharField(max_length=50, null=False)
    module_professor=models.ManyToManyField(Professor)
    year = models.CharField(null=False, max_length=4, validators=[MinLengthValidator(4)])
    semester = models.PositiveIntegerField(null=False, validators=[MinValueValidator(1), MaxValueValidator(2)])

    def __str__(self):
        #messy way to get the professors to appear by name for the view and average commands
        for name in self.module_professor.all():
            prof=", ".join(str(name))
        return '%s, %s, Semester %s, %s ' % (self.module_name, self.module_code, self.semester, self.year)

#rating database
#using two foreignkeys on professor and module for precise results for the rate and average commands
class Rating (models.Model):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0, null=False, validators=[MinValueValidator(1), MaxValueValidator(5)])
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return 'Professor %s has a rating of  %s in module %s' % (self.professor, self.rating, self.module)
