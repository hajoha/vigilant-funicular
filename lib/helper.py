import math, os, sys, yaml, datetime
from scipy.interpolate import CubicSpline
import pickle
import numpy as np

dev = False

def set_dev(mode):
    global dev
    dev = mode

def sign(x):
    return (x > 0) - (x < 0)


def record_collision_points(p1, p2, scale_factor, screen, fn):
                    
                    cs = CubicSpline(p1, p2)
                    x_fit = [math.ceil(x) for x in np.linspace(0, 320 *scale_factor, 320 *scale_factor)]
                    y_fit = [math.ceil(x) for x in cs(x_fit)]
                    
                    print('recorded data points: ', p1, p2)

                    for x, y in zip(x_fit, y_fit):
                        screen.set_at((x, y), "red")
                        
                    with open((fn), "wb") as fp:
                        pickle.dump(y_fit, fp)
                        print('saved collision y coords to: ', fn)


def path(*args):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    if len(args) == 1:
        if '/tmp/' not in args[0]:
            relative_path = os.path.join(*args[0].split('/'))
        else:
            # we probably mistakenly called path on a path object
            return args[0]
    else:
        relative_path = os.path.join(*args)
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = ''
    #print('got: ', args[0], 'returning path : ', os.path.join(base_path, relative_path))
    return os.path.join(base_path, relative_path)


#def scale_rect(rect, scale_factor):

def load_config():
     
    # running on windows
    if 'APPDATA' in os.environ:
        confighome = os.environ['APPDATA']
    # running on unix supporting XDG CONFIG
    elif 'XDG_CONFIG_HOME' in os.environ:
        confighome = os.environ['XDG_CONFIG_HOME']
    # just put it in home
    else:
        confighome = os.path.join(os.environ['HOME'], '.config')
    
    configfile = os.path.join(confighome, 'vigilant', 'config.yaml')

    if os.path.isfile(configfile):
        with open(configfile, 'r') as file:
            config = yaml.safe_load(file)
        
        if not config:
             print("Found config file but the file is empty.")
         
        return config
        
    else:
        os.makedirs(os.path.dirname(configfile), exist_ok=True)
        with open(configfile, 'w'): pass

        return {}


def save_config(config):

    if not config:
         config = {}
    
    config['date'] = str(datetime.datetime.now())
    # running on windows
    if 'APPDATA' in os.environ:
        confighome = os.environ['APPDATA']
    # running on unix supporting XDG CONFIG
    elif 'XDG_CONFIG_HOME' in os.environ:
        confighome = os.environ['XDG_CONFIG_HOME']
    # just put it in home
    else:
        confighome = os.path.join(os.environ['HOME'], '.config')
    
    configfile = os.path.join(confighome, 'vigilant', 'config.yaml')

    with open(configfile, 'a') as file:
        yaml.dump(config, file)

    print('saved config to file: ', configfile)
         