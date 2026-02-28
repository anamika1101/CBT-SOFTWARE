from django.db import models

class Test(models.Model):
    test_name = models.CharField(max_length=128)
    no_of_questions = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    status = models.CharField(max_length=128,default="Active")
    
    def __str__(self):
        return self.test_name
    
class Center(models.Model):
    center_name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    phone = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    profile_pic = models.FileField(upload_to='profile_pic/',null=True,default=None)
    password = models.CharField(max_length=128)
    
    def __str__(self):
        return self.center_name
    
class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True, blank=True, related_name='questions')
    question = models.CharField(max_length=512)
    option_1 = models.CharField(max_length=256)
    option_2 = models.CharField(max_length=256)
    option_3 = models.CharField(max_length=256)
    option_4 = models.CharField(max_length=256)
    correct_option = models.CharField(max_length=256)
    marks = models.PositiveIntegerField()
    
    def __str__(self):
        return self.question
