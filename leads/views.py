from django.shortcuts import render, redirect

from .models import Lead

from .forms import LeadModelForm



def landing_page(request):
    return render(request, 'landing.html')

def lead_list(request):
    leads = Lead.objects.all()
    context = {
        'leads':leads
    }
    return render(request, 'lead_list.html', context)


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead":lead
    }

    return render(request, "lead_details.html", context)

def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        "form":form
    }
    return render(request, "lead_create.html", context)

def lead_list(request):
    leads = Lead.objects.all()
    context = {
        'leads':leads
    }
    return render(request, 'lead_list.html', context)

def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form .is_valid():
            form.save()
            return redirect('/leads')
    context = {
        "form":form,
        'lead':lead,
    }
    return render(request, "lead_update.html", context)

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')
