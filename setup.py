import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="login-jumper",
    version="1.5.5Beta",
    author="SunnyWalden",
    author_email="sunnywalden@gmail.com",
    description="Logging ecs automatic via jumper server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sunnywalden/login-jumper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pycrypto', 'paramiko', 'pexpect', 'sentry-sdk', 'rollbar', 'redis'],
    python_requires='>=2.7',
)