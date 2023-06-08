import sys

from cx_Freeze import setup, Executable

# Definir o que dever ser incluído na pasta final
# Saida de arquivos

build_exe_options = {'packages': ['os', 'scrapy'],
                     'includes': ['tkinter', 'PySimpleGUI', 'openpyxl', 'scrapy.http',
                                  'itemadapter', 'scrapy.spiderloader', 'scrapy'],

                     'include_files': ['scrapy_tjsp', 'scrapy.cfg', 'interface.py']
                     }
base = None

programa = r'C:\Users\moise\OneDrive\Área de Trabalho\AUTOMAÇÕES\testes\scrapy_tjsp\spiders\tj.py'

if sys.platform == 'win32':
    base = 'Win32GUI'

# Configurar o executável
setup(
    name='Automatizador de login',
    version='1.0',
    description='Este programa automatiza o login de um site',
    author='Moises Melo',
    options={'build_exe': build_exe_options},
    executables=[Executable(programa, base=base)],
    base='Console'
)
