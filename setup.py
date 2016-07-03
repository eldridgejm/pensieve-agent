from setuptools import setup, find_packages

setup(
    name='pensieve_repo_agent',
    version='0.1.0',
    py_modules=['pensieve_repo_agent'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'pensieve-repo-agent = pensieve_repo_agent:main'
        ]
    }
)

