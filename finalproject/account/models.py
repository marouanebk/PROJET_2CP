from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator
# from cal.models import Event
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist

class MyAccountManager(BaseUserManager):
	def create_user(self, email,first_name,last_name, password=None):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=self.normalize_email(email),
			first_name = first_name,
			last_name = last_name,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email,first_name,last_name, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			first_name=first_name,
			last_name=last_name,
		)
		user.is_patient=False
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	# username 				= models.CharField(max_length=30, unique=True)
	first_name				= models.CharField(max_length=20,blank=True)
	last_name 				= models.CharField(max_length=20,blank=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	phone_number			= models.IntegerField(max_length=10,null=True,blank=True,validators=[MaxValueValidator(9999999999)])
	date_of_birth 			= models.DateTimeField(blank=True, null = True)
	place_of_birth 			= models.CharField(max_length=20,null=True,blank=True)
	profile_picture 		= models.ImageField(blank=True , null=True , upload_to="media/images/profiles")


	is_patient 				= models.BooleanField(default=True)
	is_doctor 				= models.BooleanField(default=False)
	is_assistant			= models.BooleanField(default=False)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	hist_code               = models.PositiveIntegerField(null=True, validators=[MaxValueValidator(999999)])
	is_email_verified		= models.BooleanField(default=False)
	# calendar 				= models.ForeignKey(Event,related_name='Event',blank=True, null = True,on_delete=models.CASCADE,)


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name','last_name']

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	def full_name(self):
		return self.last_name+" "+self.first_name

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

	def get_role(self):
		if self.is_admin:
			return "admin"
		elif self.is_staff:
			return "mod"
		elif self.is_doctor:
			return "Doctor"
		elif self.is_patient:
			return "patient "


class Profile(models.Model):
	user = models.OneToOneField(Account, on_delete=models.CASCADE )
	bio = models.TextField(max_length=500, blank=True)
	phone_number = models.CharField(max_length=12, blank=True)
	diplomes_nationaux_universitaire = models.TextField(max_length=500, blank=True)
	urgcontact = models.TextField(max_length=500, blank=True)
	lieu_cab = models.TextField(max_length=500, blank=True)
	coordonnees = models.TextField(max_length=500, blank=True)
	info_pratique = models.TextField(max_length=500, blank=True)
	diplomes = models.TextField(max_length=500, blank=True)
	experiences = models.TextField(max_length=500, blank=True)
	horaire = models.CharField(max_length=50, blank=True)
	specialite = models.CharField(max_length=50)
	profile_image = models.ImageField(default='user.svg', upload_to='account/', null=True, blank=True)
	public	  = models.BooleanField(default=True)
    
	def __str__(self):
		return '%s %s' % (self.user.first_name, self.user.last_name)




@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Account)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()













