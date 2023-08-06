from setuptools import find_packages, setup

project = "hybrid_pool_executor"


def get_readme():
    with open("README.rst", "r") as fd:
        return fd.read()


def get_version():
    return __import__(project).__version__


install_requires = []
tests_require = [
    "black",
    "coverage>=5.3",
    "flake8",
    "isort>=5.0.0",
    "pytest>=6.2.5",
    "pytest-asyncio",
    "pytest-cov",
    "pytest-timeout",
]
dev_require = tests_require + [
    "tox",
    "twine",
]
extras_require = {
    "test": tests_require,
    "dev": dev_require,
}

setup_kwargs = dict(
    name=project,
    version=get_version(),
    platforms="any",
    license="MIT",
    python_requires=">=3.8",
    description="Pool executor supporting thread, process and async.",
    long_description=get_readme(),
    long_description_content_type="text/x-rst",
    author="Leavers",
    author_email="leavers930@gmail.com",
    url="https://github.com/leavers/hybrid-pool-executor",
    py_modules=[project],
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

setup(**setup_kwargs)
