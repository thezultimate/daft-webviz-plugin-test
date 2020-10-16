#!/usr/bin/env python
# -*- coding: utf-8 -*-

# AUTOMATICALLY MADE FILE. DO NOT EDIT.
# This file was generated by DAFT on 2020-10-16 with Python executable
# /Users/DAFT/Documents/Coding/python/dev_env/bin/python3

import logging
import threading
import datetime
from pathlib import Path, PosixPath, WindowsPath

import dash
import dash_core_components as dcc
import dash_html_components as html
from flask_talisman import Talisman
import webviz_config
import webviz_config.certificate
from webviz_config.themes import installed_themes
from webviz_config.common_cache import CACHE
from webviz_config.webviz_store import WEBVIZ_STORAGE
from webviz_config.webviz_assets import WEBVIZ_ASSETS

import webviz_config.plugins as standard_plugins


# We do not want to show INFO regarding werkzeug routing as that is too verbose,
# however we want other log handlers (typically coming from webviz plugin dependencies)
# to be set to user specified log level.
logging.getLogger("werkzeug").setLevel(logging.WARNING)
logging.getLogger().setLevel(logging.WARNING)

theme = webviz_config.WebvizConfigTheme("default")
theme.from_json((Path(__file__).resolve().parent / "theme_settings.json").read_text())

app = dash.Dash(
    __name__,
    external_stylesheets=theme.external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
)
app.logger.setLevel(logging.WARNING)
server = app.server

app.title = "Test login plugin"
app.config.suppress_callback_exceptions = True

app.webviz_settings = {
    "shared_settings": webviz_config.SHARED_SETTINGS_SUBSCRIPTIONS.transformed_settings(
        {}, PosixPath('/Users/DAFT/Documents/Coding/Equinor/webviz/daft-webviz-plugin-test/examples'), True
    ),
    "portable": True,
    "theme": theme,
}

CACHE.init_app(server)

theme.adjust_csp({"script-src": app.csp_hashes()}, append=True)
Talisman(server, content_security_policy=theme.csp, feature_policy=theme.feature_policy)

WEBVIZ_STORAGE.use_storage = True
WEBVIZ_STORAGE.storage_folder = Path(__file__).resolve().parent / "webviz_storage"

WEBVIZ_ASSETS.portable = True

if False and not webviz_config.is_reload_process():
    # When Dash/Flask is started on localhost with hot module reload activated,
    # we do not want the main process to call expensive component functions in
    # the layout tree, as the layout tree used on initialization will anyway be called
    # from the child/restart/reload process.
    app.layout = html.Div()
else:
    page_content = {}
    
    page_content["front-page"] = [
       dcc.Markdown(r"""This is a `webviz` instance created from the following configuration file."""),
       standard_plugins.SyntaxHighlighter(**{'filename': PosixPath('/Users/DAFT/Documents/Coding/Equinor/webviz/daft-webviz-plugin-test/examples/basic_example.yaml'), 'dark_theme': True}).plugin_layout(contact_person=None),
       dcc.Markdown(r"""---"""),
       standard_plugins.SomeCustomPlugin(**{}).plugin_layout(contact_person=None),
       dcc.Markdown(r"""---"""),
       standard_plugins.LoginPlugin(app=app, **{}).plugin_layout(contact_person=None)
       ]
    
    page_content["some-other-page"] = [
       standard_plugins.SomeOtherCustomPlugin(app=app, **{}).plugin_layout(contact_person=None)
       ]
    
    app.layout = html.Div(
        className="layoutWrapper", 
        children=[html.Div(
            children=[dcc.Location(
                id='url', refresh=True),
        html.Div(
            className="sideWrapper",
            children=[
            
                dcc.Link("",
                    id="logo",
                    className="styledLogo",
                    href="/",),
                dcc.Link("Some other page",
                    # We will create a webviz-core-components
                    # component instead of styling dcc.Link's,
                    # then we can more easily change className to
                    # selectedButton for current page.
                    className="styledButton",
                    id="some-other-page",
                    href="/some-other-page",)
            ])]),
        html.Div(className="pageContent", id="page-content")])


@app.callback(dash.dependencies.Output("page-content", "children"),
              dash.dependencies.Input("url", "pathname"))
def update_page(pathname):
    pathname = pathname.replace("/", "")
    if not pathname:
        pathname = "front-page"
    return page_content.get(pathname, "Oooppss... Page not found.")



if __name__ == "__main__":
    # This part is ignored when the webviz app is started
    # using Docker container and uwsgi (e.g. when hosted on Azure).
    #
    # It is used only when directly running this script with Python,
    # which will then initialize a localhost server.

    port = webviz_config.utils.get_available_port(preferred_port=5000)

    token = webviz_config.LocalhostToken(app.server, port).one_time_token
    webviz_config.utils.LocalhostOpenBrowser(port, token)

    webviz_config.utils.silence_flask_startup()

    app.run_server(
        host="localhost",
        port=port,
        ssl_context=webviz_config.certificate.LocalhostCertificate().ssl_context,
        debug=False,
        use_reloader=False,
        dev_tools_prune_errors=False,
      
    )