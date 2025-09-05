from dash import Dash
import dash_bootstrap_components as dbc

# Inicio de la aplicacion
## Other themes https://www.bootstrapcdn.com/bootswatch/
## Cheatsheet https://hackerthemes.com/bootstrap-cheatsheet/


# Esto es para cuando el programa ejecuta en el .exe con el PyInstaller
import sys


class NullWriter:
    def write(self, s):
        pass

    def flush(self):
        pass


if sys.stdout is None:
    sys.stdout = NullWriter()
if sys.stderr is None:
    sys.stderr = NullWriter()


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])
server = app.server

