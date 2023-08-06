from setuptools import setup, find_packages
import sys

# Python 3.0 or later needed
if sys.version_info < (3, 0, 0, 'final', 0):
    raise SystemExit('Python 3.0 or later is required!')


print("""
 ____          _ _               _   _              
|  _ \ ___  __| (_)_ __ ___  ___| |_(_) ___  _ __   
| |_) / _ \/ _` | | '__/ _ \/ __| __| |/ _ \| '_ \  
|  _ <  __/ (_| | | | |  __/ (__| |_| | (_) | | | | 
|_| \_\___|\__,_|_|_|  \___|\___|\__|_|\___/|_| |_| 
                                                    
  ___   __ 
 / _ \ / _|
| | | | |_ 
| |_| |  _|
 \___/|_|  
           
                 _                                          _ _    
 _ __  _   _  __| | _____   ___ __ ___   __ _ _ __      ___| | |_  
| '_ \| | | |/ _` |/ _ \ \ / / '_ ` _ \ / _` | '__|    / _ \ | __| 
| |_) | |_| | (_| |  __/\ V /| | | | | | (_| | |      |  __/ | |_  
| .__/ \__, |\__,_|\___| \_/ |_| |_| |_|\__, |_|____   \___|_|\__| 
|_|    |___/                            |___/ |_____|              
""")


setup(
    name= 'pydevmgr',
    version= '0.3', # https://www.python.org/dev/peps/pep-0440/
    author='Sylvain Guieu',
    author_email='sylvain.guieu@univ-grenoble-alpes.fr',
    packages=[],
    #scripts=scripts,
    #data_files=data_files,
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    install_requires=['pydevmgr_elt'],
    
    extras_require={
    },
    
    dependency_links=[],
    long_description_content_type='text/markdown',
    
    include_package_data=True, 
    package_data= {
    }, 
    entry_points = {
        'console_scripts': [],
    }
)
