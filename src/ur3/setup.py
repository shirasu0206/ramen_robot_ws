from setuptools import setup
from glob import glob
import os

package_name = 'ur3'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml'])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='saba',
    maintainer_email='saba@com',
    description='UR3関連のノード',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ur3_negi_node = ur3.ur3_negi_node:main',
            'ur3_soup_node = ur3.ur3_soup_node:main',
            'ur3_retouch_node = ur3.ur3_retouch_node:main',
            'hello_node = ur3.hello_node:main',
            'depth_anything_node = ur3.depth_anything_node:main',   
        ],
    },
)

