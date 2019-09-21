import setuptools

setuptools.setup(
    name="Hello World",
    options={
        'build_apps': {
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.egg',
                '**/*.bam',
            ],
            'console_apps': {'ModelsConfig': 'ModelsActorsExample.py'},
            'include_modules': [
                'DirectSession'
            ],
            'platforms': [
                'manylinux1_x86_64',
                'win_amd64',
            ],
            'plugins': [
                'pandagl',
                'pandadx9',
                'p3openal_audio'
            ]
        }
    }
)