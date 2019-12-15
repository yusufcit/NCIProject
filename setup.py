import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EVDataIreland", # Replace with your own username
    version="2.0.1",
    author="Yusuf, Alain, David",
    author_email="yusufcit@gmail.com",
    install_requires=['psycopg2', 'pandas', 'datetime', 'requests','folium', 'plotly','bs4','beautifulsoup4','wget','orca','matplotlib','scipy'],
    description="Packaging up EV data ireland project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yusufcit/NCIProject.git",
    packages=setuptools.find_packages("NCIProject"),
    package_dir={'': 'NCIProject'},
    py_modules = ['StartEVapp'],
    entry_points={
        'console_scripts': [
            'StartEVapp = StartEVapp:main',
	        ],
        },
    # *strongly* suggested for sharing
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)