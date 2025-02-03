from setuptools import setup, find_packages

setup(
    name="ScanTrek",
    version="0.1.0",
    author="D3crypT0r",
    packages=find_packages(),
    install_requires=[
        'requests>=2.28',
        'beautifulsoup4>=4.11',
        'waybackpy>=3.0',
        'tldextract>=3.4',
        'pandas>=1.5'
    ],
    entry_points={
        'console_scripts': [
            'ScanTrek=main:main',
            'ScanTrek=worker:main'
        ]
    }
)
