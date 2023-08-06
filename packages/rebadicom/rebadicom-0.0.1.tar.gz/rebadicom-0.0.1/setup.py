# authors : Frank Kwizera <frankpmn@gmail.com>
# license : MIT

from setuptools import setup

setup(
    name="rebadicom",
    version='0.0.1',
    description="",
    py_modules=['study', 'image'],
    package_dir={'': 'src'},
    install_requires = [
        "cycler==0.11.0",
        "flake8==4.0.1",
        "fonttools==4.29.1",
        "importlib-metadata==4.2.0",
        "kiwisolver==1.3.2",
        "matplotlib==3.5.1",
        "mccabe==0.6.1",
        "numpy==1.21.5",
        "packaging==21.3",
        "Pillow==9.0.1",
        "pycodestyle==2.8.0",
        "pydicom==2.2.2",
        "pyflakes==2.4.0",
        "pyparsing==3.0.7",
        "python-dateutil==2.8.2",
        "six==1.16.0",
        "typing-extensions==4.1.1",
        "zipp==3.7.0",
    ],
)