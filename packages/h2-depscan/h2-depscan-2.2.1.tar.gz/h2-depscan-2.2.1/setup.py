import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="h2-depscan",
    version="2.2.1",
    author="h2 security",
    author_email="blue-team@h2security.io",
    description="Security assessment for project dependencies that is entirely open-source and based on known vulnerabilities and advisories.",
    entry_points={
        "console_scripts": ["scan=depscan.cli:main", "depscan=depscan.cli:main"]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/hhammoudi/h2-depscan",
    packages=["depscan", "depscan.lib", "vendor"],
    include_package_data=True,
    install_requires=["h2-vulnerability-db", "defusedxml", "PyYAML", "rich"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Utilities",
        "Topic :: Security",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
