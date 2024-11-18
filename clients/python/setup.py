from setuptools import setup, find_packages

setup(
    name="climate-monitor-client",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'psutil>=5.9.0'
    ],
    author="Climate System Team",
    author_email="team@climate-system.org",
    description="Client library for Climate System Monitor",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/climate-system-monitor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
