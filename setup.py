from setuptools import find_packages, setup

setup(
    name="graphql_codegen",
    version="1.0.0",
    description="GraphQL codegen with Client.",
    url="",
    author="Valeriy Menshikov",
    author_email="",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "sgqlc",
        "structlog",
        "click",
        "pystache",
        "inflection",
    ],
    entry_points="""
            [console_scripts]
            graphql_codegen=graphql_codegen.cli:main
    """,
    keywords=["graphql_codegen"],
)
