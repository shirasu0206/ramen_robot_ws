from setuptools import find_packages, setup

package_name = 'accountant'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='saba',
    maintainer_email='saba@todo.todo',
    description='accounting for ramen',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'accountant_node = accountant.accountant_node:main'
        ],
    },
)
