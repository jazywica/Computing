# -*- encoding: utf-8 -*-
""" Cookie Clicker Simulator Build Information """
# http://www.codeskulptor.org/#poc_clicker_provided.py

BUILD_GROWTH = 1.15

class BuildInfo:
    """ Class to track build information. """
    def __init__(self, build_info=None, growth_factor=BUILD_GROWTH):
        self._build_growth = growth_factor
        if build_info == None: # Case 1: the 'Built_info' object comes with no declared bonus list ex: b = BuildInfo()
            self._info = {"Cursor": [15.0, 0.1], # this is the initial cost and the extra growth per second that it brings: [15.0, 0.1]
                          "Grandma": [100.0, 0.5],
                          "Farm": [500.0, 4.0],
                          "Factory": [3000.0, 10.0],
                          "Mine": [10000.0, 40.0],
                          "Shipment": [40000.0, 100.0],
                          "Alchemy Lab": [200000.0, 400.0],
                          "Portal": [1666666.0, 6666.0],
                          "Time Machine": [123456789.0, 98765.0],
                          "Antimatter Condenser": [3999999999.0, 999999.0]}
        else: # Case 2: the 'Built_info' class for any reason comes with a predefined bonus list: b = BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15)
            self._info = {}
            for key, value in build_info.items():
                self._info[key] = list(value)

        self._items = sorted(self._info.keys()) # Produces a sorted list of keys: ['Alchemy Lab', 'Antimatter Condenser', 'Cursor', 'Factory', 'Farm', 'Grandma', 'Mine', 'Portal', 'Shipment', 'Time Machine']

    def build_items(self):
        """ Get a list of buildable items """
        return list(self._items)

    def get_cost(self, item):
        """ Get the current cost of an item Will throw a KeyError exception if item is not in the build info. """
        return self._info[item][0]

    def get_cps(self, item):
        """ Get the current CPS of an item. Will throw a KeyError exception if item is not in the build info. """
        return self._info[item][1]

    def update_item(self, item):
        """ Update the cost of an item by the growth factor. Will throw a KeyError exception if item is not in the build info. """
        cost, cps = self._info[item]
        self._info[item] = [cost * self._build_growth, cps] # here we update the cost of buying another item (we do it after we buy something in the 'simulate_clicker' procedure)

    def clone(self):
        """ Return a clone of this BuildInfo """
        return BuildInfo(self._info, self._build_growth)
