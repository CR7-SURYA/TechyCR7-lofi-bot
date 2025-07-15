from setuptools import setup

setup(
    name='TechyCR7-lofi-bot',
    version='1.0',
    description='Telegram bot to convert music into LoFi with effects.',
    author='@SuryaXCristiano',
    py_modules=['bot'],
    install_requires=[
        'pydub',
        'requests'
    ],
)
