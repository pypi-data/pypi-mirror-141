import setuptools
from scRNA.utils import _version, _pipelist

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as fp:
    install_requires = fp.read()

setuptools.setup(
    name="DNBC4_test",
    version=_version,
    author="lishuangshuang3",
    author_email="lishuangshuang3@mgi-tech.com",
    description="DNBC4 scRNA QC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MGI-tech-bioinformatics/DNBelab_C_Series_HT_scRNA-analysis-software",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    include_package_data=True,
    #entry_points=entry_dict,
    install_requires=install_requires,
)
