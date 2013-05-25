# Index has a very special view that lives out here
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist, loader, Context

import datetime

# Handle the static pages
def index(request):
        return render_to_response('index.html', {
        })

def privacypolicy(request):
        return render_to_response('about/privacypolicy.html', {
        })

def website(request):
        return render_to_response('about/website.html', {
        })


