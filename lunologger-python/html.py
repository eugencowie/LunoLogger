def tag(tag, content, attr=''):
    return '<{tag} {attr}>{content}</{tag}>'.format(tag=tag, content=content, attr=attr)

def html(content):
    return tag('html', content)

def head(content):
    return tag('head', content)

def link(rel, src):
    return '<link rel="{}" href="{}">'.format(rel, src)

def style(content):
    return tag('style', content)

def body(content):
    return tag('body', content)

def table(content, attr=''):
    return tag('table', content, attr)

def tr(content, attr=''):
    return tag('tr', content, attr)

def th(content):
    return tag('th', content)

def td(content):
    return tag('td', content)
