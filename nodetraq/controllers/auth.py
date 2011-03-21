import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from nodetraq.lib.base import BaseController, render
from nodetraq.lib.directoryhelper import check_user

from nodetraq.model.meta import Session

log = logging.getLogger(__name__)

class AuthController(BaseController):

    def index(self):
        c.title = "Login"
        c.selected_page = 'auth'
        c.subpage = 'login'
        return render('auth/login.mako')

    def login(self):
        error = False

        if request.params.has_key('username') \
                and request.params.has_key('password'):
            username = request.params['username']
            password = request.params['password']
            if not username or not password:
                error = True
            result = check_user(username, password)
            if result[0]:
                session['flash'] = 'Successfully logged in'
                session['active_user'] = { 'username': result[0], 'user_id': result[1], 'user_level': result[2]}
                session.save()
            else:
                error = True
        else:
           error = True

        if error:
            if result:
                session['flash'] = result[1][0]['desc']
            else:
                session['flash'] = 'Error Logging in'
            session['flash_error'] = True
            session.save()
            return redirect(url(controller='auth', action='index'))

        if session['active_user']['user_level'] == 0:
            if 'path_before_login' in session:
                if session['path_before_login']:
                    return redirect(url(session['path_before_login']))
        else:
            return redirect(url(controller='nodes', action='show_dbbackups'))

        return redirect(url('/'))


    def logout(self):
        session['active_user'] = None
        session['flash'] = 'Successfully logged out'
        session.save()
        return redirect(url(controller='auth', action='index'))

    def permissions_error(self):
        return 'You do not have sufficient privileges to acess this page.'

