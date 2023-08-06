from setuptools import setup

def local_scheme(version):
    return ""

setup(
    name="ci_cd_elham",
    author="Elham Amin",  # TODO: Write your name    
    use_scm_version={"local_scheme": local_scheme},
    setup_requires=['setuptools_scm'],
    packages=["dictionary"],
    install_requires=[
        "requests>=2.23.0",
    ],
    python_requires=">=3.8",

)
