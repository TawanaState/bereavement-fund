from django.contrib import admin
from .models import CustomUser, Member, Trustee, Beneficiary, Claim, PaymentHistory

# Register CustomUser with specific fields for display
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name',  'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    ordering = ('email',)

# Register Member model with a configuration for displaying fields
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'membership_date', 'status', )
    search_fields = ('user__email', 'user__last_name')
    list_filter = ('status', 'membership_date')
    ordering = ('membership_date',)

# Register BoardOfTrustees model to show relevant information
@admin.register(Trustee)
class TrusteeAdmin(admin.ModelAdmin):
    list_display = ('user', 'position')
    search_fields = ('user__email', 'position')
    ordering = ('position',)

# Register Beneficiary model with customized field displays
@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('member', 'full_name', 'relationship_type')
    search_fields = ('full_name', 'member__user__email')
    list_filter = ('relationship_type',)
    ordering = ('member',)

# Register Claim model with status filter for easy review
@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('member', 'date_filed', 'amount_claimed', 'status')
    search_fields = ('member__user__email', 'status')
    list_filter = ('status', 'date_filed')
    ordering = ('date_filed',)


# Register Payment model with status filter for easy review
@admin.register(PaymentHistory)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('member', 'payment_date', 'amount_paid', 'recorded_by')
    search_fields = ('member', 'recorded_by', 'payment_date')
    list_filter = ('amount_paid', 'payment_date')
    ordering = ('payment_date',)

