from setuptools import setup

setup(name='GLaDOS alpha',
      version='1.0',
      description='General Lookup of α-Decay for Optimised Search (GLαDOS)',
      url='https://github.com/Yottaphy/glados',
      author='Jorge Romero',
      author_email='joromero@jyu.fi',
      license='GPL-3.0',
      packages=['glados_alpha'],
      install_requires=[
          'argparse',
      ],
      zip_safe=False,
      entry_points={
        'console_scripts': [
            'glados_alpha = glados_alpha:main'
        ]},
    )