import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="barium-meal",
    version="0.0.17b0",
    author="Peckham Data Centre",
    author_email="chris@peckhamdata.com",
    description="Convenience wrapper for OpenTelemetry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/peckhamdata/barium-meal",
    packages=['barium_meal'],
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pytest",
        "requests-mock",
        "flask",
        "opentelemetry-exporter-jaeger==0.17b0",
        "opentelemetry-api==0.17b0",
        "opentelemetry-instrumentation-requests==0.17b0",
        "opentelemetry-instrumentation-boto==0.17b0",
        "opentelemetry-instrumentation-flask==0.17b0"
    ]
)
