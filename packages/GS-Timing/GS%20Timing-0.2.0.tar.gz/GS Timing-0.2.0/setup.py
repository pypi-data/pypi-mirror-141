import setuptools

setuptools.setup(
    name='GS Timing',
    version='0.2.0',
    author='Gabriel Staples',
    description='Better timing resolution on Win and Linux',
    packages = ['GStiming'])

# cd "Dropbox (ORNL)\ELIT testing\plugin for ELIT\!PACKAGE"
# python setup.py sdist bdist_wheel
# twine upload dist/*
# twine upload --skip-existing dist/*
