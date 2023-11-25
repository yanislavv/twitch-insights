from setuptools import setup, find_packages

setup(
    name="twitch-insights",
    version="0.1",
    author="Yanislav Chanev",
    description="Twitch insights",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'extract=src.extract.twitch_chat_client:main'
        ],
    },
    install_requires=[
        'boto3==1.26.137',
        'botocore==1.29.137',
        'jmespath==1.0.1',
        'python-dateutil==2.8.2',
        's3transfer==0.6.1',
        'six==1.16.0',
        'urllib3==1.26.15'
    ],
    python_requires='>=3.8',
)