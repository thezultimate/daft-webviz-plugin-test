import dash_html_components as html
import dash_core_components as dcc
import msal
import requests
import json
from ..plugins import env_var as Env_var
from webviz_config import WebvizPluginABC
from dash.dependencies import Input, Output
from flask import request, session, redirect

class LoginPlugin(WebvizPluginABC):
    def __init__(self, app):
        super().__init__()

        self._tenant_id = Env_var.get_tenant_id()
        self._client_id = Env_var.get_client_id()
        self._client_secret = Env_var.get_client_secret()
        self._scope = Env_var.get_scope()
        self._authority = Env_var.get_authority()
        self._session_secret_key = Env_var.get_session_secret_key()
        self._sumo_base_url = Env_var.get_sumo_base_url()

        self._set_app_secret_key(app)
        self._set_callbacks(app)

        self._msal_app = msal.ConfidentialClientApplication(client_id=self._client_id, 
                                                            client_credential=self._client_secret, 
                                                            authority=self._authority)

        self._origin_url = None

    @property
    def layout(self):
        return html.Div(
            [
                html.Div(id="test_url_login"),
                html.H1("Login plugin"),
                html.H3("Logged in user info:"),
                html.Div([
                    html.Div(id="login_info_name"),
                    html.Div(id="login_info_job"),
                    html.Div(id="login_info_office"),
                    html.Div(id="login_info_email")
                ]),
            ]
        )

    def _set_callbacks(self, app):
        @app.callback(
            [Output("login_info_name", "children"),
             Output("login_info_job", "children"),
             Output("login_info_office", "children"),
             Output("login_info_email", "children")],
            [Input("url", "href")]
        )
        def url_changed(url_info):
            print("url_changed: url_info:", url_info)
            print("url_changed: self._origin_url:", self._origin_url)
            # print("url_changed: session:", session)

            if not self._origin_url:
                self._origin_url = url_info
                print("url_changed: self._origin_url after setting:", self._origin_url)

            if not session.get("access_token"):
                print("url_changed: No session with key 'access_token' has been set!")
                return dcc.Location(pathname="/login", id="login"), "", "", ""

            if self._origin_url == url_info:
                # Request something to Sumo
                sumo_url = self._sumo_base_url + "api/v1/userprofile"
                header = { "Authorization": "Bearer " + session.get("access_token") }
                res = requests.get(sumo_url, headers=header)
                print("url_changed: sumo response:", res.status_code, res.reason)
                
                if res.content:
                    content_json = json.loads(res.content.decode("utf-8"))
                    if content_json:
                        return content_json.get("displayName"), content_json.get("jobTitle"), content_json.get("officeLocation"), content_json.get("mail")
            
                if res.status_code == 401:
                    return dcc.Location(pathname="/login", id="login"), "", "", ""

            return "", "", "", ""

        @app.server.route("/login")
        def login_controller():
            redirect_uri = get_redirect_uri(request.url_root)
            print("login_controller: redirect-uri:", redirect_uri)
            auth_url = self._msal_app.get_authorization_request_url(scopes=self._scope.split(), redirect_uri=redirect_uri)
            return redirect(auth_url)

        @app.server.route("/auth-return")
        def auth_return_controller():
            redirect_uri = get_redirect_uri(request.url_root)
            print("auth_return_controller: redirect-uri:", redirect_uri)
            returned_query_params = request.args
            print("auth_return_controller: request.args:", returned_query_params)
            for key, value in returned_query_params.items():
                print("auth_return_controller: request.args: key={}, value={}".format(key, value))
            # print("auth_return_controller: returned_query_params:", returned_query_params)
            code = returned_query_params.get("code")
            tokens_result = self._msal_app.acquire_token_by_authorization_code(code=code, scopes=self._scope.split(), redirect_uri=redirect_uri)
            # print("auth_return_controller: tokens-result:", tokens_result)
            session["access_token"] = tokens_result.get("access_token")
            session["refresh_token"] = tokens_result.get("refresh_token")
            print("auth_return_controller: self._origin_url:", self._origin_url)
            return redirect(self._origin_url)

    def _set_app_secret_key(self, app):
        app.server.secret_key = self._session_secret_key

def replace_http_with_https(str):
    return str.replace("http://", "https://")

def get_redirect_uri(url_root):
    return replace_http_with_https(url_root + "auth-return")