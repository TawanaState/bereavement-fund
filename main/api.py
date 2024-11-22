from django.http import JsonResponse, HttpResponse
from .models import Member, Trustee, Beneficiary, Claim, PaymentHistory, EventLog, CustomUser
from datetime import datetime, date
import csv


def dump_to_csv(model, qs):
    """
    Takes in a Django queryset and spits out a CSV file.
    """

    model = qs.model
    writer = ''

    headers = []

    # Get standard fields
    for field in model._meta.get_fields():
        headers.append(field) if 'extra' not in field.name else None

    writer += ','.join([field.name for field in headers])
    writer += '\n'

    for obj in qs:
        row = []
        for field in headers:
            # Append all general fields
            if field.get_internal_type() not in ['ForeignKey', 'ManyToManyField', 'OneToOneField']:
                val = getattr(obj, field.name)
                if callable(val):
                    val = val()
                if type(val) == str:
                    val = val.encode("utf-8")
                row.append(str(val))

            # Append all fk fields
            elif field.get_internal_type() in ['ForeignKey', 'OneToOneField']:
                from django.core import serializers
                import json

                value = field.value_from_object(obj)

                if value not in [None, ""]:
                    qs = field.remote_field.model.objects.filter(pk=value)
                    json_data = serializers.serialize("json", qs, fields=(field.name for field
                                                                          in qs.first()._meta.get_fields() if
                                                                          'extra' not in field.name))
                    json_data = [o['fields'] for o in json.loads(json_data)]
                    json_data = json.dumps(json_data)
                    json_data = json_data.replace(",", ";")
                    json_data = json_data.replace("\"", "'")
                    row.append(json_data)
                else:
                    row.append("[]")

            # Append all m2m fields
            elif field.get_internal_type() in ['ManyToManyField']:
                from django.core import serializers
                import json

                qs = getattr(obj, field.name).all()
                json_data = serializers.serialize("json", qs)
                json_data = [o['fields'] for o in json.loads(json_data)]
                json_data = json.dumps(json_data)
                json_data = json_data.replace(",", ";")
                json_data = json_data.replace("\"", "'")
                row.append(json_data)

        writer += ','.join(row)
        writer += '\n'

    return writer


def DateToPeriod(val):
    return f"{val.month}/{val.year}"

def DateToRealDate(val):
    return f"{val.day}/{val.month}/{val.year}"

def ToDate(val):
    return datetime.strptime(val, "%d/%m/%Y").date()

def NoneToZero(val):
    if val == None:
        return 0
    else:
        return val


def ClaimsTrends():
    """
    returns
    [{
        date-filed : date
        amount : float
        status : 'pending', 'approved', 'rejected'
    }]
    """
    rtnlist = []
    for x in Claim.objects.all():
        rtnlist.append(
            {
                "date_filed" : DateToRealDate(x.date_filed),
                "amount" : NoneToZero(x.amount_claimed),
                "status" : x.status
            }
        )
    return rtnlist


def member_trends():
    """
    [
    {
        age : number,
        gender : 'male', 'female'
        membership_length : number
    }
    ]
    """
    rtnlist = []
    for x in Member.objects.all():
        rtnlist.append({
            "age" : abs(date.today().year - x.date_of_birth.year),
            "gender": x.gender.lower(),
            "membership_length" : x.membership_length()
        })
    return rtnlist


def paymentHistoryTrends():
    """
    [
    {
        period : date,
        amount : number
    }
    ]
    """
    rtnlist = []


    for x in PaymentHistory.objects.all():
        rtnlist.append({
            "period" : DateToRealDate(x.period),
            "amount" : x.amount_paid
        })
    return rtnlist


def ContributionsVsClaims():
    """
    [
    {
        period : date,
        contributions : float,
        claims : float,
    }
    ]
    """
    contributions_hashmap = {}# {"12/2024" : 200}
    claims_hashmap = {}# {"13/2024" : 200}
    rtnlist = []

    for x in paymentHistoryTrends():
        y = DateToPeriod(ToDate(x["period"]))
        contributions_hashmap[y] = contributions_hashmap.get(y, 0) + x["amount"]
    

    #print(ClaimsTrends())

    for x in ClaimsTrends():
        y = DateToPeriod(ToDate(x["date_filed"]))
        claims_hashmap[y] = claims_hashmap.get(y, 0) + NoneToZero(x.get("amount", 0))
    
    allperiods = set(list(claims_hashmap.keys()) + list(contributions_hashmap.keys()))
    allsortedperiods = sorted([ToDate("01/" + x) for x in allperiods])
    for x in allsortedperiods:
        rtnlist.append({
            "period" : DateToPeriod(x),
            "contributions" : contributions_hashmap.get(DateToPeriod(x), 0),
            "claims" : claims_hashmap.get(DateToPeriod(x), 0)
        })
    return rtnlist
    
def trends_view(request):
    dataset = {
        "members" : member_trends(),
        "claims" : ClaimsTrends(),
        "contributions" : paymentHistoryTrends(),
        "contributionsVSclaims" : ContributionsVsClaims()
    }
    return JsonResponse(dataset)


def claims_export(request):
    output = []
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    query_set = Claim.objects.all()
    #Header
    writer.writerow(['Member Fullname', 'Beneficiary', 'Approved By', 'Date Filed', 'Amount Claimed', 'Status'])
    for myclaim in query_set:
        output.append([myclaim.member.user, myclaim.beneficiary.full_name, myclaim.approved_by, myclaim.date_filed, myclaim.amount_claimed, myclaim.status])
    #CSV Data
    writer.writerows(output)
    return response


def members_export(request):
    output = []
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    query_set = Member.objects.all()
    #Header
    writer.writerow(['Fullname', 'DOB', 'Gender', 'Phone Number', 'ID Number', 'Hit EC Number', 'Department'])
    for mymember in query_set:
        output.append([mymember.user, mymember.date_of_birth, mymember.gender, mymember.phone_number, mymember.id_number, mymember.hit_ec_number, mymember.department])
    #CSV Data
    writer.writerows(output)
    return response


def contributions_export(request):
    output = []
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    query_set = PaymentHistory.objects.all()
    #Header
    writer.writerow(['Fullname', 'Payment Date', 'Period', 'Amount Paid', 'Recorded By'])
    for mycontrib in query_set:
        output.append([mycontrib.member.user, mycontrib.payment_date, mycontrib.period, mycontrib.amount_paid, mycontrib.recorded_by.user])
    #CSV Data
    writer.writerows(output)
    return response


def beneficiaries_export(request):
    output = []
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    query_set = Beneficiary.objects.all()
    #Header
    writer.writerow(['Fullname', 'ID Number', 'Relationship Type'])
    for myben in query_set:
        output.append([myben.full_name, myben.id_number, myben.relationship_type])
    #CSV Data
    writer.writerows(output)
    return response