import setuptools

with open("README.md", "r") as fh:
     long_description = fh.read()

setuptools.setup(
     name="simplefetch", 
     version="0.0.1",
     author="Ercin TORUN",
     author_email="ercintorun@gmail.com",
     description="Simplified Paramiko Library to Fetch Data From MultiVendor Network Devices",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/ercintorun/simplefetch",
 packages=setuptools.find_packages(),
     classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 python_requires='>=3.6',
)
