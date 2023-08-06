# prior to this, 
# please install plantfem
import os
import sys

sys.path.append(os.pardir)

from .python.SoybeanClass.SoybeanClass import Soybean
from .python.LightClass.LightClass import Light

class plantfem:

    # create a Light object
    def Light(self,config):
        return Light(light_angle=90.0,light_direction=180.0)

    # create a Soybean object
    def Soybean(self,config):
        return Soybean(config)


