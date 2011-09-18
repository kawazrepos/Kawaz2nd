# -*- coding: utf-8 -*-
#
# Created:    2010/09/02
# Author:         alisue
#
from markdown import markdown as _markdown

import re

def markdown(source, **kwargs):
    # See. http://www.freewisdom.org/projects/python-markdown/Extra
    # 面倒くさいからHTMLの許可を廃止する
    kwargs['safe_mode'] = 'replace'
    result = _markdown(source, extensions=['extra'], **kwargs)
#    result = result.replace('<pre><code', '<pre class="code"><code')
#    # 表示を著しく変更可能なアトリビュート・タグは排除
#    # 多分markdownでほとんど削除されているが念のため
#    result = re.sub(r"""style\s*=\s*['"]?.*['"]?""", '', result)
#    result = re.sub(r"""<\s*basefont.*>(.*)<\s*/basefont\s*>""", '\1', result)
#    result = re.sub(r"""<\s*font.*>(.*)<\s*/font\s*>""", '\1', result)
#    result = re.sub(r"""<\s*iframe.*>(.*)<\s*/iframe\s*>""", '\1', result)
    return result

def comment_markdown(source, **kwargs):
    # See. http://www.freewisdom.org/projects/python-markdown/Extra
    # 面倒くさいからHTMLの許可を廃止する
    kwargs['safe_mode'] = 'replace'
    # >>1みたいなのをそのまま投稿するために置き換え
    source = re.sub(r">>(\d+)", r"\>\>\1", source)
    result = _markdown(source, extensions=['extra'], **kwargs)
    return result
