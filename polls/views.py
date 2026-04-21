from django.shortcuts import render
from .forms import DonorRegistration, Contact, Search
from .models import donor_Registration, sea_rch, con_tact
from django.core.mail import send_mail
from django.conf import settings

from .models import donor_Registration


def home(request):
    donors_count = donor_Registration.objects.count()
    blood_units = donors_count * 2
    lives_saved = donors_count * 3

    return render(request, 'polls/base.html', {
        'donors_count': donors_count,
        'blood_units': blood_units,
        'lives_saved': lives_saved
    })


def home(request):
    return render(request, 'polls/base.html')


def about(request):
    return render(request, 'polls/about.html')

def donor_registration(request):
    forms = DonorRegistration()

    # ✅ Blood groups list add ki
    blood_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

    if request.method == 'POST':
        forms = DonorRegistration(request.POST)

        if forms.is_valid():
            forms.save()

            return render(request, 'polls/donor_list.html', {
                'forms': forms,
                'blood_groups': blood_groups   # (optional but safe)
            })

        print(forms.errors)

    context_form = {
        'forms': forms,
        'blood_groups': blood_groups   # ✅ template ko bheja
    }

    return render(request, 'polls/donor_registration.html', context_form)

def search(request):
    forms = Search()
    if request.method == 'POST':
        forms = Search(request.POST)
        if forms.is_valid():
            forms.save()
            bloodgroup = forms.cleaned_data['blood_group']
            state = forms.cleaned_data['state']
            city = forms.cleaned_data['city']
            donor_filter = donor_Registration.objects.filter(
                blood_group__iexact=bloodgroup,
                state__iexact=state,
                city__iexact=city
            )
            context = {
                'donor_filter': donor_filter
            }

            return render(request, 'polls/search_list.html', context)

        print(forms.errors)

    context_form = {
        'forms': forms
    }

    return render(request, 'polls/search.html', context_form)


def search_info(request, email):
    detail = donor_Registration.objects.get(email=email)

    context = {
        'details': detail
    }

    return render(request, 'polls/search_info.html', context)


# 🔥🔥🔥 UPDATED CONTACT FUNCTION
def contact(request):
    forms = Contact()

    if request.method == 'POST':
        forms = Contact(request.POST)
        if forms.is_valid():
            data = forms.save()   # DB me save

            # 🔥 Data nikaalo
            name = data.name
            phone = data.phone_number
            email = data.email
            subject = data.subject

            # 🔥 Email message
            message = f"""
            New Contact Message:

            Name: {name}
            Phone: {phone}
            Email: {email}

            Message:
            {subject}
            """

            # 🔥 Email send
            send_mail(
                subject="New Contact Form Message",
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['thakoranant39@gmail.com'],  # 👈 apna email daalo
                fail_silently=False,
            )

            return render(request, 'polls/contact.html', {
                'forms': Contact(),
                'success': True
            })

    context = {
        'forms': forms
    }

    return render(request, 'polls/contact.html', context)
