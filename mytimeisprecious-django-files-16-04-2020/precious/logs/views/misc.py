from django.core.urlresolvers import reverse
from django.conf import settings
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from logs.models import Download
import os

def terms(request):
    return render(
        request,
        'misc/terms.html',
    )

def privacy(request):
    return render(
        request,
        'misc/privacy.html',
    )

def download(request):
    """
    Create a download object and serve the .zip file
    :param request:
    :return:
    """
    Download.objects.create(ip = request.META['REMOTE_ADDR'])

    fsock = open(os.path.join(settings.DOWNLOAD_ROOT, 'app.zip'), 'r')
    response = HttpResponse(fsock)
    response['Content-Type'] = "application/zip"
    response['Content-Disposition'] = "attachment; filename=precious_app.zip"
    return response

def main(request):
    return render(
        request,
        'misc/main.html',
    )