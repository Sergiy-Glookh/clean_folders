from setuptools import setup, find_namespace_packages

setup(name='clean_folder_Sergiy_Glookh',
      version='0.0.2',
      description='Recursively sorting files in a specified folder based on their extensions and normalizing file names',
      long_description=open('README.md', 'r', encoding='utf-8').read(),
      long_description_content_type='text/plain',      
      python_requires='>=3.11',  
      classifiers = ["Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                    ],
      url='https://github.com/Sergiy-Glookh/cleans_folder',
      author='Sregiy Glookh',
      author_email='sglookh@gmail.com',
      license='MIT',
      packages=find_namespace_packages(),
      include_package_data=True,
      install_requires=['py7zr'],
      entry_points={'console_scripts': ['clean-folder = clean_folder.clean:disassemble_junk']}
      )

