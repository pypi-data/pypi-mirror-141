from setuptools import setup

setup(
    name='rembrandt_cli',
    version='',
    packages=[''],
    url='https://github.com/GecraftetHD/rembrandt_cli',
    license='',
    author='Gecraftet_hd',
    author_email='',
    description='cryptic game client and library',
    entrypoints={
        'console_scripts': [
            'rembrandt = rembrandt_cli.rembrandt:main',
        ]
    }
)
