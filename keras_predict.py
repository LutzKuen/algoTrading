import time
import datetime
from observer_keras import controller_cython as controller

cont = controller.Controller('/home/tubuntu/settings_triangle.conf', 'demo', verbose=1)
cont.get_latest_prediction()
