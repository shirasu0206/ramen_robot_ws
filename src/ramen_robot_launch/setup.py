from setuptools import setup

package_name = 'ramen_robot_launch'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/ramen_robot_launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='saba',
    maintainer_email='saba@todo.todo',
    description='Launch file',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [],
    },
)

