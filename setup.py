from setuptools import setup, find_packages

setup(
    name='AudioFingerprinter',
    version='0.1',
    packages=find_packages(),
    install_requires=['pyacoustid==1.3.0',
                      'setuptools==70.0.0',
                      'pydub==0.25.1',
                      'flask==3.0.3',
                      'marshmallow==3.21.2',
                      'marshmallow_dataclass==8.6.1',
                      'python-dotenv==0.0.5'],
)
