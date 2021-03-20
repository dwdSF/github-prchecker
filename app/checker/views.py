from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views import View

from .forms import CheckForm
from .models import Check
from .utils import collect_user_info


class InfoView(View):
    ''' The class implements post request processing using AJAX.
        Calls the information collection function. '''

    def get(self, request, *args, **kwargs):
        return render(request, "info.html", {})

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            form = CheckForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                collect_user_info(username)  # Celery + Redis/RabbitMQ
                return JsonResponse({'message': 'success'})

            return JsonResponse({'message': 'Field couldn\'t validate'})

        return JsonResponse({'message': 'Wrong request'})


class InfoDataView(View):
    ''' Uploading the received information to the page '''

    def get(self, request, *args, **kwargs):
        username = request.GET['username']
        template = loader.get_template("data.html")

        user_prs = Check.objects.filter(username=username)
        context = {
            "user_prs": user_prs
        }
        return HttpResponse(template.render(context, self.request))
