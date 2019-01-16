"""

Project: farmhouse

File Name: exceptions

Author: Zachary Romer, zach@scharp.org

Creation Date: 1/15/19

Version: 1.0

Purpose:

Special Notes:

"""


class NonExistentTrayError(Exception):
    pass



class NonExistentRowError(Exception):
    pass


class NonExistentPlantError(Exception):
    pass


class TooLowLightError(Exception):
    pass