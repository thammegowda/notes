# Sphinx Docs


> Based on https://stackoverflow.com/a/70947204/1506477

```bash
pip install -U sphinx sphinx_rtd_theme
sphinx-quickstart docs --makefile --no-batchfile  --ext-{autodoc,mathjax,viewcode,githubpages} --sep -p Sotastream -a 'Marian NMT' -l en
```
1. cd `docs`

1. edit `Makefile` to have `BUILDDIR      = latest`  (instead of build)

1. edit `source/conf.py`
    1. add `sphinx.ext.autodoc` to `extenions` list
    1. set `html_theme = 'sphinx_rtd_theme'`
    1. add module path to sys.path
    ```python
    # -- Path setup ------------------
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.absolute()))
    # <root>/docs/source/conf.py  i.e three levels up ^
    import sotastream   # import of our module should work
    ```

1. Generate API docs
    ```bash
    # run from <root>/docs dir
    sphinx-apidoc -o source ..
    ```

1. (Optional) Customize Makefile
   Remove `current/doctrees` and move `currernt/html/* -> current/`
   Also `touch  docs/.nojekyll`

1. Build

    ```bash
    make clean
    make html

    # if you have modified source code,

    ```
1. Test website locally `python -m http.server`
