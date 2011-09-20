# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/11/28
#
from django.conf import settings
from django.template.defaultfilters import striptags
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

import os.path

def _image_viewer(url, thumbnail_url, title, description, width, height):
    kwargs = {
        'src': url,
        'thumbnail_src': thumbnail_url,
        'title': title,
        'description': description,
        'width': width,
        'height': height,
    }
    html = u"""
        <a href="%(src)s" rel="lightbox" title="%(title)s">
            <img src="%(thumbnail_src)s?width=%(width)s&height=%(height)s" alt="%(title)s" />
        </a>"""
    return mark_safe(html%kwargs)
def _audio_player(src, mimetype, width, height):
    kwargs = {
        'src': src,
        'mimetype': mimetype,
        'width': width,
        'height': height,
    }
    html = u"""
        <div id="player">
            <audio controls>
                <source src="%(src)s" type="%(mimetype)s">
            </audio>
        </div>
        """
    return mark_safe(html%kwargs)
def _movie_player(src, mimetype, width, height):
    kwargs = {
        'src': src,
        'width': width,
        'height': height,
        'mimetype': mimetype,
    }
    html = u"""
    <video>
        <source src="%(src)s" width="%(width)s" height="%(height)s">
        <!-- Flash fallback for non-HTML5 browsers without JavaScript -->
        <object width="%(width)s" height="%(height)s"
        type="application/x-shockwave-flash" data="/javascript/mediaelement/flashmediaelement.swf">
            <param name="movie" value="/javascript/mediaelement/flashmediaelement.swf" />
            <param name="flashvars" value="controls=true&file=%(src)s" />
            <!-- Image as a last resort -->
            <p>No video playback capabilities</p>
        </object>
    </video>"""
    return mark_safe(html%kwargs)
def _syntax_viewer(src, file, mimetype, width, height):
    # http://alexgorbatchev.com/SyntaxHighlighter/manual/brushes/
    SYNTAXES = {
        '.c':    'c',
        '.cs':   'csharp',
        '.cpp':  'cpp',
        '.css':  'css',
        '.js':   'javascript',
        '.java': 'java',
        '.pl':   'perl',
        '.php':  'php',
        '.py':   'python',
        '.rb':   'ruby',
        '.sql':  'sql',
        '.vb':   'vb',
        '.xml':  'xml',
        '.xhtml':'xhtml',
        '.sh':   'bash',
        '.html': 'html',
    }
    #try:
    buffer = file.readlines()
    buffer = "".join(buffer)
    ext = os.path.splitext(file.name)[1]
    kwargs = dict(
        syntax = SYNTAXES.get(ext, 'plain'),
        buffer = buffer,
        width = width,
        height = height,
    )
    return mark_safe(u"""<pre class="brush: %(syntax)s" width="%(width)s" height="%(height)s"
         style="display: block; overflow: scroll; width:%(width)spx; height: %(height)spx;">%(buffer)s</pre>"""%kwargs)
    #except:
    #    # Fail silently
    #    return _download_link(src, file, mimetype)
def _document_viewer(src, width, height):
    #2011/4/24
    #PDFが相対パスで飛ばされていたので、絶対パスに変更
    #modified by giginet
    from django.contrib.sites.models import Site
    site = Site.objects.get_current()
    url = u"http://%s%s" %  (site.domain, src)
    kwargs = {
        'src': url,
        'width': width,
        'height': height,
    }
    html = u"""<iframe src="http://docs.google.com/viewer?url=%(src)s&embedded=true" style="width:%(width)spx; height:%(height)spx;" frameborder="0"></iframe>"""
    return mark_safe(html % kwargs)
def _download_link(src, src2, file, mimetype, license):
    def mtimg(mimetype):
        u"""mimetypeIconを出力する"""
        if mimetype:
            tag = r"""<span class="mtimg %s"></span>""" % " ".join(mimetype.split('/'))
        else:
            tag = r"""<span class="mtimg unknown"></span>"""
        return mark_safe(tag)
    def humanize(size):
        K = 1024
        M = K * K
        G = K * M
        if size >= G:
            return "%s GB" % round(float(size) / G, 2)
        elif size >= M:
            return "%s MB" % round(float(size) / M, 2)
        elif size >= K:
            return "%s KB" % round(float(size) / K, 2)
        return "%s byte" % size
    dict_info = dict(
        mtimg = mtimg(mimetype),
        src = src,
        src2 = src2,
        title = os.path.basename(file.name),
        size = humanize(file.size)
    )
    if license == 'reject':
        return mark_safe(u"""%(mtimg)s <a href="%(src2)s"><del title="%(title)sのダウンロードは許可されていません" style="cursor: pointer">%(title)s (%(size)s)</del></a>"""%dict_info)
    return mark_safe(u"""%(mtimg)s <a href="%(src)s" title="%(title)s">%(title)s (%(size)s)</a>"""%dict_info)

def thumbnail_html(material, width, height):
    mimetype = material.mimetype()
    filetype = material.filetype()
    if filetype == 'image':
        return _image_viewer(
            url=material.get_preview_url(),
            thumbnail_url=material.get_thumbnail_url(),
            title=material.title,
            description=striptags(material.body),
            width=width,
            height=height,
        )
    elif filetype == 'audio':
        return _audio_player(
            src=material.get_preview_url(),
            mimetype=mimetype,
            width=width,
            height=height,
        )
    elif filetype == 'movie':
        return _movie_player(
            src=material.get_preview_url(),
            mimetype=mimetype,
            width=width,
            height=height,
        )
    elif filetype == 'text':
        if mimetype in ('application/vnd.ms-powerpoint', 'application/pdf'):
            return _document_viewer(
                src=material.get_preview_url(),
                width=width,
                height=height,
            )
        else:
            return _syntax_viewer(
                src=material.get_preview_url(),
                file=material.file,
                mimetype=mimetype,
                width=width,
                height=height,
            )
    else:
        return _download_link(
            src=material.get_download_url(),
            src2=material.get_preview_url(),
            file=material.file,
            mimetype=mimetype,
            license=material.license,
        )
