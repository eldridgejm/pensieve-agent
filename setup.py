from setuptools import setup, find_packages

setup(
    name='pensieve_repo_agent',
    version='0.3.0',
    py_modules=['pensieve_repo_agent'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            '_pensieve-repo-agent = pensieve_repo_agent:main'
        ]
    }
)

