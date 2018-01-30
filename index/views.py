from django.views.generic import TemplateView
from django.utils import timezone
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings

class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'index/index.html'

    def get(self, request, *args, **kwargs):
        
       
        return super(IndexView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            # 'html': " ".join(self.html),
            # 'key': settings.HTML_HREF_REPLACE_KEY,
            # 'tag': self.group_tag
        }

        kwargs.update(context)
        return super(IndexView, self).get_context_data(**kwargs)