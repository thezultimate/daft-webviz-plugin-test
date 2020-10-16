#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime
from pathlib import Path, PosixPath, WindowsPath

import dash

import webviz_config
from webviz_config.themes import installed_themes
from webviz_config.webviz_store import WEBVIZ_STORAGE
from webviz_config.webviz_assets import WEBVIZ_ASSETS
from webviz_config.common_cache import CACHE

import webviz_config.plugins as standard_plugins


logging.getLogger().setLevel(logging.WARNING)

theme = webviz_config.WebvizConfigTheme("default")
theme.from_json((Path(__file__).resolve().parent / "theme_settings.json").read_text())

app = dash.Dash()
app.config.suppress_callback_exceptions = True

app.webviz_settings = {
    "shared_settings": webviz_config.SHARED_SETTINGS_SUBSCRIPTIONS.transformed_settings(
        {}, PosixPath('/Users/DAFT/Documents/Coding/Equinor/webviz/daft-webviz-plugin-test/examples'), False
    ),
    "theme": theme,
}

CACHE.init_app(app.server)

WEBVIZ_STORAGE.storage_folder = Path(__file__).resolve().parent / "webviz_storage"

# The lines below can be simplified when assignment
# expressions become available in Python 3.8
# (https://www.python.org/dev/peps/pep-0572)

plugins = []






plugins.append(standard_plugins.SyntaxHighlighter(**{'filename': PosixPath('/Users/DAFT/Documents/Coding/Equinor/webviz/daft-webviz-plugin-test/examples/basic_example.yaml'), 'dark_theme': True}))





plugins.append(standard_plugins.SomeCustomPlugin(**{}))





plugins.append(standard_plugins.LoginPlugin(app=app, **{}))





plugins.append(standard_plugins.SomeOtherCustomPlugin(app=app, **{}))




for plugin in plugins:
    if hasattr(plugin, "add_webvizstore"):
        WEBVIZ_STORAGE.register_function_arguments(plugin.add_webvizstore())

WEBVIZ_ASSETS.make_portable(Path(__file__).resolve().parent / "assets")

WEBVIZ_STORAGE.build_store()