import setuptools
import os
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def build(cpp_file,dest_dir):
    cmd="g++ -fPIC -shared -O3 -o {} -std=c++11 {}".format( dest_dir,cpp_file)
    os.system(cmd)

build("src/pi_compute/include/pi.cpp"," src/pi_compute/lib/lib_pi.so")

setuptools.setup(
    name="pi_compute",
    version="3.14.1",
    author="mathm",
    author_email="mingtinglai@58.com",
    description="to compute N digits of pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://igit.58corp.com/mingtinglai/pi",
    project_urls={
        "Bug Tracker": "https://igit.58corp.com/mingtinglai/pi/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    package_data={"pi_compute":["include","include/pi.cpp","lib","lib/lib_pi.so"]},
    packages=['pi_compute'],
    python_requires=">=3.6",
)
