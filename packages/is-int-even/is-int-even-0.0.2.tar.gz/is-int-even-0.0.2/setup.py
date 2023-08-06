from setuptools import setup

README = ""
with open("README.md") as f:
    README = f.read()

setup(
    name="is-int-even",
    author="sifte",
    url="https://github.com/sifte/is-int-even",
    version="0.0.2",
    description="Is a number even?",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=["is_int_even"],
    include_package_data=True,
    license="MIT",
    maintainer="sifte",
    project_urls = {
        "Github": "https://github.com/sifte/is-int-even",
        },
    keywords="even number", 
)