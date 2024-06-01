from setuptools import setup, find_packages

setup(
    name='AudioFingerprintGenerator',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pyacoustid==1.3.0',
        'django==5.0.6',
    ],
)