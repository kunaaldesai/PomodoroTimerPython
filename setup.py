from setuptools import setup

APP = ['pomodoro.py']
DATA_FILES = [('', ['alarm.mp3'])]
OPTIONS = {
    'argv_emulation': True,
    # 'iconfile': 'path_to_icon.icns'  # For icon later
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)


### RUN IN TERMINAL BY TYPING:
### ### python setup.py py2app
