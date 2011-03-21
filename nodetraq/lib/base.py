"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons import request, session, tmpl_context as c, url
from pylons.controllers import WSGIController
from pylons.controllers.util import redirect
from pylons.templating import render_mako as render
from decorator import decorator
from urllib import urlencode

import base64

from nodetraq.model.meta import Session

client_user = 'nodetraq_user'
client_password = 'nodetraq_password'

class BaseController(WSGIController):

    requires_auth = False

    def __before__(self):
        c.flash = None
        c.flash_error = None
        c.active_user = None
        if 'flash' in session:
            c.flash = session['flash']
            if 'flash_error' in session:
                if session['flash_error']:
                    c.flash_error = 'flash_error'
            session['flash'] = None
            session['flash_error'] = None
            session.save()

        if 'active_user' in session:
            c.active_user = session['active_user']

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()

class AuthController(BaseController):

    requires_auth = True

    def __before__(self):
        if self.requires_auth and 'active_user' not in session:
            session['path_before_login'] = request.path_info
            session.save()
            return redirect_to(controller='auth', action='login')

        if 'active_user' in session:
            c.active_user = session['active_user']

# Authorization
def user_level(permission):
    """Authorization decorator for controller functions

    Decorating the __before__(self) will handle authorization
    for all of the sibling functions in the controller

    Ex:
        @user_level(0)
        def __before__(self):
            BaseController.__before__(self)

    You can also decorate any single functions to have their own permissions.

    Ex:
        @user_level(2)
        def showlevel(self):
            return 'User level is 2.'


    Just keep in mind that these run top down.
        __before__ first, and then the sibling functions.
        Permissions will follow the same order.

    Ex:
        @user_level(1)
        def __before__(self):
            BaseController.__before__(self)

        @editor_level(0)
        def hello(self):
            return 'Hello'

    Will require a base level of 1 to enter any of the sibling functions
    and additionally a level of 0 to enter hello.
    """

    def check_permissions(target, *args, **kwargs):
        if request.headers.has_key('Authorization'):
            auth = request.headers['Authorization']
            auth_list = auth.split(' ')
            auth_type = auth_list[0]
            if auth_type == 'Basic':
                auth_login, auth_pass = \
                    base64.b64decode(auth_list[1]).split(':')
            if auth_login == client_user and auth_pass == client_password:
                session['active_user'] = {
                    'username': 'nodeclient',
                    'user_level': 0,
                    'user_id': 9 }
                session.save()

        if 'active_user' not in session:
            session['path_before_login'] = request.path_info + \
                urlencode(request.params)
            session['flash'] = 'Login Required'
            session['flash_error'] = True
            session.save()
            return redirect(url(controller='auth', action='index'))
        if not session['active_user']:
            session['path_before_login'] = request.path_info + \
                urlencode(request.params)
            session['flash'] = 'Login Required'
            session['flash_error'] = True
            session.save()
            return redirect(url(controller='auth', action='index'))

        if permission < session['active_user']['user_level']:
            session['path_before_login'] = request.path_info + \
                urlencode(request.params)
            return redirect(url(controller='auth', action='permissions_error'))
        return target(*args, **kwargs)

    return decorator(check_permissions)
