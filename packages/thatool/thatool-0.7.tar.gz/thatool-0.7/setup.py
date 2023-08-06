from setuptools import setup, find_packages

setup(
  name = 'thatool',         # How you named your package folder (MyLib)
  version = '0.7',      # Start with a small number and increase it with every change you make
  author = 'Cao Thang',                   # Type in your name
  author_email = 'caothangckt@gmail.com',      # Type in your E-Mail
  description = 'TYPE YOUR DESCRIPTION HERE',   # Give a short description about your library
  long_description='This package contains the docs for several in-house codes to handle some specific tasks.',
  # license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
#   url = 'https://github.com/user/reponame',   # Provide either the link to your github or to your website
#   download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
#   keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best

  packages = find_packages(),
  install_requires=[            # I get to this in a second
          'scipy', 
          'pandas', 
          'matplotlib', 
          'lmfit', 
          'shapely',
          'jypyterlab',
      ],

  python_requires='>=3.7',

  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'Programming Language :: Python :: 3.7',
  ],

)



# Ref: https://aaltoscicomp.github.io/python-for-scicomp/packaging/