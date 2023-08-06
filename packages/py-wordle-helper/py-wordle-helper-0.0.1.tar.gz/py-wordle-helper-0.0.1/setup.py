import setuptools

__description__ = 'The package targets protocol for uploading and reusing task and libraries'

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='py-wordle-helper',
     version='0.0.1',
     author="Saurabh Pandey",
     py_modules=["wordlehelper"],
     entry_points={
        'console_scripts': [
            'wordlehelper=wordlehelper:execute'
        ],
     },
     author_email="saurabh@ask-jennie.com",
     description=__description__,
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/dextrop/wordlehelper",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )