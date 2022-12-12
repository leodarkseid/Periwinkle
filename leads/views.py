from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from agents.mixins import PeriwinkleRequiredMixin

from .models import Lead, Category

from .forms import LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm


class SignupView( CreateView):
    template_name= "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

class LandingPageView(TemplateView):
    template_name="landing.html"

class LeadListView(LoginRequiredMixin,ListView):
    template_name="lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        
        #this is filtering leads based on what should be available for each user(whether it is an organisor or agent)
        if user.is_organisor:
            #the agent__isnull=False ensures that the leads are divided into two assigned and non-assigned
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation, agent__isnull=False)
            #this filters the info gotten from abobe and ensures the agent only sees what is assigned to him
            queryset = queryset.filter(agent__user=user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile, 
                agent__isnull=True
            )
            context.update({
                "unassigned_leads":queryset
            })
        return context


def landing_page(request):
    return render(request, 'landing.html')


class LeadDetailView(LoginRequiredMixin,DetailView):
    template_name = "lead_details.html" 
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        
        #this is filtering leads based on what should be available for each user(whether it is an organisor or agent)
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            #this filters the info gotten from abobe and ensures the agent only sees what is assigned to him
            queryset = queryset.filter(agent__user=user)
        return queryset
    

class LeadCreateView(LoginRequiredMixin,CreateView):
    template_name = "lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead_list")

    def form_valid(self, form):
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)
    


# class LeadUpdateView(LoginRequiredMixin,UpdateView):
#     template_name = "lead_update.html"
#     queryset = Lead.objects.all()
#     form_class = LeadModelForm

#     def get_success_url(self):
#         return reverse("leads:lead_list")

class LeadUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "lead_update.html"
    form_class = LeadModelForm

    #The logic behind this is to ensure that Agents can only update what they are assigned and Oragnisers can update everything
    def get_queryset(self):
        user = self.request.user
        
        #this is filtering leads based on what should be available for each user(whether it is an organisor or agent)
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            #this filters the info gotten from abobe and ensures the agent only sees what is assigned to him
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self, pk=None):
    # Use the current lead's pk if none is provided
        if pk is None:
            pk = self.object.pk

    # Return the URL with the pk as a parameter
        return reverse("leads:lead_detail", kwargs={'pk': pk})

class LeadDeleteView(PeriwinkleRequiredMixin,DeleteView):
    template_name = "lead_delete.html"
    queryset = Lead.objects.all()

    #This ensures only Organiser can delete any lead
    def get_queryset(self):
        user = self.request.user
        
        #this is filtering leads to ensure just the organisor can delete any lead
        queryset = Lead.objects.filter(organisation=user.userprofile)
        return queryset
    

    def get_success_url(self):
        return reverse("leads:lead_list")


class AssignAgentView(PeriwinkleRequiredMixin, FormView):
    template_name = "assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead_list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "category_list.html"
    context_object_name = "category_list"

    def get_queryset(self):
        user = self.request.user
        
        #this is filtering leads based on what should be available for each user(whether it is an organisor or agent)
        if user.is_organisor:
            #the agent__isnull=False ensures that the leads are divided into two assigned and non-assigned
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        #this is filtering leads based on what should be available for each user(whether it is an organisor or agent)
        if user.is_organisor:
            #the agent__isnull=False ensures that the leads are divided into two assigned and non-assigned
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)

        context.update({
            "unassigned_lead_count":queryset.filter(category__isnull=True).count()
        })
        return context

class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "category_detail.html"
    context_object_name = "category"

    # This is not necessary, I opt to call "Category.leads.all" in the template since that's all I need
    # def get_context_data(self, **kwargs):
    #     context = super(CategoryDetailView, self).get_context_data(**kwargs)
    #     leads = self.get_object().leads.all()
    #     context.update({
    #         "leads":leads
    #     })
    #     return context

    def get_queryset(self):
        user = self.request.user
        
        #this is filtering leads based on what should be available for each user(whether it is an organisor or agent)
        if user.is_organisor:
            #the agent__isnull=False ensures that the leads are divided into two assigned and non-assigned
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(organisation=user.agent.organisation)
        return queryset

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        #this is filtering leads based on what should be available for each user(whether it is an organisor or agent)
        if user.is_organisor:
            #the agent__isnull=False ensures that the leads are divided into two assigned and non-assigned
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset


    def get_success_url(self):
        return reverse("leads:lead_detail", kwargs={"pk":self.get_object().id})


    
