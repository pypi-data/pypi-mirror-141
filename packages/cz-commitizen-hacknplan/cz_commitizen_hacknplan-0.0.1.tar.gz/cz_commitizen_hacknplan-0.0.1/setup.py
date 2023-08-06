from setuptools import setup


setup(
    name="cz_commitizen_hacknplan",
    version="0.0.1",
    py_modules=["cz_commitizen_hacknplan"],
    author='Nigel George',
    author_email='nigel.george@shiroikuma.co.uk',
    url='https://github.com/CanisHelix/commitizen_hacknplan',
    license="MIT",
    long_description="A variation of conventional commits with HackNPlan Tasks.",
    install_requires=["commitizen"],
)