from django.shortcuts import render, redirect
from django.urls import reverse
import random
from django.core.mail import send_mail

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import PeriwinkleRequiredMixin


class AgentListView(PeriwinkleRequiredMixin, ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

class AgentCreateView(PeriwinkleRequiredMixin, CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent_list")

    # def form_valid(self, form):
    #     agent = form.save(commit=False)
    #     agent.organisation = self.request.user.userprofile
    #     agent.save()
    #     return super(AgentCreateView, self).form_valid(form)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"periwinkle{random.randint(0, 100000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )
        send_mail(
            subject="You are invited to be an agent",
            message="You were added as an agent. Please login and make sure to set a password.",
            from_email="admin@test.com",
            recipient_list=[user.email]
        )

        return super(AgentCreateView, self).form_valid(form)

class AgentDetailView(PeriwinkleRequiredMixin, DetailView):
    template_name = "agents/agent_detail.html"
    # context_object_name = "agents"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

# class AgentUpdateView(LoginRequiredMixin,UpdateView):
#     template_name = "agents/agent_update.html"
#     form_class = AgentModelForm
#     print(form_class)
   
    
        
#     def get_queryset(self):
#         return Agent.objects.all()


#     def get_success_url(self):
#         return reverse("agents:agent_list")

class AgentUpdateView(LoginRequiredMixin,UpdateView):
    template_name = "agents/agent_update.html"
    form_class = AgentModelForm

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


    def get_success_url(self, pk=None):
        # Use the current agent's pk if none is provided
        if pk is None:
            pk = self.object.pk

        # Return the URL with the pk as a parameter
        return reverse("agents:agent_detail", kwargs={'pk': pk})



class AgentDeleteView(PeriwinkleRequiredMixin,DeleteView):
    template_name = "agents/agent_delete.html" 

    def get_success_url(self):
        return reverse("agents:agent_list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)





    

