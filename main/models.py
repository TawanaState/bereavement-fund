from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from datetime import datetime, date


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"  # Set email as the unique identifier
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


# Member Model - Linked to Django's User model
class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    membership_date = models.DateField(auto_created=True)
    gender = models.CharField(default="male", null=True, max_length=50, choices=[('male', 'Male'), ('female', 'Female')])
    phone_number = models.CharField(null=True, max_length=15, verbose_name="Phone Number")
    date_of_birth = models.DateField(null=True, verbose_name="Date Of Birth")
    id_number = models.CharField(null=True, max_length=20, verbose_name="ID Number")
    hit_ec_number = models.CharField(null=True, max_length=20, verbose_name="HIT EC Number")
    residential_address = models.TextField(null=True, blank=True)
    employment_position = models.CharField(null=True, max_length=100)
    extension = models.CharField(null=True, max_length=100)
    fax = models.CharField(null=True, max_length=100)
    department = models.CharField(null=True, max_length=100)
    employment_duration = models.CharField(null=True, max_length=50)
    office_number = models.CharField(null=True, max_length=50)
    # monthly_subscription = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(default="active", null=True, max_length=50, choices=[('active', 'Active'), ('inactive', 'Inactive')])
    # payment_status = models.BooleanField(default=False)  # Track monthly payment status

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def membership_length(self):
        date1 = self.membership_date
        date2 = date.today()
        months = (date2.year - date1.year) * 12 + date2.month - date1.month
        return abs(months)

# Board of Trustees Model - Also Linked to Django's User model
class Trustee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    position = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.user.last_name


# Beneficiary Model
class Beneficiary(models.Model):
    member = models.ForeignKey(Member, related_name='beneficiaries', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, verbose_name="FullName")
    id_number = models.CharField(max_length=20, verbose_name="ID Number")
    relationship_type = models.CharField(max_length=50, choices=[('spouse', 'Spouse'), ('child', 'Child'), ('parent', 'Parent'),('principal', 'Principal'), ('nominee', 'Nominee')], verbose_name="Relationship Type")
    proof_of_relationship = models.FileField(upload_to='beneficiary_proofs/', null=True)
    deceased = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.full_name}({self.relationship_type})'


# Claim Model
class Claim(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    beneficiary = models.OneToOneField(Beneficiary, on_delete=models.DO_NOTHING)
    approved_by = models.ForeignKey(Trustee, on_delete=models.CASCADE, null=True)
    date_filed = models.DateField(auto_now_add=True)
    amount_claimed = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    proof_of_claim = models.FileField(upload_to='claims/')
    description = models.TextField(blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Claim by {self.member} on {self.date_filed}"


# 4. Payment History
class PaymentHistory(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    payment_date = models.DateField(auto_created=True, auto_now_add=True)
    period = models.DateField()
    amount_paid = models.DecimalField(default=2,max_digits=6, decimal_places=2)
    recorded_by = models.ForeignKey(Trustee, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f"Payment for {self.member.user.last_name} on {self.payment_date}"
    
    def disp(self):
        return f'{self.period.strftime("%b")} {self.period.year}'


# 5. Event Log (for tracking changes made by trustees)
class EventLog(models.Model):
    trustee = models.ForeignKey(Trustee, on_delete=models.SET_NULL, null=True)
    event = models.TextField()
    event_type = models.CharField(max_length=20, choices=[('delete', 'Delete'), ('create', 'Create'), ('update', 'Update'), ('other', 'Other')])
    event_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event by {self.trustee.user} on {self.event_date}"


class Setting(models.Model):
    monthly_contribution = models.DecimalField(verbose_name="Monthly Contribution(USD)", default=2, max_digits=6, decimal_places=2)
    grace_period = models.IntegerField(verbose_name="Grace Period(Months)", default=3)
    nominee_claim_amount = models.DecimalField(verbose_name="Nominee Claim Amount(USD)", default=400, max_digits=6, decimal_places=2)
    principal_claim_amount = models.DecimalField(verbose_name="Principal Claim Amount(USD)", default=500, max_digits=6, decimal_places=2)
    spouse_claim_amount = models.DecimalField(verbose_name="Spouse Claim Amount(USD)", default=500, max_digits=6, decimal_places=2)
    child_claim_amount = models.DecimalField(verbose_name="Child Claim Amount(USD)", default=300, max_digits=6, decimal_places=2)
    parent_claim_amount = models.DecimalField(verbose_name="Parent Claim Amount(USD)", default=400, max_digits=6, decimal_places=2)

