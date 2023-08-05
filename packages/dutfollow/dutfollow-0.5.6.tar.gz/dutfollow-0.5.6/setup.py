from distutils.core import setup
setup(
  name = 'dutfollow',         # How you named your package folder (MyLib)
  packages = ['dutfollow'],   # Chose the same as "name"
  version = '0.5.6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Followbot package for Entry',   # Give a short description about your library
  author = 'lemonbbt',                   # Type in your name=
  url = 'https://github.com/lemonbbt/',   # Provide either the link to your github or to your website
  keywords = ['FOLLOWBOT', 'DUTGYO'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)