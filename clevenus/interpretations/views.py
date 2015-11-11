from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy

from django.views.generic import TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import GenericInterpretation
from .forms import InterpretationForm

class InterpretationList(ListView):
    model = GenericInterpretation

class InterpretationCreate(CreateView):
    model = GenericInterpretation
    form_class = InterpretationForm
    success_url = reverse_lazy('interpretation_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(InterpretationCreate, self).form_valid(form)


class InterpretationUpdate(UpdateView):
    model = GenericInterpretation
    form_class = InterpretationForm
    success_url = reverse_lazy('interpretation_list')


class InterpretationDelete(DeleteView):
    model = GenericInterpretation
    form_class = InterpretationForm
    success_url = reverse_lazy('interpretation_list')