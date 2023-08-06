from setuptools import setup


def readfile(filename):
    with open(filename, 'r+') as f:
        return f.read()


setup(
    name="index-renamer",
    version="0.0.3",
    description="Recursively rename index to its parent folder",
    long_description=readfile('README.md'),
    author="William Wigemo",
    author_email="william.wigemo@outlook.com",
    url="",
    py_modules=['index-renamer'],
    license=readfile('LICENSE'),
    entry_points={
        'console_scripts': [
            'index-renamer = __main__:main'
        ]
    },
)