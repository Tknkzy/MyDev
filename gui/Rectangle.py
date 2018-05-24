# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs

class Rect:
    def __init__(self, plane, width, height):
        self.plane = plane
        self.width = width
        self.height = height
        rs.AddRectangle(plane, width, height)

if __name__ == '__main__':
    Rect()
