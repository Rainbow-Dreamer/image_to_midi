from setuptools import setup, find_packages
from os import path

setup(
    name='image_to_midi',
    packages=['image_to_midi'],
    version='0.19',
    license='LGPLv2.1',
    description=
    'This is a python package that turns any images into MIDI files that views the same as them',
    author='Rainbow-Dreamer',
    author_email='1036889495@qq.com',
    url='https://github.com/Rainbow-Dreamer/image_to_midi',
    download_url=
    'https://github.com/Rainbow-Dreamer/image_to_midi/archive/0.19.tar.gz',
    keywords=['music', 'image', 'midi'],
    install_requires=['musicpy', 'pillow'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    include_package_data=True)
