# -*- coding: utf-8 -*-

# A very simple setup script to create a single executable
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

from cx_Freeze import setup, Executable

executables = [
    Executable('compress_image_fb2')
]

setup(name='compress_image_fb2',
      version='0.1',
      description='compress_image_fb2',
      executables=executables
      )
