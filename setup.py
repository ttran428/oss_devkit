from setuptools import setup

setup(
    name='testgit',
    version='0.1',
    py_modules=['testgit'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        testgit=testgit:cli
    ''',
)