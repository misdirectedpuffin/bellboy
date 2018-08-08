"""Package setup file"""
from setuptools import setup, find_packages

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements


def get_requirements(file):
    """Return a list of requirements from a file."""
    requirements = parse_requirements(file, session=False)
    return [str(ir.req) for ir in requirements if not None]


setup(
    name="trivago",
    version="0.1.0",
    author="Steven Carey",
    author_email="misdirectedpuffin@gmail.com",
    description="A data parsing tool",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'transformer=trivago.cli:entrypoint',
        ],
    },
    install_requires=get_requirements('requirements.txt'),
    tests_require=get_requirements('requirements_test.txt'),
    setup_requires=['pytest-runner'],
    classifiers=[
        'Programming Language :: Python :: 3.5',
    ],
    zip_safe=False,
    keywords='trivago, transformer'
)
