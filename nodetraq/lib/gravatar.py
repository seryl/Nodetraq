import urllib, hashlib
from webhelpers.html import literal

def get_gravatar_url(email, size=48, default_type='identicon'):
    """Returns the url for the users gravatar.
    Usage:

    """
    gravatar_url = "https://secure.gravatar.com/avatar.php?"
    gravatar_url += urllib.urlencode({
        'gravatar_id': hashlib.md5(email.lower()).hexdigest(),
        'default': default_type,
        'size': str(size)
        })
    return gravatar_url

def gravatar(email, _class=None, size=48, default_type='identicon'):
    if _class:
        return literal('<img src="' + \
                get_gravatar_url(email, size, default_type) + \
                '" class="' + _class + '" />')
    else:
        return literal('<img src="' + \
                get_gravatar_url(email, size, default_type) + '" />')

