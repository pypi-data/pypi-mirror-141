import setuptools

setuptools.setup(
    name="QuangDinhdemopackage2",
    version="0.0.1",
    author="Dinh",
    author_email="dinh@example.com",
    description="Sort description",
    long_description="Full description",
    long_description_content_type="text/markdown",
    url="https://github.com/juicyDD",
    #packages=setuptools.find_packages(),
    packages =setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)