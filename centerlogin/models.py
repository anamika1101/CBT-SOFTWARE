from django.db import models
from companylogin.models import Center, Test


class CenterStudent(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
    ]

    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name="students")
    roll_no = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    course = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("center", "roll_no")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.roll_no} - {self.name}"


class ExamAssignment(models.Model):
    STATUS_CHOICES = [
        ("ASSIGNED", "Assigned"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    ]

    center = models.ForeignKey(Center, on_delete=models.CASCADE, related_name="exam_assignments")
    student = models.ForeignKey(CenterStudent, on_delete=models.CASCADE, related_name="exam_assignments")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="center_assignments")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ASSIGNED")
    score = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "test")
        ordering = ["-assigned_at"]

    def __str__(self):
        return f"{self.student.name} -> {self.test.test_name}"
