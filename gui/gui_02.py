# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs
import scriptcontext
import Rhino
import math
import Meier_UI_Utility
import System.Windows.Forms.DialogResult

def main():
    data = ChairData()
    ui = ChairUI(data)
    controller = FormController(ui)
    ui.ValueChangeCallback(data)
    result = Rhino.UI.Dialogs.ShowSemiModal(ui.form)
    if (result == System.Windows.Forms.DialogResult.OK):print "OK"
    else: print "Cancel"
    controller.AddCurveToDocument()

class ChairData(): #デフォルトのデータ値
    def __init__(self):
        self.thickness = 2
        self.depth = 16
        self.height = 16
        self.width = 16
        self.seat_height = 32

class ChairUI():
    def __init__(self, data):
        self.ValueChangeCallback = None
        self.data = data
        self.form = Meier_UI_Utility.UIForm('Chair maker')
        self.addControls()
        self.form.layoutControls()

    def SetValueChangedCallback(self, callback):
        self.ValueChangeCallback = callback

    def addControls(self):
        updnWidth = 80
        buttonWidth = 105

        p = self.form.panel

        p.addLabel('', 'Thickness:', None, False)
        p.addNumericUpDown('thickness', 1, 8, 1, 0, self.data.thickness, updnWidth, True, self.thickness_OnValueChange)

        p.addLabel('', 'Depth:', None, False)
        p.addNumericUpDown('depth', 1, 64, 1, 0, self.data.depth, updnWidth, True, self.depth_OnValueChange)

        p.addLabel('', 'Height:', None, False)
        p.addNumericUpDown('height', 1, 64, 1, 0, self.data.height, updnWidth, True, self.height_OnValueChange)

        p.addLabel('', 'Width:', None, False)
        p.addNumericUpDown('width', 1, 64, 1, 0, self.data.width, updnWidth, True, self.width_OnValueChange)

        p.addLabel('', 'Seat Height:', None, False)
        p.addNumericUpDown('seat_height', 1, 128, 1, 0, self.data.seat_height, updnWidth, True, self.seat_height_OnValueChange)

        p.addButton('OK', 'OK', buttonWidth, False, None)

    def thickness_OnValueChange(self, sender, e):
        self.data.thickness = sender.Value
        if self.ValueChangeCallback != None:
            self.ValueChangeCallback(self.data)

    def depth_OnValueChange(self, sender, e):
        self.data.depth = sender.Value
        if self.ValueChangeCallback != None:
            self.ValueChangeCallback(self.data)

    def height_OnValueChange(self, sender, e):
        self.data.height = sender.Value
        if self.ValueChangeCallback != None:
            self.ValueChangeCallback(self.data)

    def width_OnValueChange(self, sender, e):
        self.data.width = sender.Value
        if self.ValueChangeCallback != None:
            self.ValueChangeCallback(self.data)

    def seat_height_OnValueChange(self, sender, e):
        self.data.seat_height = sender.Value
        if self.ValueChangeCallback != None:
            self.ValueChangeCallback(self.data)

class FormController():
    def __init__(self, UI):
        self.box1 = None
        self.box2 = None
        self.box3 = None
        self.box4 = None
        self.boundingBox1 = None
        self.boundingBox2 = None
        self.boundingBox3 = None
        self.boundingBox4 = None
        self.data = UI.data
        UI.SetValueChangedCallback(self.UpdateGeometry)
        Rhino.Display.DisplayPipeline.CalculateBoundingBox += self.OnCalcBoundingBox
        Rhino.Display.DisplayPipeline.DrawForeground += self.OnDrawForeground
        UI.form.FormClosed += self.OnFormClosed

    def OnFormClosed(self, sender, e):
        Rhino.Display.DisplayPipeline.DrawForeground -= self.OnDrawForeground
        Rhino.Display.DisplayPipeline.CalculateBoundingBox -= self.OnCalcBoundingBox
        scriptcontext.doc.Views.Redraw()

    def OnDrawForeground(self, sender, e):
        boxColor = System.Drawing.Color.Red
        e.Display.DrawBox(self.box1, boxColor)
        e.Display.DrawBox(self.box2, boxColor)
        e.Display.DrawBox(self.box3, boxColor)
        e.Display.DrawBox(self.box4, boxColor)

    def OnCalcBoundingBox(self, sender, e):
        if self.boundingBox1 != None:
            e.IncludeBoundingBox(self.boundingBox1)
        if self.boundingBox2 != None:
            e.IncludeBoundingBox(self.boundingBox2)
        if self.boundingBox3 != None:
            e.IncludeBoundingBox(self.boundingBox3)
        if self.boundingBox4 != None:
            e.IncludeBoundingBox(self.boundingBox4)

    def UpdateGeometry(self, data):
        self.box1 = None
        self.box2 = None
        self.box3 = None
        self.box4 = None
        self.boundingBox1 = None
        self.boundingBox2 = None
        self.boundingBox3 = None
        self.boundingBox4 = None

        # Box 1
        bmin = Rhino.Geometry.Point3d(0, 0, 0)
        bmax = Rhino.Geometry.Point3d(data.thickness, data.depth, data.height)
        bbox = Rhino.Geometry.BoundingBox(bmin, bmax)
        self.box1 = Rhino.Geometry.Box(bbox)
        self.boundingBox1 = bbox

        # Box 2
        bmin = Rhino.Geometry.Point3d(data.width, 0, 0)
        bmax = Rhino.Geometry.Point3d(data.thickness + data.width, data.depth, data.height)
        bbox = Rhino.Geometry.BoundingBox(bmin, bmax)
        self.box2 = Rhino.Geometry.Box(bbox)
        self.boundingBox2 = bbox

        # Box 3
        bmin = Rhino.Geometry.Point3d(0, 0, data.height)
        bmax = Rhino.Geometry.Point3d(data.thickness + data.width, data.depth, data.thickness + data.height)
        bbox = Rhino.Geometry.BoundingBox(bmin, bmax)
        self.box3 = Rhino.Geometry.Box(bbox)
        self.boundingBox3 = bbox

        # Box 4
        bmin = Rhino.Geometry.Point3d(0, data.depth, 0)
        bmax = Rhino.Geometry.Point3d(data.thickness+data.width, data.thickness+data.depth, data.thickness+data.seat_height)
        bbox = Rhino.Geometry.BoundingBox(bmin, bmax)
        self.box4 = Rhino.Geometry.Box(bbox)
        self.boundingBox4 = bbox

        scriptcontext.doc.Views.Redraw()

    def AddCurveToDocument(self):
        pad = 5

        if self.box1:
            center_point = Rhino.Geometry.Point3d(-64, 64, 0)
            height_point = Rhino.Geometry.Point3d(-64, 64, 1)
            zaxis = height_point - center_point
            plane = Rhino.Geometry.Plane(center_point, zaxis)
            rect1 = Rhino.Geometry.Rectangle3d(plane, self.data.depth, self.data.height)
            scriptcontext.doc.Objects.AddRectangle(rect1)
            scriptcontext.doc.Objects.AddBox(self.box1)

        if self.box2:
            center_point = Rhino.Geometry.Point3d(-64+self.data.depth+pad, 64, 0)
            height_point = Rhino.Geometry.Point3d(-64+self.data.depth+pad, 64, 1)
            zaxis = height_point - center_point
            plane = Rhino.Geometry.Plane(center_point, zaxis)
            rect2 = Rhino.Geometry.Rectangle3d(plane, self.data.depth, self.data.height)
            scriptcontext.doc.Objects.AddRectangle(rect2)
            scriptcontext.doc.Objects.AddBox(self.box2)

        if self.box3:
            center_point = Rhino.Geometry.Point3d(-64+self.data.depth*2+pad*2, 64, 0)
            height_point = Rhino.Geometry.Point3d(-64+self.data.depth*2+pad*2, 64, 1)
            zaxis = height_point - center_point
            plane = Rhino.Geometry.Plane(center_point, zaxis)
            rect3 = Rhino.Geometry.Rectangle3d(plane, self.data.width, self.data.depth)
            scriptcontext.doc.Objects.AddRectangle(rect3)
            scriptcontext.doc.Objects.AddBox(self.box3)

        if self.box4:
            center_point = Rhino.Geometry.Point3d(-64+self.data.depth*2+pad*3+self.data.width, 64, 0)
            height_point = Rhino.Geometry.Point3d(-64+self.data.depth*2+pad*3+self.data.width, 64, 1)
            zaxis = height_point - center_point
            plane = Rhino.Geometry.Plane(center_point, zaxis)
            rect4 = Rhino.Geometry.Rectangle3d(plane, self.data.width, self.data.seat_height)
            scriptcontext.doc.Objects.AddRectangle(rect4)
            scriptcontext.doc.Objects.AddBox(self.box4)

        scriptcontext.doc.Views.Redraw()

        filter = "SBP File (*.sbp)|*.sbp||"
        filename = rs.SaveFileName("Save point coordinates as", filter)
        if filename == None: return

        with open(filename, 'w') as f:
            for i in range(4):
                pnt = rect1.Corner(i)
                f.write('M3,{0},{1},{2}\n'.format(pnt.X, pnt.Y, pnt.Z))

            for i in range(4):
                pnt = rect2.Corner(i)
                f.write('M3,{0},{1},{2}\n'.format(pnt.X, pnt.Y, pnt.Z))

            for i in range(4):
                pnt = rect3.Corner(i)
                f.write('M3,{0},{1},{2}\n'.format(pnt.X, pnt.Y, pnt.Z))

            for i in range(4):
                pnt = rect4.Corner(i)
                f.write('M3,{0},{1},{2}\n'.format(pnt.X, pnt.Y, pnt.Z))

if __name__ == '__main__':
    main()
