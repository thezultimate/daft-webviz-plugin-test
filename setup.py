from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

TESTS_REQUIRE = ["selenium~=3.141", "pylint", "mock", "black", "bandit"]

setup(
    name="daft_webviz_plugin_test",
    description="A webviz plugin test",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Dafferianto Trinugroho",
    packages=find_packages(exclude=["tests"]),
    entry_points={
        "webviz_config_plugins": [
            "SomeCustomPlugin = daft_webviz_plugin_test.plugins:SomeCustomPlugin",
            "SomeOtherCustomPlugin = daft_webviz_plugin_test.plugins:SomeOtherCustomPlugin",
        ]
    },
    install_requires=[
        "webviz-config>=0.1.0",
    ],
    tests_require=TESTS_REQUIRE,
    extras_require={"tests": TESTS_REQUIRE},
    setup_requires=["setuptools_scm~=3.2"],
    python_requires="~=3.6",
    use_scm_version=True,
    zip_safe=False,
    classifiers=[
        "Natural Language :: English",
        "Environment :: Web Environment",
        "Framework :: Dash",
        "Framework :: Flask",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
