from pywebio.output import *
from pywebio.input import *
from pywebio.session import *
from pywebio.session import get_current_session
from pywebio.pin import *
from tornado.web import create_signed_value, decode_signed_value

__all__ = ['get_all_query', 'get_query', 'set_localstorage', 'get_localstorage', 'set_cookie', 'get_cookie', 'login']


def get_all_query():
    """Get URL parameter (also known as "query strings" or "URL query parameters") as a dict"""
    query = eval_js("Object.fromEntries(new URLSearchParams(window.location.search))")
    return query


def get_query(name):
    """Get URL parameter value"""
    query = eval_js("new URLSearchParams(window.location.search).get(n)", n=name)
    return query


def set_localstorage(key, value):
    """Save data to user's web browser

    The data is specific to the origin (protocol+domain+port) of the app.
    Different origins use different web browser local storage.

    :param str key: the key you want to create/update.
    :param str value: the value you want to give the key you are creating/updating.

    You can read the value by using :func:`get_localstorage(key)`
    """
    run_js("localStorage.setItem(key, value)", key=key, value=value)


def get_localstorage(key) -> str:
    """Get the key's value in user's web browser local storage"""
    return eval_js("localStorage.getItem(key)", key=key)


def _init_cookie_client():
    session = get_current_session()
    if 'cookie_client_flag' not in session.internal_save:
        session.internal_save['cookie_client_flag'] = True
        # Credit: https://stackoverflow.com/questions/14573223/set-cookie-and-get-cookie-with-javascript
        run_js("""
        window.setCookie = function(name,value,days) {
            var expires = "";
            if (days) {
                var date = new Date();
                date.setTime(date.getTime() + (days*24*60*60*1000));
                expires = "; expires=" + date.toUTCString();
            }
            document.cookie = name + "=" + (value || "")  + expires + "; path=/";
        }
        window.getCookie = function(name) {
            var nameEQ = name + "=";
            var ca = document.cookie.split(';');
            for(var i=0;i < ca.length;i++) {
                var c = ca[i];
                while (c.charAt(0)==' ') c = c.substring(1,c.length);
                if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
            }
            return null;
        }
        """)


def set_cookie(key, value, days=7):
    _init_cookie_client()
    run_js("setCookie(key, value, days)", key=key, value=value, days=days)


def get_cookie(key):
    _init_cookie_client()
    return eval_js("getCookie(key)", key=key)


def login(*, basic_auth=None, custom_auth=None, salt=None, expire_days=7):
    """Persistence auth

    You need to provide a function to implement your auth logic and pass it to ``basic_auth`` or ``custom_auth``
    parameter.

    :param callable basic_auth: ``(username, password) -> is_succeed:bool``
    :param callable custom_auth: ``() -> username:str``
    :param str salt: HMAC secret for the signature. It should be a long, random str.
    :param int expire_days: how many days the auth state can keep valid.
       After this time, logged-in users need to log in again.
    :return str: username of the currently logged-in user
    """
    assert bool(basic_auth) != bool(custom_auth), "You can only assign to one of `basic_auth` or `custom_auth`"

    token = get_localstorage('webio-token')  # get token from user's web browser
    # try to decrypt the username from the token
    username = decode_signed_value(salt, 'token', token, max_age_days=expire_days)
    if not token or not username:  # no token or token validation failed
        while True:
            if basic_auth:
                user = input_group('Login', [
                    input("Username", name='username'),
                    input("Password", type=PASSWORD, name='password'),
                ])
                username = user['username']
                ok = basic_auth(username, user['password'])
            else:
                username = ok = custom_auth()

            if ok:
                signed = create_signed_value(salt, 'token', username).decode("utf-8")  # encrypt username to token
                set_localstorage('token', signed)  # set token to user's web browser
                break

    return username
