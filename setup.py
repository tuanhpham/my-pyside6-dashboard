from setuptools import setup, find_packages

setup(
    name="my-pyside6-dashboard",  # Name of your package
    version="0.1.0",              # Initial version
    description="A PySide6 dashboard with various UI components",
    author="Your Name",           # Your name or the organization
    author_email="youremail@example.com",  # Your email
    url="https://github.com/tuanhpham/my-pyside6-dashboard.git",  # URL to your project
    packages=find_packages(where="src"),  # Automatically discover all packages under 'src'
    package_dir={"": "src"},      # Specify 'src' as the root for your package directories
    install_requires=[           # List your project's dependencies here
        "PySide6",                # Add any dependencies here
        "pytest",                 # Optional: add for testing
    ],
    classifiers=[                # Additional classifiers for Python Package Index (PyPI)
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",     # Define the supported Python version(s)
    include_package_data=True,   # Include non-Python files listed in MANIFEST.in
    long_description=open("README.md").read(),  # Read the long description from the README file
    long_description_content_type="text/markdown",  # Specify the format of the long description
)
