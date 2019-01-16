"""

Project: farmhouse

File Name: shelvingunit

Author: Zachary Romer, romerzs14@gmail.com

Creation Date: 1/15/19

Version: 1.0

Purpose: provide classes which represent the components of a shelving unit being used for hydroponics

Special Notes:

"""

import logging

from .exceptions import *

log = logging.getLogger('farmhouse.logger')

class BaseTray:

    def __init__(self, width, length, height, volume=0, layout=None):
        """

        Args:
            width: [float] width of tray in inches
            length: [float] length of tray in inches
            height: [float] height of tray in inches
            layout: [BaseLayout] map representing layout of possible planting sights

        """
        self.width = width
        self.length = length
        self.height = height

        if not volume:
            self.volume = self.get_volume(self.width, self.length, self.height)

        self.layout = layout

    def get_volume(self, width, length, height):
        return width*length*height

class BaseShelvingUnit:

    def __int__(self, width, length, height, shelves=None):
        """

        Args:
            width: [float] width of shelving unit in inches
            length: [float] length of shelving unit in inches
            height: [float] height of shelving unit in inches
            shelves: [list] containing shelf objects


        """
        self.num_shelves = len(shelves)
        self.shelves = shelves

        self.width = width
        self.length = length
        self.height = height

    def remove_shelf(self, index):
        """

        Args:
            index: [int] specifying which shelf to remove.  Bottom shelf is considered index=0

        Returns:

        """
        try:
            del self.shelves[index]
            self.num_shelves = len(self.shelves)
        except KeyError:
            err_message = 'No shelf exists at index {}.  Remember that shelves are indexed starting at 0 counting from the bottom up'
            raise NonExistentTrayError


class BaseShelf:

    def __init__(self, tray):
        self.tray = tray


class TrayLayout:

    def __init__(self, num_plants, matrix):
        """ Holds a layout for a tray of plants.  The matrix is a list of vertically-oriented lists of netcup objects which
            describe what kind of plant they contain, their dimensions, and anything else found interesting.

        Args:
            num_plants:
            matrix:
        """

        self.num_plants = num_plants
        self.matrix = matrix


class MatrixFactory:

    def __init__(self):
        self.rows = []
        self.num_rows = 0

    def add_row(self, row, row_index):
        """

        Args:
            row: list[netcup] a list of netcup objects to add as a row
            row_index: the index at which the row was added.  Row indexing starts at 0 from the left

        """
        self.rows.insert(row_index, row)
        self.num_rows = len(self.rows)

    def remove_row(self, row_index):

        del self.rows[row_index]
        self.num_rows = len(self.rows)


    def remove_plant_from_row(self, row_index, plant_index):
        """ Remove a netcupped plant from a row at the row/plant specified index.  Plant indexing starts at 0, from the open / accessible
            side of shelving unit.

        Args:
            row_index: [int]
            plant_index: [int]

        """

        try:
            del self.rows[row_index][plant_index]
        except KeyError as ke:
            if str(row_index) in ke.args:
                err_msg = 'No row was found at row index {}.  Remember row indexing increments from 0 going left to right.'.format(row_index)
                raise NonExistentRowError(err_msg)
            elif str(plant_index) in ke.args:
                err_msg = 'No plant was found at plant index {}.  Remember that plant indexing increments from 0 going from front to back'.format(plant_index)
                raise NonExistentPlantError(err_msg)

class NetCupPlant:

    def __init__(self, diameter, depth, plant, media, num_seeds):
        """

        Args:
            diameter: [float] diameter of netcup
            depth: [float] depth of netcup
            plant: [PlantObj] type of plant placed in netcup
            media: [str] type of media used for plant
        """

        self.diameter = diameter
        self.depth = depth
        self.plant = plant
        self.media = media
        self.num_seeds = num_seeds

class Plant:

    def __init__(self, name, distance_from_light, latin_name='', roots_showing=False):
        self.name = name
        self.latin_name = latin_name
        self.roots_showing = roots_showing
        self.distance_from_light = distance_from_light

        if self.roots_showing:
            log.info('Roots began showing out bottom of netcup')



    def roots_showing(self):
        self.roots_showing = True
        log.info('Roots began showing out bottom of netcup')


    def adjust_distance_from_light(self, inches_changed):

        self.distance_from_light = self.distance_from_light - inches_changed
        if self.distance_from_light < 1:
            err_msg = 'Plant distance from light as measured from top of plant is less than 1 inch, which should not the case'
            raise TooLowLightError(err_msg)