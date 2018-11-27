from setuptools import setup, find_packages

setup(
    name='sonogram-deepspeech',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'deepspeech',
        'sox',
        'sounddevice'
    ]
)