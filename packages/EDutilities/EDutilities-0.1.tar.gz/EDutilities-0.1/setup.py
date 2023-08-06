import setuptools

#with open("latex/README.md", "r") as fh:
#    long_description = fh.read()

setuptools.setup(
    name="EDutilities",
    version="0.1",
    author="Tarik Ronan Drevon",
    author_email="tarik.drevon@stfc.ac.uk",
    description="Continuous Electron Diffraction utilities ",
    long_description=' ', #long_description,
    long_description_content_type="",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License ",
        "Operating System :: POSIX :: Linux ",
    ],
    python_requires='>=3.8',
    install_requires=[
        # 'EDutils','TDdisplay',
        # 'numpy','scipy','matplotlib','colorama','pandas',
        # 'easygui','tifffile','bsd','pickle5','bs4'
        ],
)
