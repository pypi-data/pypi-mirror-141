import setuptools


setuptools.setup(
   name='mojang_python',
   version='1.0.1',
   description='Easy Mojang API Wrapper',
   licence = 'Apache',
   long_description=open('README.md').read(),
   long_description_content_type='text/markdown',
   url = "https://github.com/Hades1232/mojang_python",
   author='Hades_',
   packages=setuptools.find_packages(), 
   install_requires=['requests', 'datetime'],
   python_requires='>=3.5'
)
