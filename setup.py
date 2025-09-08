from setuptools import setup, find_packages

setup(
    name="novel_toy_tools",
    version="1.0",
    description="Various tools for the Novel Toy Study",
    author="Tom Endejan",
    author_email="tom.endejan@gmail.com",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'generate-renditions=novel_toy_tools.utils.generate_renditions:cli_main',
            'generate-stochastic-renditions=novel_toy_tools.scripts.generate_stochastic_renditions:main',
            'grab-csvs=novel_toy_tools.scripts.grab_csvs:main',
            'viewer3d-reliability=novel_toy_tools.scripts.Viewer3dReliability:main',
        ],
    },
    install_requires=[
        'polars',
        'scipy',
        'tqdm',
        'opencv-python',
        'pygame',
        'PyOpenGL',
        'PyOpenGL-accelerate',
        'moderngl',
        'moderngl-window',
        'numpy',
        'Pillow',
    ],
)