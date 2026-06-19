from django.db import models
from Administrator.models import tbl_activitycategory
from Guest.models import tbl_faculty

class tbl_activity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    activitycategory = models.ForeignKey(tbl_activitycategory, on_delete=models.CASCADE)
    faculty = models.ForeignKey(tbl_faculty, on_delete=models.CASCADE)
    activity_name = models.CharField(max_length=100)
    activity_description = models.TextField()
    activity_credit = models.IntegerField()
    activity_startdate = models.DateField()
    activity_enddate = models.DateField()
    activity_file = models.FileField(upload_to='Assets/ActivityDocs/', null=True, blank=True)
    activity_status = models.IntegerField(default=0) # 0 = Open/Active, 1 = Completed, 2 = Cancelled
    activity_date = models.DateField(auto_now_add=True)
