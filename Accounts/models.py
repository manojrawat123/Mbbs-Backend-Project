from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name= None, last_name= None, username= None, email= None, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)

        # Send verification email
        # self.send_verification_email(user)

        return user
    
    def send_verification_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        user.token= token
        user.save()
        
        subject = 'Verify Your Email'
        message = f"Hello ,\n\nPlease verify your email by clicking the link below:\n\n"
        verification_link = f"http://localhost:3000/verify-email/{uid}/{token}/"
        message += verification_link

        from_email = 'sanjayjaiswal121234@gmail.com'  # Replace with your email address
        to_email = user.email
        send_mail(subject, message, from_email, [to_email])

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    first_name      = models.CharField(max_length=50,null= True,blank=True)
    last_name       = models.CharField(max_length=50,null=True,blank=True)
    username        = models.CharField(max_length=50,null= True,blank=True)
    email           = models.EmailField(max_length=100, unique=True)
    password        = models.CharField(max_length=100)
    token           = models.CharField(max_length= 255,default= '')


    # required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=True)
    is_superadmin        = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default= False)  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
    user= models.OneToOneField(User,on_delete= models.DO_NOTHING)
    user_address = models.CharField(max_length=100, blank=True)
    user_phone = models.CharField(max_length=20,blank= True,null= True)
    user_converted = models.BooleanField(default=False)
    user_father_name = models.CharField(max_length=50, blank=True)
    user_dob = models.DateField(blank=True,null=True)
    user_budget = models.DecimalField(max_digits=10, decimal_places=2,null= True,blank=True)
    user_college_preference = models.CharField(max_length=100, blank=True)
    user_profile_image = models.ImageField(upload_to='user_profile_images', blank=True,null= True)
    user_status = models.CharField(max_length=20, choices=[("active","ACTIVE"),("inactive","INACTIVE")],default="active")
    user_created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


#userTransaction
transactionType= ["Semester Fee","College Fee"]
class UserTransactionTable(models.Model):
    user= models.ForeignKey(User,on_delete= models.DO_NOTHING)
    user_payment_date= models.DateTimeField(auto_now_add= True)
    user_amount= models.DecimalField(max_digits=10,decimal_places= 2)
    user_transaction_type= models.CharField(max_length=20,choices= [(type,type) for type in transactionType])

    def __unicode__(self):
        return  self.user_payment_date
    

#userTestInfo    
testType= ["NEET"]
class UserTestInfo(models.Model):
    user= models.OneToOneField(User,models.DO_NOTHING)
    user_test_type= models.CharField(max_length=20,choices= [(type,type) for type in testType])
    user_test_score= models.DecimalField(max_digits=10,decimal_places= 2,null= True,blank=True)
    user_test_date= models.DateField(blank=True,null=True)
    user_test_exp_date= models.DateField(blank=True,null=True)
    user_test_document_image= models.ImageField(upload_to='test_score_image',blank= True,null=True)
    


#ACCOUNT
class Account(models.Model):

    user= models.OneToOneField(User, on_delete= models.DO_NOTHING)
    user_profile= models.OneToOneField(UserProfile, on_delete= models.DO_NOTHING)
    user_test_info= models.OneToOneField(UserTestInfo, on_delete= models.DO_NOTHING)

    def delete(self,*args,**kwargs):
        self.user.is_active= False
        self.user.save()


    def __str__(self):
        return self.user.email




    