# Ref: http://djangosnippets.org/snippets/160/

from django.template import add_to_builtins
add_to_builtins('compress.templatetags.compressed')
add_to_builtins('reversetag.templatetags.reversetag')
add_to_builtins('templatetags.templatetags.call')
add_to_builtins('templatetags.templatetags.expr')
add_to_builtins('templatetags.templatetags.macro')
add_to_builtins('templatetags.templatetags.smart_if')
add_to_builtins('templatetags.templatetags.switchcase')
add_to_builtins('templatetags.templatetags.truncateletters')
