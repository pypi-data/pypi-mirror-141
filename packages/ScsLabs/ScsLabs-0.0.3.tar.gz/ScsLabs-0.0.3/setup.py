from setuptools import setup, find_packages

def readme() -> str:
    with open(r'README.md') as f:
        README = f.read()
    return README

classifiers = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Education',
    'Operating System :: Unix',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='ScsLabs',
    version='0.0.3',
    description='ScsLabs adalah modul edukasi untuk Pemula / Expert.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/SkullCyberSecurity/ScsLabs',
    author='TomsDroid',
    author_email='tomsdroid@kingeagle.tech',
    license='MIT',
    classifiers=classifiers,
    keywords=['scs', 'skullcybersecurity', 'whois-domain', 'whois'],
    packages=find_packages(),
    install_requires=['requests','beautifulsoup4']
)
