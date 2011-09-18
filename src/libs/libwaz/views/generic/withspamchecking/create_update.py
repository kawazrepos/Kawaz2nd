# -*- coding: utf-8 -*-
#    
#    
#    created by giginet on 2011/07/20
#
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.xheaders import populate_xheaders
from django.utils.translation import ugettext
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.views.generic.create_update import apply_extra_context, get_model_and_form_class, redirect, lookup_object

from libwaz.forms import ModelFormWithRequest
from libwaz.db.models import ModelWithRequest
from libwaz.utils.akismet import is_spam as _is_spam

#
#    外部ユーザーが書き込めるオブジェクトを生成させるとき、この汎用ビューを使ってください
#    英訳は誰かしてね！
#
def create_object(request, spam_check_scope_attr, author_name_attr, model=None, template_name=None,
        template_loader=loader, extra_context=None, post_save_redirect=None,
        login_required=False, context_processors=None, form_class=None, initial=None, initial_with_get=False):
    """
    Generic object-creation function.

    Templates: ``<app_label>/<model_name>_form.html``
    Context:
        form
            the form for the object
    """
    if not initial and initial_with_get:
        initial = request.GET.items()
    elif initial_with_get:
        initial.update(request.GET.items())
    if extra_context is None: extra_context = {}
    if login_required and not request.user.is_authenticated():
        return redirect_to_login(request.path)
    model, form_class = get_model_and_form_class(model, form_class)
    if request.method == 'POST':
        if issubclass(form_class, ModelFormWithRequest):
            form = form_class(request, request.POST, request.FILES)
        else:
            form = form_class(request.POST, request.FILES)
        if form.is_valid():
            # checking spam
            new_object = form.save(commit=False)
            body = getattr(new_object, spam_check_scope_attr, None)
            author = getattr(new_object, author_name_attr, None)
            if _is_spam(model, new_object, body, author, request):
                msg = ugettext("The %(verbose_name)s was created unsuccessfully.") %\
                                    {"verbose_name": model._meta.verbose_name}
                messages.error(request, msg, fail_silently=True)
            else:
                new_object = form.save(commit=True)
                msg = ugettext("The %(verbose_name)s was created successfully.") %\
                                    {"verbose_name": model._meta.verbose_name}
                messages.success(request, msg, fail_silently=True)
                return redirect(post_save_redirect, new_object)
    else:
        if issubclass(form_class, ModelFormWithRequest):
            form = form_class(request, initial=initial)
        else:
            form = form_class(initial=initial)
    # Create the template, context, response
    if not template_name:
        template_name = "%s/%s_form.html" % (model._meta.app_label, model._meta.object_name.lower())
    t = template_loader.get_template(template_name)
    c = RequestContext(request, {
        'form': form,
    }, context_processors)
    apply_extra_context(extra_context, c)
    return HttpResponse(t.render(c))