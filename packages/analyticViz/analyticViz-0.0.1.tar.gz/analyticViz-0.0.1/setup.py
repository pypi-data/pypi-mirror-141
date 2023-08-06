import setuptools

with open("README.md", 'r', encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name = 'analyticViz',
      version = '0.0.1',
      author = 'David Adarkwah',
      author_email = 'davidwyse48@gmail.com',
      description = 'Package for data visualization',
      package = ['analyticViz'],
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      package_dir={"": "src"},
      packages=setuptools.find_packages(where="src"),
      python_requires='>=3.6',
      keywords = ['plotly', 'analysis', 'visualization', 'data analysis', 'data science']
      )




