from setuptools import setup, find_packages

setup(
    name="pensieve_agent",
    version="2.1.0",
    py_modules=["pensieve_agent"],
    install_requires=[],
    entry_points={"console_scripts": ["_pensieve-agent = pensieve_agent:main"]},
)
