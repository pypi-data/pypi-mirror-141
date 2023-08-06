
from distutils.core import setup
setup(
    name='cofffee',         # How you named your package folder (MyLib)
    # include_package_data=True,
    packages=['cofffee'],   # Chose the same as "name"
    # Start with a small number and increase it with every change you make
    version='1.0.010',
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='A complete python visualizer, using an intuitive, conssistent, and approachable, OOP framework.',
    author='Brian J. Masse',                   # Type in your name
    author_email='brianm25it@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/Brian-Masse/Coffee',
    # I explain this later on
    download_url='https://github.com/Brian-Masse/Coffee/archive/refs/tags/v1.0.07.tar.gz',
    keywords=['Visualization', 'python', 'pandas', 'rendering', 'data', 'customizable',
              'powerful', 'intuitive'],   # Keywords that define your package best
    package_dir={"cofffee":"cofffee"},
    package_data={"cofffee": ["extra/coffee.xlsx"]},
    install_requires=[            # I get to this in a second
        'numpy',
        'pandas',
        'pygame',
        'matplotlib',
        'openpyxl'
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
