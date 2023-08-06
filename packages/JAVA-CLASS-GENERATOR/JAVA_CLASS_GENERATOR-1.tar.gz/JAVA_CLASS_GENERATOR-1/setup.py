from setuptools import setup


def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
        return long_description


setup(
    name='JAVA_CLASS_GENERATOR',
    version='1',
    packages=['JAVA_CLASS_GENERATOR'],
    url='https://github.com/DigitalCreativeApkDev/JAVA_CLASS_GENERATOR',
    license='MIT',
    author='DigitalCreativeApkDev',
    author_email='digitalcreativeapkdev2022@gmail.com',
    description='This package contains implementation of the application "Java Class Generator". This application '
                'allows users to reduce the effort needed to write Java classes.',
    long_description=readme(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
    entry_points={
        "console_scripts": [
            "JAVA_CLASS_GENERATOR=JAVA_CLASS_GENERATOR.java_class_generator:main",
        ]
    }
)