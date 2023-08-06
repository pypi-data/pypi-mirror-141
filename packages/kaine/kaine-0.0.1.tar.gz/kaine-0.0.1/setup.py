import sys
import platform
import setuptools

import kaine

if sys.version_info < (3,):
    print('Python 2 has reached end-of-life and is no longer supported by Kaine.')
    sys.exit(-1)
if sys.platform == 'win32' and sys.maxsize.bit_length() == 31:
    print('32-bit windows Python runtime is not supported. Please switch to 64-bit Python.')
    sys.exit(-1)

python_min_version = (3, 8, 0)
python_min_version_str = '.'.join(map(str, python_min_version))
if sys.version_info < python_min_version:
    print(f'You are using Python {platform.python_version()}. Python >= {python_min_version_str} is required.')
    sys.exit(-1)


with open('README.md', 'r') as f:
    long_description = f.read()


setuptools.setup(
    name='kaine',
    version=kaine.__version__,
    author='winterchild',
    author_email='demie.oh@gmail.com',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/demianoh/Kaine',
    packages=setuptools.find_packages(),
    classifier=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8'
)
