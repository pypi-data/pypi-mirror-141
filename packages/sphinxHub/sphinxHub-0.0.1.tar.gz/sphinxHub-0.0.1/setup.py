from setuptools import setup, find_packages






setup(
    name='sphinxHub',
    version ='0.0.1',
    author= 'Ademola Adefioye',
    author_email = 'ademola.adefioye@atyeti.com',
    description = 'Basic library helpers',
    long_description='',
    long_description_content_type = 'text/markdown',
    url = '',
    packages=find_packages(),
    classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License', 
   
  ],
    python_requires = '>=3.6',
    install_requires=[
        'cbpro',
        'requests',
        'delta-spark',
        'azure-eventhub',
    ],



)





