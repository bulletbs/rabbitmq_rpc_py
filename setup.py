from setuptools import setup, find_packages

setup(
    name="rabbitmq_rpc_py",
    version="0.1.0",
    description="Asynchronous RPC library using RabbitMQ and aio-pika",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Oleksandr K.",  # Replace with your name
    author_email="bulletua@gmail.com",  # Replace with your email
    url="https://github.com/bulletbs/rabbitmq_rpc_py",  # Replace with your repo URL
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "aio-pika>=9.0.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
)