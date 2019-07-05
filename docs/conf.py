# -- Copy source files into docs and strip warnings from notebooks ------

import nbclean, os
from pathlib import Path

# read time of previous build
try:
    text = (Path.cwd() / '.last_sphinx_build').read_text()
    last_build_time = float(text)
except FileNotFoundError:
    last_build_time = 0

# iterate through all source files and check time stemps
cwd = Path.cwd()
paths = [
    f for f in cwd.parent.glob('**/*')
    if f.suffix in {'.ipynb', '.rst'}
    and 'ipynb_checkpoints' not in str(f)
    and 'docs' not in str(f)
]
for f in paths:
    time = f.stat().st_mtime
    if time > last_build_time:
        print(f)
        if 'ipynb_checkpoints' in str(f):
            continue
        # newfile is same file but in docs directory
        newfile = Path(str(f).replace(str(cwd.parent), str(cwd)))
        os.makedirs(newfile.parent, exist_ok=True)
        if f.suffix == '.rst':  # copy file
            Path(newfile).write_text(f.read_text())
        elif f.suffix == '.ipynb':  # copy and strip file
            ntbk = nbclean.NotebookCleaner(str(f))
            ntbk.clear('stderr')
            ntbk.save(str(newfile))

# write time of this build
from datetime import datetime
(Path.cwd() / '.last_sphinx_build').write_text(str(datetime.now().timestamp()))

# -- actually move all ----------------------------------------------

project = 'sunny'
copyright = '2019, Cellarity.'
author = 'Sunny Sun'

version = ''
release = version

extensions = [
    'nbsphinx',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints']
pygments_style = 'sphinx'

# -- Options for HTML output ----------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_theme_options = dict(
    navigation_depth=4,
)
html_context = dict(
    display_github=True,      # Integrate GitHub
    github_user='cellarity',   # Username
    github_repo='sunny',     # Repo name
    github_version='master',  # Version
    conf_py_path='/',    # Path in the checkout to the docs root
)
html_static_path = ['_static']

def setup(app):
    app.add_stylesheet('css/custom.css')

htmlhelp_basename = 'sunnydoc'
html_show_sphinx = False

