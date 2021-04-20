from setuptools import setup, find_packages
setup(
    name="po",
    version="0.0.1",
    author="james bradbury",
    packages=find_packages(),
    install_requires=['rich', 'click'],
    entry_points={
        'console_scripts': [
            'po = po.po:cli',
        ],
    },
)
