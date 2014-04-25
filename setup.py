from setuptools import setup, find_packages

setup(
    name = 'drawille',
    version = '0.0.1',
    author = 'Adam Tauber',
    author_email = 'asciimoo@gmail.com',
    description = ('Drawing in terminal with unicode braille characters'),
    license = 'AGPLv3+',
    keywords = "terminal braille drawing canvas console",
    url = 'https://github.com/asciimoo/drawille',
    scripts = ['drawille.py'],
    py_modules = ['drawille'],
    packages = find_packages(),
    install_requires = [],
    download_url = 'https://github.com/asciimoo/drawille/tarball/master',
    # TODO
    #entry_points={
    #    "console_scripts": ["drawille=drawille:__main__"]
    #},
    classifiers = [
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        'Environment :: Console',
        'License :: OSI Approved :: GNU Affero General Public License v3'
    ],
)
