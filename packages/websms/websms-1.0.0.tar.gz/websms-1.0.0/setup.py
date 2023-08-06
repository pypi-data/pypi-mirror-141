from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()


setup(
    name='websms',
    version='1.0.0',
    description=(
        'Python library that allows to send messages using websms platform.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/W-Z-FinTech-GmbH/websms',
    author='W&Z FinTech GmbH',
    author_email='dk@ownly.de',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
    ],
    keywords='sms websms message text phone sender mobile',
    py_modules=['websms'],
    install_requires=['requests >= 2.25'],
    test_suite='tests',
    tests_require=['mock'],
)
