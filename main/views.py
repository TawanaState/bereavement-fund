from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Member, Trustee, Beneficiary, Claim, PaymentHistory, EventLog, CustomUser, Setting
from .forms import MemberForm, ClaimForm, BeneficiaryForm, LoginForm, MemberDetailForm, TrusteeForm, ChangePasswordForm, AccountForm, SettingsForm

@login_required
def index(request):
    if hasattr(request.user, 'trustee'):
        return redirect("main:trustee_dashboard")
    if hasattr(request.user, 'member'):
        return redirect("main:member_dashboard")
    return redirect("main:signup")


def signup_view(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a member profile linked to the user
            # Member.objects.create(user=user)
            login(request, user)
            messages.info(request, "Let's finish setting up your account. ")
            return redirect('main:update_member_profile')
        else:
            messages.error(request, "You submitted invalid information, please check for errors. ")
            return render(request, 'signup.html', {'form': form})
    else:
        form = MemberForm()
        return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Welcome back!")
                if hasattr(user, 'Trustee'):
                    return redirect('main:trustee_dashboard')
                elif hasattr(user, 'member'):
                    return redirect('main:member_dashboard')
            else:
                messages.error(request, 'Invalid email or password')
                return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            if request.user.check_password(old_password):
                myuser = CustomUser.objects.get(email=request.user.email)
                myuser.set_password(new_password)
                myuser.save()
                logout(request)
                messages.success(request, "The user's password was changed successfully. ")
                return redirect("main:login")
            else:
                messages.error(request, "The old password you entered is incorrect!")
                return render(request, 'form.html', {'form': form, 'title' : 'Change Password'})
        else:
            messages.error(request, "The passwords you entered are invalid!")
            return render(request, 'form.html', {'form': form, 'title' : 'Change Password'})
    else:
        form = ChangePasswordForm()
        return render(request, 'form.html', {'form': form, 'title' : 'Change Password'})


@login_required
def account_details(request):
    if request.method == "POST":
        form = AccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            logout(request)
            messages.success(request, "The user's details were changed successfully. ")
            return redirect("main:login")
        else:
            messages.error(request, "The information you entered is invalid!")
            return render(request, 'form.html', {'form': form, 'title' : 'Account Settings'})
    else:
        form = AccountForm(instance=request.user)
        return render(request, 'form.html', {'form': form, 'title' : 'Account Settings'})


@login_required
def logout_view(request):
    logout(request)
    return redirect('main:login')


@login_required
def update_member_profile(request):
    member = request.user.member  # Retrieve the member associated with the logged-in user
    if request.method == 'POST':
        form = MemberDetailForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('main:member_dashboard')
        else:
            messages.error(request, "You submitted invalid information, please check for errors. ")
            return render(request, 'member-form.html', {'form': form})
    else:
        form = MemberDetailForm(instance=member)
        return render(request, 'member-form.html', {'form': form, 'title' : "Update member Details", 'subtitle' : member.user})


@login_required
def member_dashboard(request):
    if not hasattr(request.user, 'member'):
        return HttpResponse('Unauthorized', status=401)
    member = request.user.member
    history = PaymentHistory.objects.filter(member=member).order_by("-payment_date")[:3]
    beneficiaries = member.beneficiaries.all()
    return render(request, 'member_dashboard.html', {'member': member, 'rclaims': Claim.objects.filter(member=member, status = "rejected"), 'aclaims': Claim.objects.filter(member=member, status = "approved"), 'beneficiaries': beneficiaries, 'history' : history, "title" : f'Welcome {request.user.member}'})


@login_required
def member_info(request, member_id):
    if not hasattr(request.user, 'trustee'):
        return HttpResponse('Unauthorized', status=401)
    member = get_object_or_404(Member, id=member_id)
    claims = Claim.objects.filter(member=member)
    beneficiaries = member.beneficiaries.all()
    istrustee = Trustee.objects.filter(user = member.user).exists()
    mtrustee = None
    if istrustee:
        mtrustee = Trustee.objects.get(user = member.user)
    print(PaymentHistory.objects.filter(member=member, period = datetime(datetime.today().year, datetime.today().month, 1)))
    fpaid = PaymentHistory.objects.filter(member=member, period__year = datetime.today().year, period__month = datetime.today().month).exists()
    return render(request, 'member_details.html', {'member': member, 'claims': claims, 'beneficiaries': beneficiaries, 'trustee' : mtrustee, "title" : "Member Details", "fullypaid" : fpaid})


@login_required
def member_list(request):
    if not hasattr(request.user, 'trustee'):
        return HttpResponse('Unauthorized', status=401)

    memberslist = Member.objects.all()

    if 'query' in request.GET:
        query = request.GET['query']
        memberslist = Member.objects.filter(
                Q(user__first_name__icontains=query) | 
                Q(user__last_name__icontains=query) | 
                Q(user__email__icontains=query) | 
                Q(hit_ec_number=query) |
                Q(id_number=query)  # Assuming `id` represents the ID number for the member
            )
    return render(request, 'member_list.html', {"members" : memberslist, "title" : "Members List"})

@login_required
def member_delete(request, member_id):
    if not hasattr(request.user, 'trustee'):
        return HttpResponse('Unauthorized', status=401)
    oldmember = Member.objects.get(id = member_id)
    
    EventLog.objects.create(event = f'Deleted Trustee ({oldmember.user.first_name + oldmember.user.last_name})', event_type = "delete", trustee = Trustee.objects.get(user = request.user))
    # oldmember.delete()
    CustomUser.objects.get(email = Member.objects.get(id = member_id).user.email).delete()
    messages.success(request, "The member was successfully deleted!")
    return redirect("main:member_list")


@login_required
def trustee_dashboard(request):
    if not hasattr(request.user, 'trustee'):
        return HttpResponse('Unauthorized', status=401)
    claims = Claim.objects.filter(status='pending')  # List pending claims

    ## Setting the Settings if they don't exists --->
    if Setting.objects.all().first() == None:
        Setting.objects.create(
            monthly_contribution = 2
        )
    
    return render(request, 'trustee_dashboard.html', {
        'pending_claims': claims,
        "members_count" : Member.objects.all().count(),
        'trustees_count' : Trustee.objects.all().count(),
        'beneficiaries_count' : Beneficiary.objects.all().count(),
        'claims_count' : Claim.objects.all().count(),
        'events' : EventLog.objects.order_by("-event_date")[:20],
        "title" : "Trustee Dashboard"
    })


@login_required
def trustee_analytics(request):
    if not hasattr(request.user, 'trustee'):
        return HttpResponse('Unauthorized', status=401)
    
    return render(request, 'trustee_analytics.html', {
        "title" : "Trustee Dashboard"
    })

@login_required
def create_trustee(request, member_id):
    if not hasattr(request.user, 'trustee'):
        return HttpResponse('Unauthorized', status=401)
    if request.method == "POST":
        form = TrusteeForm(request.POST)
        if form.is_valid():
            newtrustee = form.save(commit=False)
            newtrustee.user = Member.objects.get(id=member_id).user
            newtrustee.save()
            EventLog.objects.create(event = f'Created Trustee({newtrustee.user.first_name + newtrustee.user.last_name})', event_type = "create", trustee = Trustee.objects.get(user = request.user))
            messages.success(request, "The Trustee was created successfully. ")
            return redirect('main:member_info', member_id)
        else:
            messages.error(request, "You submitted invalid information, please check the errors. ")
            return render(request, 'trustee-form.html', {'form': form, 'title' : "Create Trustee", 'subtitle' : Member.objects.get(id=member_id).user})
    else:
        form = TrusteeForm()
        return render(request, 'trustee-form.html', {'form': form, 'title' : "Create Trustee", 'subtitle' : Member.objects.get(id=member_id).user})


@login_required
def update_trustee(request, trustee_id):
    if not hasattr(request.user, 'trustee'):
        return HttpResponse('Unauthorized', status=401)
    og_trustee = Trustee.objects.get(id=trustee_id)

    if og_trustee.user == request.user:
        messages.error(request, "You cannot edit your own trustee details. ")
        return redirect("main:trustee_dashboard")
    if request.method == "POST":
        form = TrusteeForm(request.POST, instance=og_trustee)
        if form.is_valid():
            form.save()
            EventLog.objects.create(event = f'Updated Trustee({og_trustee.user.first_name + og_trustee.user.last_name})', event_type = "update", trustee = Trustee.objects.get(user = request.user))
            messages.success(request, "The Trustee was updated successfully...")
            return redirect('main:member_info', Member.objects.get(user = og_trustee.user).pk)
        else:
            messages.error(request, "You submitted invalid information, please check the errors. ")
            return render(request, 'trustee-form.html', {'form': form, 'title' : "Update Trustee", 'subtitle' : og_trustee.user})
    else:
        form = TrusteeForm(instance=og_trustee)
        return render(request, 'trustee-form.html', {'form': form, 'title' : "Create Trustee", 'subtitle' : og_trustee.user})


@login_required
def delete_trustee(request, trustee_id):
    if not hasattr(request.user, 'trustee'):
        return HttpResponse('Unauthorized', status=401)
    og_trustee = Trustee.objects.get(id=trustee_id)
    memberid = Member.objects.get(user = og_trustee.user).pk

    if og_trustee.user == request.user:
        return redirect("main:trustee_dashboard")
    EventLog.objects.create(event = f'Deleted Trustee({og_trustee.user.first_name + og_trustee.user.last_name})', event_type = "delete", trustee = Trustee.objects.get(user = request.user))
    og_trustee.delete()
    messages.success(request, "The Trustee was deleted successfully...")
    return redirect("main:member_info", memberid)


@login_required
def create_claim(request):
    if not hasattr(request.user, 'member'):
        return HttpResponse('Unauthorized', status=401)
    
    graceperiod = Setting.objects.first().grace_period
    if not request.user.member.membership_length() >= graceperiod:
        messages.error(request, f"You need to atleast have been a member for {graceperiod} months for you to claim anything. ")
        return redirect('main:member_dashboard')

    if request.method == 'POST':
        form = ClaimForm(request.POST, request.FILES, qset=Beneficiary.objects.filter(member = request.user.member, deceased = False))
        if form.is_valid():
            claim = form.save(commit=False)
            claim.member = request.user.member
            claim.save()
            messages.success(request, 'Claim submitted successfully')
            return redirect('main:member_dashboard')
        else:
            messages.error(request, "The claim could not be created. Please fix the errors on your entries. ")
            return render(request, 'member-form.html', {'form': form, 'title' : "Submit a claim"})
    else:
        form = ClaimForm(qset=Beneficiary.objects.filter(member = request.user.member, deceased = False))
        return render(request, 'member-form.html', {'form': form, 'title' : "Submit a claim"})


@login_required
def update_claim(request, claim_id):
    if not hasattr(request.user, 'member'):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        form = ClaimForm(request.POST, request.FILES, instance=Claim.objects.get(id=claim_id), qset=Beneficiary.objects.filter(member = request.user.member, deceased = False))
        if form.is_valid():
            form.save()
            messages.success(request, 'Claim updated successfully')
            return redirect('main:claim_list')
        else:
            messages.error(request, "The claim could not be updated. Please fix the errors on your entries. ")
            return render(request, 'member-form.html', {'form': form, 'title' : "Submit a claim"})
    else:
        form = ClaimForm(instance=Claim.objects.get(id=claim_id), qset=Beneficiary.objects.filter(member = request.user.member, deceased = False))
        return render(request, 'member-form.html', {'form': form, 'title' : "Submit a claim"})


@login_required
def member_payment_history(request):
    if not hasattr(request.user, 'member'):
        return HttpResponse('Unauthorized', status=401)
    return render(request, "member_finance_table.html", {"history" : PaymentHistory.objects.filter(member__user = request.user).order_by("-payment_date"), "title" : "Payment History"})


@login_required
def claims_list(request):
    if not hasattr(request.user, 'member'):
        return HttpResponse('Unauthorized', status=401)
    return render(request, "member_claims_table.html", {"claims" : Claim.objects.filter(member__user = request.user).order_by("-date_filed"), "title" : "Claims"})


@login_required
def claiminfo(request, claim_id):
    if not hasattr(request.user, 'trustee'):
        return HttpResponse('Unauthorized', status=401)
    claim = get_object_or_404(Claim, id=claim_id)
    claim_amount = 0
    mysettings = Setting.objects.first()
    thebeneficiary = claim.beneficiary
    if thebeneficiary.relationship_type == "spouse":
        claim_amount = mysettings.spouse_claim_amount
    elif thebeneficiary.relationship_type == "child":
        claim_amount = mysettings.child_claim_amount
    elif thebeneficiary.relationship_type == "parent":
        claim_amount = mysettings.parent_claim_amount
    elif thebeneficiary.relationship_type == "principal":
        claim_amount = mysettings.principal_claim_amount
    elif thebeneficiary.relationship_type == "nominee":
        claim_amount = mysettings.nominee_claim_amount
    else:
        claim_amount = 0
    return render(request, 'claim_detail.html', {'claim': claim, "title" : "Claims", "amount" : claim_amount})

@login_required
def trustee_claim_list(request):
    if not hasattr(request.user, 'trustee'):
        return HttpResponse('Unauthorized', status=401)
    return render(request, "trustee_claims_table.html", {"claims" : Claim.objects.all().order_by("-date_filed"), "title" : "Claims"})

@login_required
def approve_claim(request, claim_id):
    if not hasattr(request.user, 'trustee'):
        return HttpResponse('Unauthorized', status=401)
    
    if request.method == "POST":
        claim = get_object_or_404(Claim, id=claim_id)

        if claim.member.user == request.user:
            messages.error(request, "You can't approve your own claim!")
            return redirect('main:claim_info', claim_id)

        #if not request.POST["amount"]:
        #    messages.error(request, "No claimed amount entered 🤷...")
        #    return redirect('main:claim_info', claim_id)
        claim_amount = 0
        mysettings = Setting.objects.first()
        thebeneficiary = claim.beneficiary
        if thebeneficiary.relationship_type == "spouse":
            claim_amount = mysettings.spouse_claim_amount
        elif thebeneficiary.relationship_type == "child":
            claim_amount = mysettings.child_claim_amount
        elif thebeneficiary.relationship_type == "parent":
            claim_amount = mysettings.parent_claim_amount
        elif thebeneficiary.relationship_type == "principal":
            claim_amount = mysettings.principal_claim_amount
        elif thebeneficiary.relationship_type == "nominee":
            claim_amount = mysettings.nominee_claim_amount
        else:
            claim_amount = 0

        claim.status = 'approved'
        claim.amount_claimed = claim_amount
        claim.approved_by = Trustee.objects.get(user = request.user)
        claim.approval_date = datetime.now()

        Beneficiary.objects.filter(pk=claim.beneficiary.pk).update(deceased = True)
        claim.save()
        messages.success(request, 'Claim successfully approved!')
        return redirect('main:claim_info', claim_id)


@login_required
def reject_claim(request, claim_id):
    if not hasattr(request.user, 'trustee'):
        return HttpResponse('Unauthorized', status=401)
    claim = get_object_or_404(Claim, id=claim_id)

    if claim.member.user == request.user:
            messages.error(request, "You can't reject your own claim!")
            return redirect('main:claim_info', claim_id)

    claim.status = 'rejected'
    claim.save()
    messages.success(request, 'Claim successfully rejected!')
    return redirect('main:trustee_dashboard')


@login_required
def trustee_settings(request):
    if not hasattr(request.user, 'trustee'):
        return HttpResponse('Unauthorized', status=401)
    if request.method == "POST":
        form = SettingsForm(request.POST, instance=Setting.objects.all().first())
        if form.is_valid():
            form.save()
            EventLog.objects.create(event = f'Updated Settings', event_type = "update", trustee = Trustee.objects.get(user = request.user))
            messages.success(request, "The Settings were updated successfully...")
            return render(request, 'trustee-form.html', {'form': form, 'title' : "Settings", 'subtitle' : ""})
        else:
            messages.error(request, "You submitted invalid information, please check for errors. ")
            return render(request, 'trustee-form.html', {'form': form, 'title' : "Settings", 'subtitle' : ""})
    else:
        form = SettingsForm(instance=Setting.objects.all().first())
        return render(request, 'trustee-form.html', {'form': form, 'title' : "Settings", 'subtitle' : ""})
    
    

@login_required
def update_payment_status(request, member_id): # Not really being used anymore!
    if not hasattr(request.user, 'trustee'):
        return HttpResponse('Unauthorized', status=401)
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        #member.payment_status = not member.payment_status  # Toggle payment status
        #member.save()
        messages.success(request, 'Payment status updated')
        return redirect('main:trustee_dashboard')
    return render(request, 'update_payment_status.html', {'member': member})


@login_required
def add_payment(request, member_id):
    the_member = Member.objects.get(id = member_id)
    if the_member.user != request.user:
        nextp = datetime(datetime.now().year, datetime.now().month, 1)

        if PaymentHistory.objects.filter(member = the_member).order_by("-period").count() >= 1:
            prev = PaymentHistory.objects.filter(member = the_member).order_by("-period")[0]
            nextp = datetime(prev.period.year, prev.period.month, 1) + timedelta(35)
            nextp = datetime(nextp.year, nextp.month, 1)
    
        PaymentHistory.objects.create(
            member = the_member,
            period = nextp,
            recorded_by = Trustee.objects.get(user = request.user),
            amount_paid = Setting.objects.first().monthly_contribution
        )
        messages.success(request, f'The payment update for {nextp.strftime("%b")} {nextp.year} was saved successfully!')
        return redirect("main:member_info", member_id)
    else:
        messages.error(request, "You cannot update your own financial member details!")
        return redirect("main:member_list")



@login_required
def beneficiary_list(request):
    if not hasattr(request.user, 'member'):
        return HttpResponse('Unauthorized', status=401)
    return render(request, "member_beneficiary_table.html", {"beneficiaries" : Beneficiary.objects.filter(member__user = request.user), 'title' : "Beneficiaries List"})


@login_required
def add_beneficiary(request):
    if not hasattr(request.user, 'member'):
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST, request.FILES)
        if form.is_valid():
            beneficiary = form.save(commit=False)
            beneficiary.member = request.user.member
            ## Validation check algorithm
            if not beneficiary.relationship_type == "child":
                if beneficiary.relationship_type == "parent" and Beneficiary.objects.filter(relationship_type = "parent", member=request.user.member).count() == 2:
                    messages.error(request, "You already have 2 Parents, can't add another! ")
                    return render(request, 'member-form.html', {'form': form, 'title' : "Add a Beneficiary"})
                elif beneficiary.relationship_type == "nominee" and Beneficiary.objects.filter(relationship_type = "nominee", member=request.user.member).count() == 2:
                    messages.error(request, "You already have 2 Nominees, can't add another! ")
                    return render(request, 'member-form.html', {'form': form, 'title' : "Add a Beneficiary"})
                elif beneficiary.relationship_type == "spouse" and Beneficiary.objects.filter(relationship_type = "spouse", member = request.user.member).count() == 1:
                    messages.error(request, "You already have 1 Spouse, can't add another! ")
                    return render(request, 'member-form.html', {'form': form, 'title' : "Add a Beneficiary"})
            
            beneficiary.save()
            
            messages.success(request, 'Beneficiary added successfully')
            return redirect('main:beneficiary_list')
        else:
            messages.error(request, 'Beneficiary could not be added, an error occured. Check your entries!')
            return render(request, 'member-form.html', {'form': form, 'title' : "Add a Beneficiary"})
    else:
        form = BeneficiaryForm()
    return render(request, 'member-form.html', {'form': form, 'title' : "Add a Beneficiary"})


@login_required
def update_beneficiary(request, beneficiary_id):
    if not hasattr(request.user, 'member'):
        return HttpResponse('Unauthorized', status=401)
    
    beneficiary = get_object_or_404(Beneficiary, id=beneficiary_id)
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST, request.FILES, instance=beneficiary)
        if form.is_valid():
            beneficiary = form.save(commit=False)

            if not beneficiary.relationship_type == "child":
                if beneficiary.relationship_type == "parent" and Beneficiary.objects.filter(relationship_type = "parent", member=request.user.member).count() == 2:
                    messages.error(request, "You already have 2 Parents, can't add another! ")
                    return render(request, 'member-form.html', {'form': form, 'title' : "Add a Beneficiary"})
                elif beneficiary.relationship_type == "nominee" and Beneficiary.objects.filter(relationship_type = "nominee", member=request.user.member).count() == 2:
                    messages.error(request, "You already have 2 Nominees, can't add another! ")
                    return render(request, 'member-form.html', {'form': form, 'title' : "Add a Beneficiary"})
                elif beneficiary.relationship_type == "spouse" and Beneficiary.objects.filter(relationship_type = "spouse", member = request.user.member).count() == 1:
                    messages.error(request, "You already have 1 Spouse, can't add another! ")
                    return render(request, 'member-form.html', {'form': form, 'title' : "Add a Beneficiary"})
            beneficiary.save()
            messages.success(request, 'Beneficiary updated successfully')
            return redirect('main:beneficiary_list')
        else:
            messages.error(request, 'Beneficiary could not be updated. Please fix the errors on your entries.')
            return render(request, 'member-form.html', {'form': form, 'title' : "Update Beneficiary"})
    else:
        form = BeneficiaryForm(instance=beneficiary)
        return render(request, 'member-form.html', {'form': form, 'title' : "Update Beneficiary"})


@login_required
def delete_beneficiary(request, beneficiary_id):
    if not hasattr(request.user, 'member'):
        return HttpResponse('Unauthorized', status=401)
    
    if not Beneficiary.objects.filter(id = beneficiary_id).exists():
        messages.error(request, "Beneficiary does not exist")
        return redirect("main:beneficiary_list")
    
    beneficiary = get_object_or_404(Beneficiary, id=beneficiary_id)
    beneficiary.delete()
    messages.success(request, 'Beneficiary removed')
    return redirect('main:beneficiary_list')


