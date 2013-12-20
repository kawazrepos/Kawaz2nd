# -*- coding:utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User

from libwaz.http import Http403, JsonResponse
from libwaz.views.generic import list_detail
from libwaz.views.generic import create_update
from libwaz.contrib.object_permission.decorators import permission_required
from django.core.servers.basehttp import FileWrapper

from utils import watermark
from models import Material
from forms import MaterialForm, AttachementMaterialForm
from filtersets import MaterialFilterSet
from ..projects.models import Project

import os
import urllib
try:
    from PIL import Image
except ImportError:
    import Image
class StreamingHttpResponse(HttpResponse):

    """This class exists to bypass middleware that uses .content.

    See Django bug #6027: http://code.djangoproject.com/ticket/6027

    We override content to be a no-op, so that GzipMiddleware doesn't exhaust
    the FileWrapper generator, which reads the file incrementally.
    """

    def _get_content(self):
        return ""

    def _set_content(self, value):
        pass

    content = property(_get_content, _set_content)

def _thumbnail_image_response(material, width, height):
    img = Image.open(material.file)
    if img.size[0] > width or img.size[1] > height:
        img.thumbnail((width, height), Image.ANTIALIAS)
    response = HttpResponse(mimetype='image/png')
    img.save(response, "PNG")
    return response
def _thumbnail_movie_response(material, width, height, _watermark=False):
    filename = u'thumbnails/%(filename)s.%(width)sx%(height)s.jpg' % {
        'filename': material.filename(),
        'width': width,
        'height': height,
    }
    WATERMARK_FILE = os.path.join(settings.MEDIA_ROOT, 'image/commons/movie.jpg')
    filename= os.path.join(settings.MEDIA_ROOT, filename)
    if not os.path.exists(filename):
        # ffmpegは日本語ファイル名を処理できないため一時ファイルを作成
        import tempfile
        import commands
        source = os.path.join(settings.MEDIA_ROOT, material.file.name)
        ext = os.path.splitext(source)[1]
        f = open(source, 'rb')
        #tmp = tempfile.NamedTemporaryFile('wb', bufsize=f.size(), suffix=ext, delete=False)
        tmp = tempfile.NamedTemporaryFile(suffix=ext, delete=False)
        # tmp2は存在しているとエラーチェックに使えないのであえて`delete=False`を指定せずすぐに閉じている
        tmp2 = tempfile.NamedTemporaryFile()
        tmp2.close()
        tmp.write(f.read())
        tmp.close()
        format = u'ffmpeg -ss %(sec)s -vframes 1 -i "%(movie)s" -s %(width)sx%(height)s -f image2 "%(output)s"'
        kwargs = {
            'movie': tmp.name,
            'width': width,
            'height': height,
            'output': tmp2.name,
        }
        FIRST_POS = 30
        for i in xrange(0, FIRST_POS, 10):
            kwargs['sec'] = FIRST_POS - i
            commands.getstatusoutput(format % kwargs)[0]
            # ffmpegは正しいstatusを返さないようなのでファイルの存在で
            # 処理の実行ができたかを確認する
            if os.path.exists(tmp2.name): break
        if os.path.exists(tmp2.name):
            # 作成したサムネイルを移動
            import shutil
            shutil.move(tmp2.name, filename)
        else:
            # 動画の切り取りに失敗したので画像ファイルを通常の画像ファイルを使用する
            filename = WATERMARK_FILE
            _watermark = False
        os.unlink(tmp.name)
    img = Image.open(filename)
    if img.size[0] > width or img.size[1] > height:
        img.thumbnail((width, height), Image.ANTIALIAS)
    if _watermark:
        mark = Image.open(WATERMARK_FILE)
        img = watermark.watermark(img, mark, 'tile', 0.1)
    response = HttpResponse(mimetype='image/jpeg')
    img.save(response, "jpeg")
    return response

def _watermark_image_response(material, width=None, height=None):
    WATERMARK = os.path.join(settings.MEDIA_ROOT, 'image/watermark.png')
    img = Image.open(material.file)
    if not width:
        width = img.size[0]
    if not height:
        height = img.size[1]
    if img.size[0] > width or img.size[1] > height:
        img.thumbnail((width, height), Image.ANTIALIAS)
    mark = Image.open(WATERMARK)
    img = watermark.watermark(img, mark, 'tile', 0.3)
    response = HttpResponse(mimetype='image/png')
    img.save(response, "PNG")
    return response
#
#
# list_detail
#----------------------------------------------------------------------------------------
def material_filter(request, author=None, project=None):
    if author:
        author = get_object_or_404(User, username=author)
        qs = Material.objects.published(request).filter(author=author)
    else:
        qs = Material.objects.commons(request)
    if project:
        project = get_object_or_404(Project, slug=project)
        qs = qs.filter(project=project)
    kwargs = {
        'queryset': qs,
        'filter_class': MaterialFilterSet,
        'extra_context': {
            'author': author,
            'project': project,
        }
    }
    return list_detail.object_filter(request, **kwargs)

@permission_required('commons.view_material', Material)
def material_detail(request, object_id):
    kwargs = {
        'queryset': Material.objects.published(request),
    }
    return list_detail.object_detail(request, object_id=object_id, **kwargs)

@permission_required('commons.view_material', Material)
@never_cache
def material_download(request, *args, **kwargs):
    # Notice:
    #  Djangoの機能としてのキャッシュおよびブラウザでのキャッシュを制限している
    #  これを行わないと正しいダウンロード数の記録やファイル編集時に正しいファイルを
    #  返すなどの処理ができなくなる。またファイルを添付と指定することで再生可能ファイル
    #  などでも強制的にダウンロードするように指定している
    #
    # Notice:
    #   ref http://djangosnippets.org/snippets/1710/
    #
    obj = get_object_or_404(Material, pk=kwargs['object_id'])
    # ライセンスでダウンロード可能かチェック
    if obj.license == 'reject' and not request.user.is_superuser: raise Http403
    # Downloadカウンターを更新
    obj.pv += 1
    obj.save(request=request, action='download')
    # Response作成
    mimetype = obj.mimetype() if obj.mimetype() else 'application/octet-stream'
    response = HttpResponse(obj.file)
    response['Cache-Control'] = 'no-cache'
    response['Content-Type'] = mimetype
    if obj.encoding():
        response['Content-Encoding'] = obj.encoding()
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    if u'webkit' in user_agent:
        response['Content-Disposition'] = (u"attachment; filename=%s" % obj.filename()).encode('utf-8')
    elif u'msie' in user_agent:
        filename = urllib.quote(obj.filename().encode('utf-8'))
        response['Content-Disposition'] = u"attachment; filename=%s" % filename
    else:
        filename = urllib.quote(obj.filename().encode('utf-8'))
        response['Content-Disposition'] = u"attachment; filename*=UTF-8''%s" % filename
    return response

@permission_required('commons.view_material', Material)
@never_cache
def material_preview(request, *args, **kwargs):
    obj = get_object_or_404(Material, pk=kwargs['object_id'])
    mimetype = obj.mimetype()
    filetype = obj.filetype()
    if 'image' == filetype:
        WIDTH = 960
        HEIGHT = 620
        return _watermark_image_response(obj, width=WIDTH, height=HEIGHT)
    response = StreamingHttpResponse(obj.file)
    response['Content-Type'] = mimetype
    response['Content-Length'] = obj.file.size
    return response

@permission_required('commons.view_material', Material)
def material_thumbnail(request, *args, **kwargs):
    obj = get_object_or_404(Material, pk=kwargs['object_id'])
    mimetype = obj.mimetype()
    filetype = obj.filetype()
    width = int(request.GET.get('width', 320))
    height = int(request.GET.get('height', 240))
    if "image" == filetype:
        return _thumbnail_image_response(obj, width, height)
    elif 'movie' == filetype:
        return _thumbnail_movie_response(obj, width, height)
    else:
        # 他のファイル形式に関してはサムネイルに対応していない
        # PDFとかは可能かなぁ・・・微妙だよねぇ
        response = HttpResponse(obj.file, mimetype=mimetype)
        return response

@permission_required('commons.view_material', Material)
def material_digest(request, *args, **kwargs):
    obj = get_object_or_404(Material, pk=kwargs['object_id'])
    filetype = obj.filetype()
    if filetype == 'image':
        return _thumbnail_image_response(obj, 144, 144)
    elif filetype == 'movie':
        return _thumbnail_movie_response(obj, 144, 144, True)
    elif filetype in ('audio', 'archive', 'text', 'application'):
        filename = os.path.join(settings.MEDIA_ROOT, r'image/commons/%s.jpg' % filetype)
    else:
        filename = os.path.join(settings.MEDIA_ROOT, r'image/commons/unknown.jpg')
    img = Image.open(filename)
    response = HttpResponse(mimetype='image/png')
    img.save(response, 'PNG')
    return response
#
# create_update
#-----------------------------------------------------------------------------------------
@permission_required('commons.add_material')
def create_material(request, project=None):
    if project:
        project = get_object_or_404(Project, slug=project)
        if not request.user.has_perm('projects.add_material_project', project):
            raise Http403
    kwargs = {
        'form_class': MaterialForm,
        'extra_context': {
            'project': project
        }
    }
    if project:
        kwargs['initial'] = {'project': project.pk}
    return create_update.create_object(request, **kwargs)

@permission_required('commons.change_material', Material)
def update_material(request, object_id):
    kwargs = {
        'form_class': MaterialForm,
    }
    return create_update.update_object(request, object_id=object_id, **kwargs)

@permission_required('commons.delete_material', Material)
def delete_material(request, object_id):
    kwargs = {
        'model': Material,
        'post_delete_redirect': reverse('commons-material-list'),
    }
    return create_update.delete_object(request, object_id=object_id, **kwargs)

#
# API
#-------------------------------------------------------------------------
#
# Notice:
#    通常AJAXによるアクセスの場合CSRFは気にする必要はない（Ajaxによる
#    アクセスの場合は自動的にCSRFがオフになるため）が
#    ファイルのアップロードをAJAX(XMLHttpRequest)で行うことはできない
#    したがってAjaxで擬似的にファイルアップロードを行うためのビューでは
#    CSRFを切ってやる必要がある。
#
@require_POST
@csrf_exempt
@permission_required('commons.add_material')
def attache_material(request):
    form = AttachementMaterialForm(request, request.POST, request.FILES)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.pub_state = 'public'
        instance.license = 'reject'
        instance.save(request=request, action='attache')
        # JSON形式で通知
        value = {
            'status': 'ok',
            'instance': {
                'tag':   u"{commons: %d}" % instance.pk,
                'url': instance.get_absolute_url(),
                'filename': instance.filename(),
            },
        }
        return JsonResponse(value)
    else:
        from django.template.defaultfilters import striptags
        errors = [unicode(striptags("%s: %s"%(k, v))) for k, v in form.errors.iteritems()]
        return JsonResponse({'status': "failed", 'errors': errors})
