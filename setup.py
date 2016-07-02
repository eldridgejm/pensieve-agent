from setuptools import setup, find_packages

setup(
    name='pensieve_repo_agent',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'pensieve-repo-agent = pensieve_repo_agent:main'
        ]
    }
)

