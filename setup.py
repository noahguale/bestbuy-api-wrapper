from distutils.core import setup

setup(
    name='bestbuy',
    version='0.1.0',
    packages=['bestbuy', 'tests'],
    description='Python API wrapper for Best Buy',
    long_description=open('README.md').read(),
    author='Noah Guale',
    author_email='noahguale@gmail.com',
    url='https://github.com/noahguale/bestbuy-api-wrapper',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=open('requirements.txt').readlines(),
)
