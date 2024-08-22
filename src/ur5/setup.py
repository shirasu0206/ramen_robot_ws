from setuptools import setup

package_name = 'ur5'

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
    maintainer='syu',
    maintainer_email='saba@todo.todo',
    description='UR5関連のパッケージ',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ur5_noodle_node = ur5.ur5_noodle_node:main',
            'ur5_retouch_node = ur5.ur5_retouch_node:main',
            'ur5_pork_node = ur5.ur5_pork_node:main',
            'pork_image_node = ur5.pork_image_node:main'
        ],
    },
)

