import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="login-jumper", # Replace with your own username
    version="1.5.1",
    author="SunnyWalden",
    author_email="sunnywalden@gmail.com",
    description="Logging ecs automatic via jumper server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sunnywalden/login_jump",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)