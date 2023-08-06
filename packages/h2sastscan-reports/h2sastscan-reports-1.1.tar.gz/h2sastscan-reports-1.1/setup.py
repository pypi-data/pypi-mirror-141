import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="h2sastscan-reports",
    version="1.1",
    author="H2 Security",
    author_email="blue-team@h2security.io",
    description="A library for creating beautiful HTML reports from H2-sastscan results. SARIF and Grafeas formats are supported..",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/hhammoudi/h2sastscan-reports",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["Jinja2"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Utilities",
        "Topic :: Security",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
