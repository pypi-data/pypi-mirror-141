from setuptools import setup, find_packages

# Set up the package metadata
setup(
    author="Jamie O'Brien",
    description="A package with functions for reading/writing different file types from/to AWS s3 storage.",
    name="s3_connection",
    version="0.1.0",
    packages=find_packages(include=["s3_connection", "s3_connection.*"]),
    install_requires=[
        'boto3==1.17.13', 
        'numpy', 
        'pandas', 
        'regex', 
        'requests', 
        's3fs==0.5.2', 
        's3transfer==0.3.4', 
        'tensorflow', 
        'tensorflow-estimator', 
        'python-dotenv==0.19.2'
        ]
)