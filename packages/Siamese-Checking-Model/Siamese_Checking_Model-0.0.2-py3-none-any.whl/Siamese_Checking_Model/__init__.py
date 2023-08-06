# -*- coding: utf-8 -*-

__author__ = """xalphonse"""
__email__ = 'xalphonse@gmail.com'
__version__ = '0.0.1'

from pkg_resources import resource_filename

def pose_predictor_model_location():
    return resource_filename(__name__, "models/shape_predictor_68_face_landmarks.dat")

