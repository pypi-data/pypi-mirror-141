"""
py setup.py sdist
twine upload dist/expressmoney-5.0.8.tar.gz
"""
import setuptools

setuptools.setup(
    name='expressmoney',
    packages=setuptools.find_packages(),
    version='5.0.8',
    description='SDK ExpressMoney',
    author='Development team',
    author_email='dev@expressmoney.com',
    install_requires=('requests', 'google-cloud-secret-manager', 'google-cloud-error-reporting', 'google-cloud-tasks',
                      ),
    python_requires='>=3.7',
)
