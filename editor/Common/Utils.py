import os
import yaml

os.chdir(os.path.dirname(os.path.realpath(__file__)))

LANGUAGES_PATH = os.path.join('languages')
THEMES_PATH = os.path.join('themes')

def parse_file(path=None):
    with open(path, 'r') as stream:
        try:
            return yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as error:
            print(error)
    return None

def parse_language_file(language='kotlin'):
    return parse_file(path=os.path.join(LANGUAGES_PATH, '{}.yml'.format(language)))

def parse_theme_file(theme='dracula'):
    return parse_file(path=os.path.join(THEMES_PATH, '{}.yml'.format(theme)))

FONT_FAMILY = 'Consolas'
FONT_SIZE_MAP = {
    'Small': 15,
    'Medium': 18,
    'Large': 20
}
FONT_SIZE_DEFAULT = 'Small'