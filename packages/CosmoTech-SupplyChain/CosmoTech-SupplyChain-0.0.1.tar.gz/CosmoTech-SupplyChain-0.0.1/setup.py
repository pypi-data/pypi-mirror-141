import setuptools

setuptools.setup(
    name='CosmoTech-SupplyChain',
    version='0.0.1',
    author='Alexis Fossart',
    author_email='alexis.fossart@cosmotech.com',
    url='https://github.com/Cosmo-Tech/supplychain-python-library',
    license='MIT',
    packages=setuptools.find_packages(),
    description='A support package for SupplyChain',
    install_requires=[
        "azure-core",
        "azure-digitaltwins-core",
        "azure-identity",
        "azure-kusto-data",
        "azure-kusto-ingest",
        "azure-storage-queue",
        "azure-storage-blob",
        "cma",
        "jsonschema",
        "numpy",
        "openpyxl",
        "pandas",
        "python-dateutil",
        "pytest"
    ]
)
