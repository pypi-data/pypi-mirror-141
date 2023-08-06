from setuptools import setup

setup(
    name='yaw-cli',
    description='Query weather via cli',
    author='dynamicfire',
    author_email='plus@plusnow.me',
    version='0.1.2',
    py_modules=['yaw'],
    install_requires=[
        'Click',
        'requests',
        'Path'
    ],
    license="MIT",
    entry_points={
        'console_scripts': [
            'yaw = yaw:main',
        ],
    },
)
