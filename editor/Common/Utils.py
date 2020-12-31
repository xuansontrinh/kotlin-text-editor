import os
import tkinter as tk
import yaml

from PIL import Image, ImageTk

os.chdir(os.path.dirname(os.path.realpath(__file__)))

LANGUAGES_PATH = os.path.join('languages')
THEMES_PATH = os.path.join('themes')
ICONS_PATH = os.path.join('resources')

FONT_FAMILY = 'Consolas'
FONT_SIZE_MAP = {
    'Small': 15,
    'Medium': 18,
    'Large': 20
}
FONT_SIZE_DEFAULT = 'Small'

FILE_NAME = "tmp"

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

def get_icon(name):
    image = tk.PhotoImage(file=os.path.join(ICONS_PATH, '{}.png'.format(name)))
    # image = image.subsample(2) 
    
    # image = Image.open(os.path.join(ICONS_PATH, '{}.png'.format(name)))
    # image = image.resize((5, 5), Image.ANTIALIAS)
    return image
