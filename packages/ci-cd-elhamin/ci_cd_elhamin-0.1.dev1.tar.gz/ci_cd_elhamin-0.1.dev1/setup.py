from setuptools import setup

def local_scheme(version):
    return ""

setup(
    name="ci_cd_elhamin",
    author="Elham Amin",    
    use_scm_version={"local_scheme": local_scheme},
    setup_requires=['setuptools_scm'],
    packages=["dictionary"],
    install_requires=[
        "requests>=2.23.0",
    ],
    python_requires=">=3.8",

)
