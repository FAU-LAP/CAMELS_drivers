python -m build
python -m twine upload --skip-existing dist\*
del /S /Q dist