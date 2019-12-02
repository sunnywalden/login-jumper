import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="login_jumper",
    version="1.5.6Alpha8",
    author="SunnyWalden",
    author_email="sunnywalden@gmail.com",
    description="Logging ecs automatic via jumper server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sunnywalden/login-jumper",
    packages=setuptools.find_packages(),
    package_data={'': ['config.ini', 'redis.ini']},
    include_package_data=True,
    data_files=[
        (
            'login_jumper/conf/',
            ['login_jumper/conf/config.ini', 'login_jumper/conf/redis.ini']),
        (
            'logs/.gitfile',
            ['login_jumper/logs/.gitfile']
        )
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    entry_points={
        'console_scripts': [
            'jmp = login_jumper.cli:main',
        ]
    },
    platforms="any",
    install_requires=['pycrypto', 'paramiko', 'pexpect', 'sentry-sdk', 'rollbar', 'redis'],
    python_requires='>=2.7',
)