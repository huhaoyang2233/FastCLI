from setuptools import setup, find_packages

setup(
    name="my-api-cli",
    version="1.0.0",
    description="由 FastAPI 自动生成的 CLI 工具",
    author="Your Name",
    author_email="your.email@example.com",
    py_modules=["cli"],
    install_requires=[
        'typer>=0.9.0',
        'requests>=2.31.0',
        'rich>=13.7.0',
    ],
    entry_points={
        'console_scripts': [
            "mytool=cli:main",
        ],
    },
)