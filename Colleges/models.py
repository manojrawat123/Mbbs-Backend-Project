from django.db import models

# Create your models here.
class College(models.Model):
    college_name    = models.CharField(max_length=50)
    college_slug    = models.SlugField()
    college_email   = models.EmailField()
    college_country = models.CharField(max_length=50)
    college_phone   = models.CharField(max_length=13)
    college_contact = models.CharField(max_length=50)
    college_status  = models.CharField(max_length=50, choices=[("active","Active"),("inactive","Inactive")],default="active")
    
    def __str__(self):
        return self.college_name
    

class CollegeMedia(models.Model):
    image = models.ImageField(upload_to='college_images')
    
    def __str__(self):
        return self.image.name
    
class University(models.Model):
    name = models.CharField(max_length=255,null= True)
    location = models.CharField(max_length=255,null= True)
    established_year = models.TextField(null= True)
    medium_of_instruction = models.TextField(null= True)
    temperature_range = models.TextField(max_length=50,null= True)
    visa_success_ratio = models.TextField(null=True ,default= "100 % Visa Success Ratio")
    study_material_worth = models.TextField(null= True,default= "No Entrance Exam")
    hostel_facility = models.TextField(null= True,default= "Best Hostel Facility")
    crime_free_campus = models.TextField(null= True,default= "No crime, ragging free campus")
    no_donation = models.TextField(null=True,default= "No Donation")
    extra_university_info = models.TextField(null= True,default= "Quality Education")

    def __str__(self):
        return self.name


class FeeStructure(models.Model):
    name = models.CharField(max_length=255,null= True)
    tuition_fees = models.JSONField(default=dict({"sem1": 1750, "sem2": 1750, "sem3": 0, "sem4": 0, "sem5": 0, "sem6": 0}),null= True)
    one_time_charges = models.JSONField(default={"sem1": 1750, "sem2": 1750, "sem3": 0, "sem4": 0, "sem5": 0, "sem6": 0},null= True)
    hostel_fees = models.JSONField(default={"sem1": 1750, "sem2": 1750, "sem3": 0, "sem4": 0, "sem5": 0, "sem6": 0},null= True)
    totals = models.JSONField(default={"sem1": 1750, "sem2": 1750, "sem3": 0, "sem4": 0, "sem5": 0, "sem6": 0},null= True)
    
    def __str__(self):
        return self.name


class CollegeInfo(models.Model):
    college = models.OneToOneField(College, on_delete=models.DO_NOTHING, related_name='info')
    college_extra_info= models.OneToOneField(University, on_delete=models.DO_NOTHING, related_name='extra_info',null=True)
    colege_fee_info= models.OneToOneField(FeeStructure, on_delete=models.DO_NOTHING, related_name='fee',null=True)

    college_address               = models.CharField(max_length=200)
    college_fee_total             = models.IntegerField()
    college_course_offered        = models.CharField(max_length=200)
    college_required_twelth_marks = models.FloatField()
    college_exam_accepted         = models.CharField(max_length=100)
    college_scholarship           = models.PositiveIntegerField()
    college_course_duration       = models.PositiveIntegerField()
    college_media                 = models.ManyToManyField(CollegeMedia, blank=True, related_name='colleges')
    college_description           = models.TextField()
    college_intake_session        = models.CharField(max_length=30)
    college_yt_video              = models.URLField()

    def delete(self,*args,**kwargs):
        self.college.college_status= 'inactive'
        self.college.save()


    def __str__(self):
        return self.college.college_name


