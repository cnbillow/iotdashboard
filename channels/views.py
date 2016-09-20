# -*- coding: utf-8 -*-
"""
Channels page

https://iothook.com/
"""

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import user_passes_test

from iotdashboard.settings import LOGIN_URL
from devices.views import admin_group

from .forms import *

@csrf_exempt
def channel_add(request):
    """
    :param request:
    :return:
    """
    msg_ok = ""
    msg_err = ""

    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = request.user
            f.save()
            msg_ok = _(u'Kanal ekleme başarılı')
        else:
            msg_err = _(u'Dikkat! Lütfen hataları düzeltiniz!')

    form = ChannelForm()
    form.fields['device'].queryset = Device.objects.filter(owner=request.user)

    return render(request, "back/add.html", locals())

def channel_list(request):
    """
    :param request:
    :return:
    """
    list = Channel.objects.filter(owner=request.user).order_by('-pk')
    return render(request, "back/channel_list.html", locals())

def channel_edit(request, id):
    """
    :param request:
    :param id:
    :return:
    """
    val = get_object_or_404(Channel, id=id)

    form = ChannelForm(request.POST or None, instance=val)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            msg_ok = _(u'Kanal güncelleme başarılı')
            return HttpResponseRedirect(reverse('channel_list'))
        else:
            msg_err = _(u'Dikkat! Lütfen hataları düzeltiniz!')

    return render(request, "back/add.html", locals())

@user_passes_test(admin_group, login_url=LOGIN_URL)
def channel_delete(request, id=None):
    """
    :param request:
    :param id:
    :return:
    """
    val = get_object_or_404(Channel, id=id)
    val.delete()
    msg_ok = _(u'Kanal silindi')

    return HttpResponseRedirect(reverse('channel_list'), locals())

############################

def key_list(request):
    """
    :param request:
    :return:
    """
    list = Channel.objects.filter(owner=request.user, enable=True).order_by('-pk')
    return render(request, "back/key_list.html", locals())

def generate_key(request, id=None):
    """
    :param request:
    :param id:
    :return:
    """
    val = get_object_or_404(Channel, id=id)
    val.api_key = hashlib.sha256((str(val.owner.username) + str(random.random())).encode('utf-8')).hexdigest()[:7] + '-' + hashlib.sha1(str(val.pub_date).encode('utf-8')).hexdigest()[:7]
    val.save()
    list = Channel.objects.filter(owner=request.user, enable=True).order_by('-pk')
    msg_ok = _(u'Key üretildi')

    return render(request, "back/key_list.html", locals())
