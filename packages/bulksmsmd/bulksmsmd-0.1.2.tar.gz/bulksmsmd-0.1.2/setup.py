try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

from bulksmsmd import __version__

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().splitlines()

setup(
    name='bulksmsmd',
    version=__version__,
    description='Python wrapper for Unifun BulkSMSAPI (bulksms.md)',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    author='Mark Melnic',
    author_email='me@markmelnic.com',
    url='https://github.com/markmelnic/bulksmsmd',
    packages=find_packages(),
    package_dir={'bulksmsmd': 'bulksmsmd'},
    include_package_data=True,
    package_data={'': ['stdlib', 'mapping']},
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    keywords='python api wrapper unifun bulksms bulksmsmd bulksmsapi',
    classifiers=[
        'Natural Language :: English',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)