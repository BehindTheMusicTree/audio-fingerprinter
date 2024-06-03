from setuptools import setup, find_packages

setup(
    name='AudioFingerprintGenerator',
    version='0.1',
    packages=find_packages(),
    install_requires=['pyacoustid==1.3.0',
                      'django==5.0.6',
                      'setuptools==69.2.0',
                      'pydub==0.25.1',
                      'flask==3.0.3',
                      'marshmallow==3.21.2',
                      'marshmallow_dataclass==8.6.1'],
)
