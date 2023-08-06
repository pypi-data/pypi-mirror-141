import setuptools

VERSION = '0.0.5'
DESCRIPTION = "A common utils package used by the Atomic Loops Team"

setuptools.setup(
    name = "atomicloops_utils",
    version = "0.0.5",
    author = "Atomic Loops",
    description= "Utils package for common operations used by Atomic Loops in projects",
    packages = setuptools.find_packages(),
    install_requires = [] 
)