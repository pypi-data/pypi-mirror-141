from setuptools import setup, find_packages  # type: ignore


VERSION = "0.0.1"

# Send to pypi
# python3 setup.py sdist bdist_wheel
# twine upload dist/*

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="modulesync",
    version=VERSION,
    author="Kipling Crossing",
    author_email="kip.crossing@gmail.com",
    description="For syncing same modules in different locations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KipCrossing/modulesync",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[],
    entry_points={"console_scripts": ["modulesync = modulesync.__main__:main"]},
    license_files=("LICENSE",),
    # cmdclass={"egg_info": egg_info_ex},
)
