# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs
import scriptcontext
import Rhino
from .lib.EmotiveModeler-CAD-tool import Meier_UI_Utility # This is the module with the UI creation code
import System.Windows.Forms.DialogResult
import Rectangle

def Main(): #UIオブジェクトの表示
    data = Rectangle.Rect(rs.WorldXYPlane(), 20, 20)
    ui = RectUI(data)
    controller = FormController(ui)
    result = Rhino.UI.Dialogs.ShowSemiModal(ui.form)
    if (result == System.Windows.Forms.DialogResult.OK):print "OK"
    else: print "Cancel"
    controller.AddCurveToDocument()

class RectData(): #UIの初期値を設定
    def __init__(self):
        self.width = 10.0
        self.height = 10.0

class RectUI(): #UI変数を作成して管理するクラス
    def __init__(self, data):
        self.ValueChangeCallback = None
        self.data = data
        self.form = Meier_UI_Utility.UIForm("Rect UI Example") #新しいフォームを作成
        self.addControls()
        self.form.layoutControls() #フォームにコントロールをレイアウト

    def SetValueChangedCallback(self, callback):
        self.ValueChangeCallback = callback

    def addControls(self):
        updnWidth = 80
        buttonWidth = 105

        p = self.form.panel

        p.addLabel('', 'Width:', None, False)
        p.addNumericUpDown('width', 1, 100, 1, 0, self.data.width, updnWidth, True, self.width_OnValueChange)

        p.addLabel('', 'Height:', None, False)
        p.addNumericUpDown('height', 1, 100, 1, 0, self.data.height, updnWidth, True, self.height_OnValueChange)

        p.addButton('OK', 'OK', buttonWidth, False, None)
        p.addButton('Cancel', 'Cancel', buttonWidth, False, None)

    def width_OnValueChange(self, sender, e):
        self.data.width = sender.Value
        if self.ValueChangeCallback != None:
            self.ValueChangeCallback(self.data)

    def height_OnValueChange(self, sender, e):
        self.data.height = sender.Value
        if self.ValueChangeCallback != None:
            self.ValueChangeCallback(self.data)

class FormController():
    def __init__(self, UI):
        self.rect1 = None
        self.data = UI.data
        UI.SetValueChangedCallback(self.UpdateGeometry)
        Rhino.Display.DisplayPipeline.DrawForeground += self.OnDrawForeground

    def OnDrawForeground(self, sender, e):
        boxColor = System.Drawing.Color.Red
        e.Display.DrawBox(self.rect1, boxColor)

    def UpdateGeometry(self, data):
        self.rect1 = None

        bmin = Rhino.Geometry.Point3d(0, 0, 0)
        bmax = Rhino.Geometry.Point3d(data.width, data.height, 0)
        brect = Rhino.Geometry.BoundingBox(bmin, bmax)
        self.rect1 = Rhino.Geometry.Box(brect)

        scriptcontext.doc.Views.Redraw()

    def AddCurveToDocument(self):
        if self.rect1:
            zaxis = Rhino.Geometry.Vector3d(0, 0, 1)
            center_point = Rhino.Geometry.Point3d(0, 0, 0)
            plane = Rhino.Geometry.Plane(center_point, zaxis)
            rect2 = Rhino.Geometry.Rectangle3d(plane, self.data.width, self.data.height)
            scriptcontext.doc.Objects.AddRectangle(rect2)
            scriptcontext.doc.Objects.AddBox(self.rect1)

        scriptcontext.doc.Views.Redraw()

#Execute it...
if(__name__ == "__main__"):
    Main()
