from setuptools import setup

setup(
    name='sidd',
    version='1',    
    description='A simple image de-duplication library.',
    url='https://github.com/RubberClucky/SIDD',
    author='Zachary Higgins',
    author_email='zachhiggins@gmail.com',
    key_words="image, probalistic, comparison, duplicates, cleanup",
    license='mit',
    packages=['sidd'],
    install_requires=['opencv-python',
                      'tqdm',
                      'numpy'                     
                      ],

    classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Information Technology",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Operating System :: MacOS",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: Unix",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
    ],
)