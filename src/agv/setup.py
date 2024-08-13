from setuptools import setup

package_name = 'agv'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Syu Kato',
    maintainer_email='saba@todo.todo',
    description='AGV関連のパッケージ',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'agv_commander_node = agv.agv_commander_node:main',
            'agv1_node = agv.agv1_node:main',
            'agv2_node = agv.agv2_node:main',
            'agv3_node = agv.agv3_node:main'
        ],
    },
)

