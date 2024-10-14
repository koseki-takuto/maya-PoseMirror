# -*- coding: utf-8 -*-
import maya.cmds as cmds
from maya.common.ui import LayoutManager


class Main:
    def __init__(self, *args) :
        self.Poses = []
        self.SetList = []
        self.noLockAttr = []
        self.setAttr = []
        self.getAttr = []
        self.CheckedList = []
        self.ListValue = []
        self.PoseList = []
        self.NoLockList = []
        self.AttrCount = []
        self.AttrToggleCheckList = []
        self.SetToggleCheckLiset = []
        self.PoseFrame = []
        self.Mirror = False
        self.MirrorCheck = False
        self.SetCheck = False
        self.optionmenu = "YZ"
        self.AttrToggle = ["TX", "TY", "TZ", "RX", "RY", "RZ", "SX", "SY", "SZ"]
        self.AttrCheck = ["",".translateX", ".translateY", ".translateZ",\
                            ".rotateX", ".rotateY", ".rotateZ",\
                            ".scaleX", ".scaleY", ".scaleZ",]


    def GetPose(self, *args):
        #CheckedListの中身を初期化
        self.CheckedList.clear()
        #選択したオブジェクトを取得
        self.Objects = cmds.ls(sl = True)
        self.Frame = cmds.currentTime(q = True)
        if len(self.Objects):
            #選択したオブジェクトのアトリビュートの取得とそのロックの状態をチェック
            self.CheckedList = self.LockCheck(self.Objects)
            #アトリビュートを選択ごとにリスト化
            self.PoseList.append(self.CheckedList.copy())
            #ロックされていないアトリビュートのリストの番号を取得
            self.AttrCheckList = self.GetSetList(self.CheckedList)
            self.NoLockList.append(self.AttrCheckList.copy())
            self.Poses.append(self.Objects)
            self.PoseFrame.append(self.Frame)
            self.ListRefresh()
        else:
            print("オブジェクトを選択してください")


    def SetPose(self, *args):
        if cmds.textScrollList('PoseScrollList', q = True, selectIndexedItem = True) == None:
            print("リストを選択してください")
        else:
            #textScrollListの何番目を選んでいるか取得 listの数と一致させるため-1している
            SelectIndex = int(cmds.textScrollList('PoseScrollList', q = True, selectIndexedItem = True)[0]) - 1
            #textfieldの文字を取得
            self.UpperText = cmds.textField("UpperTextField", q = True, text = True)
            self.LowerText = cmds.textField("LowerTextField", q = True, text = True)
            self.MirrorOptionTextField = cmds.textField("MirrotoptionTextField", q = True, text = True)
            #チェックボックスの状態の確認
            StateofMirrorCheckBox = cmds.checkBox("MirrorOptionCheck", q = True, value = True)
            StateofSetCheckBox = cmds.checkBox("SetOption", q = True, value = True)
            #Mirrorがオフの場合
            if self.Mirror == False:        
                #PoseListには最初にオブジェクト名,そのあとにアトリビュート情報tx,ty,tz,rx,ry,rz,sx,sy,szが入っている
                #self.PoseList[ textscrolllistの何番目かを決める階層 [ オブジェクトごとに分ける階層 [ オブジェクト情報 ] ] ]
                #オブジェクトの個数分繰り返す
                for SetV in range(len(self.PoseList[SelectIndex])):
                    #ロックされていないアトリビュートの分だけ繰り返す
                    for SetA in range(len(self.NoLockList[SelectIndex][SetV])):
                        #Setoptionのチェックボックスがオンの場合
                        if StateofSetCheckBox == True:
                            #SetToggleCheckLisetにオンになっているボタンのアトリビュートが入っている
                            if self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]] in self.SetToggleCheckLiset:
                                #オブジェクト名 + アトリビュート名 , 数値
                                cmds.setAttr(self.PoseList[SelectIndex][SetV][0] + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                            self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]])
                        #Setoptionのチェックボックスがオフの場合
                        else:
                            cmds.setAttr(self.PoseList[SelectIndex][SetV][0] + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                        self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]])
            #Uppertextが空の場合
            elif self.Mirror == True and len(self.UpperText) == 0:
                print("上のテキストボックスにコントローラーの識別(例 _R)を入力してください")
            #Lowertextが空の場合
            elif self.Mirror == True and len(self.LowerText) == 0:
                print("下のテキストボックスにコントローラーの識別(例 _L)を入力してください")
            #Upper Lower どちらも空の場合
            elif self.Mirror == True and len(self.UpperText) == 0 and len(self.LowerText) == 0:
                print("上下のテキストボックスにコントローラーの識別(例 _R)を入力してください")
            #Mirrorがオンの場合
            else:
                for SetV in range(len(self.PoseList[SelectIndex])):
                    #ロックされていないアトリビュートの分だけ繰り返す
                    for SetA in range(len(self.NoLockList[SelectIndex][SetV])):
                        #Setoptionのチェックボックスがオンの場合
                        if StateofSetCheckBox == True:
                            #SetToggleCheckLisetにオンになっているボタンのアトリビュートが入っている
                            #セットするオブジェクトのアトリビュートとセットオプションのアトリビュートが一致したらセットする
                            if self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]] in self.SetToggleCheckLiset:
                                if self.UpperText in self.PoseList[SelectIndex][SetV][0]:
                                    cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.UpperText, self.LowerText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                                self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]])
                                elif self.LowerText in self.PoseList[SelectIndex][SetV][0]:
                                    cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.LowerText, self.UpperText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                                self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]])
                        #MirrorオプションのチェックボックスがオンでSetoptionのチェックボックスもオンの場合
                        elif StateofMirrorCheckBox == True and StateofSetCheckBox == True:
                            #オブジェクト名の置き換え　上のテキストフィールドに入っている文字と 例 _R と一致したらその文字と 下のテキストフィールドの文字と入れ替える   
                            #'該当させたい文字列'x in 検索したい文字列の入ったリストy   xがyの中にあるとTrue
                            if self.UpperText in self.PoseList[SelectIndex][SetV][0]:
                                #MirrorOptionTextFieldに何も入力されていないとき
                                if len(self.MirrorOptionTextField) == 0:
                                    #SetToggleCheckLisetにオンになっているボタンのアトリビュートが入っている
                                    #セットするオブジェクトのアトリビュートとセットオプションのアトリビュートが一致したらセットする
                                    if self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]] in self.SetToggleCheckLiset:
                                        #self.AttrToggleCheckListにはミラーオプションでオンになっているアトリビュートが入っているのでここを*-1する　なければそのままセット
                                        if self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]] in self.AttrToggleCheckList:
                                            #オブジェクト名 + アトリビュート名 , 数値
                                            cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.UpperText, self.LowerText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                                        self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]] * -1)
                                        else:
                                            cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.UpperText, self.LowerText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                                        self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]])
                                    #MirrorOptionTextFieldに入力されているとき
                                else:
                                    #SetToggleCheckLisetにオンになっているボタンのアトリビュートが入っている
                                    #セットするオブジェクトのアトリビュートとセットオプションのアトリビュートが一致したらセットする
                                    if self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]] in self.SetToggleCheckLiset:
                                        #MirrorOptionTextFieldに入っているオブジェクト名と一致してミラー軸のボタンがオンの時　そのオブジェクトのみミラー時-1する
                                        #self.AttrToggleCheckListにはミラーオプションでオンになっているアトリビュートが入っているのでここを*-1する　なければそのままセット
                                        if self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]] in self.AttrToggleCheckList and self.PoseList[SelectIndex][SetV][0] in self.MirrorOptionTextField:
                                            #オブジェクト名 + アトリビュート名 , 数値
                                            cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.UpperText, self.LowerText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                                        self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]] * -1)
                                        else:
                                            cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.UpperText, self.LowerText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                                        self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]])
                            elif self.LowerText in self.PoseList[SelectIndex][SetV][0]:
                                if len(self.MirrorOptionTextField) == 0:
                                    #SetToggleCheckLisetにオンになっているボタンのアトリビュートが入っている
                                    #セットするオブジェクトのアトリビュートとセットオプションのアトリビュートが一致したらセットする
                                    if self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]] in self.SetToggleCheckLiset:
                                        #self.AttrToggleCheckListにはミラーオプションでオンになっているアトリビュートが入っているのでここを*-1する　なければそのままセット
                                        if self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]] in self.AttrToggleCheckList:
                                            #オブジェクト名 + アトリビュート名 , 数値
                                            cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.LowerText, self.UpperText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                                        self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]] * -1)
                                        else:
                                            cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.LowerText, self.UpperText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                                    self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]])
                                else:
                                    #SetToggleCheckLisetにオンになっているボタンのアトリビュートが入っている
                                    #セットするオブジェクトのアトリビュートとセットオプションのアトリビュートが一致したらセットする
                                    if self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]] in self.SetToggleCheckLiset:
                                        #self.AttrToggleCheckListにはミラーオプションでオンになっているアトリビュートが入っているのでここを*-1する　なければそのままセット
                                        if self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]] in self.AttrToggleCheckList and self.PoseList[SelectIndex][SetV][0] in self.MirrorOptionTextField:
                                            #オブジェクト名 + アトリビュート名 , 数値
                                            cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.LowerText, self.UpperText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                                        self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]] * -1)
                                        else:
                                            cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.LowerText, self.UpperText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                                    self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]])
                        #Mirrorオプションのチェックボックスがオン
                        elif StateofMirrorCheckBox == True:
                            #オブジェクト名の置き換え　上のテキストフィールドに入っている文字と 例 _R と一致したらその文字と 下のテキストフィールドの文字と入れ替える   
                            #'該当させたい文字列'x in 検索したい文字列の入ったリストy   xがyの中にあるとTrue
                            if self.UpperText in self.PoseList[SelectIndex][SetV][0]:
                                #MirrorOptionTextFieldに何も入力されていないとき
                                if len(self.MirrorOptionTextField) == 0:
                                    #self.AttrToggleCheckListにはミラーオプションでオンになっているアトリビュートが入っているのでここを*-1する　なければそのままセット
                                    if self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]] in self.AttrToggleCheckList:
                                        #オブジェクト名 + アトリビュート名 , 数値
                                        cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.UpperText, self.LowerText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                                    self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]] * -1)
                                    else:
                                        cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.UpperText, self.LowerText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                                    self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]])
                                #MirrorOptionTextFieldに入力されているとき
                                else:
                                    #MirrorOptionTextFieldに入っているオブジェクト名と一致してミラー軸のボタンがオンの時　そのオブジェクトのみミラー時-1する
                                    #self.AttrToggleCheckListにはミラーオプションでオンになっているアトリビュートが入っているのでここを*-1する　なければそのままセット
                                    if self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]] in self.AttrToggleCheckList and self.PoseList[SelectIndex][SetV][0] in self.MirrorOptionTextField:
                                        #オブジェクト名 + アトリビュート名 , 数値
                                        cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.UpperText, self.LowerText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                                    self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]] * -1)
                                    else:
                                        cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.UpperText, self.LowerText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                                    self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]])
                            elif self.LowerText in self.PoseList[SelectIndex][SetV][0]:
                                if len(self.MirrorOptionTextField) == 0:
                                    #self.AttrToggleCheckListにはミラーオプションでオンになっているアトリビュートが入っているのでここを*-1する　なければそのままセット
                                    if self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]] in self.AttrToggleCheckList:
                                        #オブジェクト名 + アトリビュート名 , 数値
                                        cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.LowerText, self.UpperText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                                    self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]] * -1)
                                    else:
                                        cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.LowerText, self.UpperText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                                self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]])
                                else:
                                    #self.AttrToggleCheckListにはミラーオプションでオンになっているアトリビュートが入っているのでここを*-1する　なければそのままセット
                                    if self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]] in self.AttrToggleCheckList and self.PoseList[SelectIndex][SetV][0] in self.MirrorOptionTextField:
                                        #オブジェクト名 + アトリビュート名 , 数値
                                        cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.LowerText, self.UpperText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                                    self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]] * -1)
                                    else:
                                        cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.LowerText, self.UpperText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                                self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]])
                        #Mirrorオプションのチェックボックスがオフ
                        else:
                            if self.UpperText in self.PoseList[SelectIndex][SetV][0]:
                                cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.UpperText, self.LowerText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                            self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]])
                            elif self.LowerText in self.PoseList[SelectIndex][SetV][0]:
                                cmds.setAttr(self.PoseList[SelectIndex][SetV][0].replace(self.LowerText, self.UpperText) + self.AttrCheck[self.NoLockList[SelectIndex][SetV][SetA]],\
                                            self.PoseList[SelectIndex][SetV][self.NoLockList[SelectIndex][SetV][SetA]])


    def CloseCommand(self, *args):
        self.PoseList.clear()
        self.Poses.clear()
        self.NoLockList.clear()
        self.PoseFrame.clear()


    #ポーズの削除
    def DeletePose(self, *args):
        if cmds.textScrollList('PoseScrollList', q = True, selectIndexedItem = True) == None:
            print("リストを選択してください")
        else:
            DelSelectPoseIdx = cmds.textScrollList('PoseScrollList', q = True, selectIndexedItem = True)
            for i in range(len(DelSelectPoseIdx)):
                del self.PoseList[max(DelSelectPoseIdx) - 1]
                del self.Poses[max(DelSelectPoseIdx) - 1]
                del self.NoLockList[max(DelSelectPoseIdx) - 1]
                del self.PoseFrame[max(DelSelectPoseIdx) - 1]
                del DelSelectPoseIdx[-1]
            self.ListRefresh()


    #表示リストの更新
    def ListRefresh(self, *args):
        NameList = []
        FrameList = []
        DisplayList = []
        for Name in self.Poses:
            NameList.append(Name[0])
        for Frame in self.PoseFrame:
            intFrame = int(Frame)
            FrameList.append(intFrame)
        for i in range(len(NameList)):
            DList = NameList[i] + " " + "[" +  str(FrameList[i]) + "F" + "]"
            DisplayList.append(DList)
        cmds.textScrollList('PoseScrollList', e = True, removeAll = True)
        cmds.textScrollList('PoseScrollList', e = True, append = DisplayList)


    #名前変更
    def ListReNeme(self, *args):
        if cmds.textScrollList('PoseScrollList', q = True, selectIndexedItem = True) == None:
            print("リストを選択してください")
        else:
            NameChangeIdx = int(cmds.textScrollList('PoseScrollList', q = True, selectIndexedItem = True)[0]) - 1
            result = cmds.promptDialog(title = 'Rename Object', message = 'Enter Name:', button = ['OK', 'Cancel'], defaultButton = 'OK',\
                                        cancelButton = 'Cancel', dismissString = 'Cancel')
            if result == 'OK':
                text = cmds.promptDialog(query = True, text = True)
            self.Poses[NameChangeIdx] = text.split()
            self.ListRefresh()


    #表示リストの選択をした場合オブジェクトを選択
    def SelectPoseList(self, *args):
        PoseIdx = int(cmds.textScrollList('PoseScrollList', q = True, selectIndexedItem = True)[0]) - 1
        ObjList = []
        for PIdx in range(len(self.PoseList[PoseIdx])):
            ObjList.append(self.PoseList[PoseIdx][PIdx][0])
        cmds.select(ObjList)


    #ミラーボタンを押したときの処理
    def MirrorToggle(self, *args):
        if not self.Mirror:
            self.Mirror = True
            #cmds.button("M", e = True, noBackground = self.Mirror)
            cmds.textField("UpperTextField", e = True, enable = True)
            cmds.textField("LowerTextField", e = True, enable = True)
            cmds.checkBox("MirrorOptionCheck", e = True, enable = True,)
        else:
            self.Mirror = False
            #cmds.button("M", e = True, noBackground = self.Mirror)
            cmds.textField("UpperTextField", e = True, enable = False)
            cmds.textField("LowerTextField", e = True, enable = False)
            if cmds.checkBox("MirrorOptionCheck", q = True, value = True) and self.MirrorCheck:
                self.MirrorCheckBoxToggle()
            cmds.checkBox("MirrorOptionCheck", e = True, enable = False, value = False)


    # def MirrorAxis(self, ReturnAxis, *args):
    #     self.optionmenu = ReturnAxis


    def MirrorCheckBoxToggle(self, *args):
        if not self.MirrorCheck:
            self.MirrorCheck = True
            cmds.button("TX", e = True, enable = True)
            cmds.button("TY", e = True, enable = True)
            cmds.button("TZ", e = True, enable = True)
            cmds.button("RX", e = True, enable = True)
            cmds.button("RY", e = True, enable = True)
            cmds.button("RZ", e = True, enable = True)
            cmds.button("SX", e = True, enable = True)
            cmds.button("SY", e = True, enable = True)
            cmds.button("SZ", e = True, enable = True)
            cmds.textField("MirrotoptionTextField", e = True, enable = True )
        else:
            self.MirrorCheck = False
            cmds.button("TX", e = True, enable = False)
            cmds.button("TY", e = True, enable = False)
            cmds.button("TZ", e = True, enable = False)
            cmds.button("RX", e = True, enable = False)
            cmds.button("RY", e = True, enable = False)
            cmds.button("RZ", e = True, enable = False)
            cmds.button("SX", e = True, enable = False)
            cmds.button("SY", e = True, enable = False)
            cmds.button("SZ", e = True, enable = False)
            cmds.textField("MirrotoptionTextField", e = True, enable = False )


    def Toggle(self, BName, AName):
        if not AName in self.AttrToggleCheckList:
            cmds.button(BName, e = True, noBackground = True)
            self.AttrToggleCheckList.append(str(AName))
        else:
            cmds.button(BName, e = True, noBackground = False)
            self.AttrToggleCheckList = [item.replace(AName, "") for item in self.AttrToggleCheckList]


    def TransformXToggle(self, *args):
        self.Toggle("TX", ".translateX")


    def TransformYToggle(self, *args):
        self.Toggle("TY",".translateY")


    def TransformZToggle(self, *args):
        self.Toggle("TZ",".translateZ")


    def RotateXToggle(self, *args):
        self.Toggle("RX",".rotateX")


    def RotateYToggle(self, *args):
        self.Toggle("RY",".rotateY")


    def RotateZToggle(self, *args):
        self.Toggle("RZ",".rotateZ")

 
    def ScaleXToggle(self, *args):
        self.Toggle("SX",".scaleX")


    def ScaleYToggle(self, *args):
        self.Toggle("SY",".scaleY")


    def ScaleZToggle(self, *args):
        self.Toggle("SZ",".scaleZ")


    def SetCheckBoxToggle(self, *args):
        if not self.SetCheck:
            self.SetCheck = True
            cmds.button("SetTX", e = True, enable = True)
            cmds.button("SetTY", e = True, enable = True)
            cmds.button("SetTZ", e = True, enable = True)
            cmds.button("SetRX", e = True, enable = True)
            cmds.button("SetRY", e = True, enable = True)
            cmds.button("SetRZ", e = True, enable = True)
            cmds.button("SetSX", e = True, enable = True)
            cmds.button("SetSY", e = True, enable = True)
            cmds.button("SetSZ", e = True, enable = True)
        else:
            self.SetCheck = False
            cmds.button("SetTX", e = True, enable = False)
            cmds.button("SetTY", e = True, enable = False)
            cmds.button("SetTZ", e = True, enable = False)
            cmds.button("SetRX", e = True, enable = False)
            cmds.button("SetRY", e = True, enable = False)
            cmds.button("SetRZ", e = True, enable = False)
            cmds.button("SetSX", e = True, enable = False)
            cmds.button("SetSY", e = True, enable = False)
            cmds.button("SetSZ", e = True, enable = False)


    def SetToggle(self, SetBName, SetAName):
        if not SetAName in self.SetToggleCheckLiset:
            cmds.button(SetBName, e = True, noBackground = True)
            self.SetToggleCheckLiset.append(str(SetAName))
        else:
            cmds.button(SetBName, e = True, noBackground = False)
            self.SetToggleCheckLiset = [item.replace(SetAName, "") for item in self.SetToggleCheckLiset]


    def SetTransformXToggle(self, *args):
        self.SetToggle("SetTX", ".translateX")


    def SetTransformYToggle(self, *args):
        self.SetToggle("SetTY",".translateY")


    def SetTransformZToggle(self, *args):
        self.SetToggle("SetTZ",".translateZ")


    def SetRotateXToggle(self, *args):
        self.SetToggle("SetRX",".rotateX")


    def SetRotateYToggle(self, *args):
        self.SetToggle("SetRY",".rotateY")


    def SetRotateZToggle(self, *args):
        self.SetToggle("SetRZ",".rotateZ")

 
    def SetScaleXToggle(self, *args):
        self.SetToggle("SetSX",".scaleX")


    def SetScaleYToggle(self, *args):
        self.SetToggle("SetSY",".scaleY")


    def SetScaleZToggle(self, *args):
        self.SetToggle("SetSZ",".scaleZ")


    #引数には取得したアトリビュートの情報が入っている
    #ロックされていないアトリビュートのリストの中の位置を取り出す
    def GetSetList(self, s):
        self.SetList.clear()
        #引数のオブジェクトの数だけ繰り返す
        for SetL in range(len(s)):
            self.ListValue.clear()
            #オブジェクトのアトリビュートの数だけ繰り返す
            for NoLock in range(len(s[SetL])):
                try:
                    #そのアトリビュートがfloatに変換できるか試す 変換できる = ロックされていないアトリビュートになる
                    float(s[SetL][NoLock])
                except TypeError:
                    #変換できない場合何もしない
                    pass
                except ValueError:
                    #変換できない場合何もしない
                    pass
                else:
                    #変換できたもののリストの中の位置を追加
                    self.ListValue.append(NoLock)
            #位置をオブジェクトごとに追加 .copyをしないとすべて同じ値になる 参照値
            self.SetList.append(self.ListValue.copy())
        return self.SetList


    def LockCheck(self, GetName, *args):
        #print(getName)
        #オブジェクトの数だけ繰り返す
        for gn in range(len(GetName)):
            self.noLockAttr.clear()
            #attrCheckの数だけ繰り返す
            for i in range(len(self.AttrCheck) - 1):
                #ロックされているか調べる　オブジェクト名+.アトリビュート
                lockAttr = cmds.getAttr(GetName[gn] + self.AttrCheck[i + 1], lock = True)
                settableAttr = cmds.getAttr(GetName[gn] + self.AttrCheck[i + 1], settable = True)
                keyableAttr = cmds.getAttr(GetName[gn] + self.AttrCheck[i + 1], keyable = True)
                #ロックされていないアトリビュートをnoLockAttrに入れる appendでリストの末尾に要素を追加
                if lockAttr == False and settableAttr == 1 and keyableAttr == True:
                    self.noLockAttr.append(self.AttrCheck[i + 1])
                    #print(attrCheck[i])
                    #print(self.noLockAttr)
            
            #ロックされていないアトリビュートを取得
            if (".translateX" in self.noLockAttr) == True:
                self.tx = cmds.getAttr(GetName[gn] + ".translateX")
            else:
                self.tx = ()

            if (".translateY" in self.noLockAttr) == True:
                self.ty = cmds.getAttr(GetName[gn] + ".translateY")
            else:
                self.ty = ()

            if (".translateZ" in self.noLockAttr) == True:
                self.tz = cmds.getAttr(GetName[gn] + ".translateZ")
            else:
                self.tz = ()

            if (".rotateX" in self.noLockAttr) == True:
                self.rx = cmds.getAttr(GetName[gn] + ".rotateX")
            else:
                self.rx = ()

            if (".rotateY" in self.noLockAttr) == True:
                self.ry = cmds.getAttr(GetName[gn] + ".rotateY")
            else:
                self.ry = ()

            if (".rotateZ" in self.noLockAttr) == True:
                self.rz = cmds.getAttr(GetName[gn] + ".rotateZ")
            else:
                self.rz = ()

            if (".scaleX" in self.noLockAttr) == True:
                self.sx = cmds.getAttr(GetName[gn] + ".scaleX")
            else:
                self.sx = ()

            if (".scaleY" in self.noLockAttr) == True:
                self.sy = cmds.getAttr(GetName[gn] + ".scaleY")
            else:
                self.sy = ()

            if (".scaleZ" in self.noLockAttr) == True:
                self.sz = cmds.getAttr(GetName[gn] + ".scaleZ")
            else:
                self.sz = ()
            
            self.getAttr = [GetName[gn], self.tx, self.ty, self.tz, self.rx, self.ry, self.rz, self.sx, self.sy, self.sz]
            #print(self.getAttr, gn)
            self.setAttr.append(self.getAttr)
            #print(self.setAttr, gn)
        return self.setAttr


select = Main()


#windowを作成
def createwindow():
    if cmds.window( 'MyWindow', exists=True ): #existsは指定したオブジェクトが存在するかどうかを返す
        cmds.deleteUI( 'MyWindow', window=True ) #window = Trueは削除するオブジェクト名をウィンドウに限定します。
    winMyWindow = cmds.window( 'MyWindow', title = 'PoseMirror', closeCommand = select.CloseCommand)
    with LayoutManager(cmds.columnLayout("Gui", parent = "MyWindow", adjustableColumn = True)):
        cmds.text("PoseList")
        cmds.textScrollList("PoseScrollList", numberOfRows = 10, doubleClickCommand = select.SelectPoseList, allowMultiSelection = True)
        with LayoutManager(cmds.rowLayout("Button", parent = "Gui", width = 200, numberOfColumns = 4, adjustableColumn = 1, adjustableColumn4 = 2)):
            cmds.button("GetPose", command = select.GetPose)
            cmds.button("SetPose", command = select.SetPose)
            cmds.button("DeletePose", command = select.DeletePose)
            cmds.button("Rename", command = select.ListReNeme)
        with LayoutManager(cmds.columnLayout("SetOptionLayout", parent = "Gui", adjustableColumn = 1)):
            cmds.checkBox("SetOption", changeCommand = select.SetCheckBoxToggle)
            with LayoutManager(cmds.rowColumnLayout(numberOfColumns = 4, parent = "SetOptionLayout", adjustableColumn = 1, columnAttach = (1, "left", 5))):
                cmds.text("SetTranslate", label = "Translate", align = "left")
                cmds.button("SetTX", label = "X", enable = False, command = select.SetTransformXToggle)
                cmds.button("SetTY", label = "Y", enable = False, command = select.SetTransformYToggle)
                cmds.button("SetTZ", label = "Z", enable = False, command = select.SetTransformZToggle)
                cmds.text("SetRotate", label = "Rotate", align = "left")
                cmds.button("SetRX", label = "X", enable = False, command = select.SetRotateXToggle)
                cmds.button("SetRY", label = "Y", enable = False, command = select.SetRotateYToggle)
                cmds.button("SetRZ", label = "Z", enable = False, command = select.SetRotateZToggle)
                cmds.text("SetScale", label = "Scale", align = "left")
                cmds.button("SetSX", label = "X", enable = False, command = select.SetScaleXToggle)
                cmds.button("SetSY", label = "Y", enable = False, command = select.SetScaleYToggle)
                cmds.button("SetSZ", label = "Z", enable = False, command = select.SetScaleZToggle)
        with LayoutManager(cmds.rowLayout("MirrorLayout", numberOfColumns = 2, rowAttach = (1, "top", 0), columnAttach = (2, "left", 0), adjustableColumn = 2)):
            with LayoutManager(cmds.columnLayout("MirrorCheckBox", parent = "MirrorLayout",)):
                with LayoutManager(cmds.rowLayout("MirrorCheckBoxLayout", parent = "MirrorCheckBox", numberOfColumns = 1,)):
                    cmds.checkBox("M", label = "Mirror", changeCommand = select.MirrorToggle)
                with LayoutManager(cmds.columnLayout("TextLayout", parent = "MirrorCheckBox",)):
                    cmds.textField("UpperTextField", enable = False, parent = "TextLayout")
                    cmds.textField("LowerTextField", enable = False, parent = "TextLayout")
            with LayoutManager(cmds.columnLayout("MirrotoptionLayout", parent = "MirrorLayout", adjustableColumn = 1)):
                cmds.checkBox("MirrorOptionCheck", label = "MirrorOption", enable = False, changeCommand = select.MirrorCheckBoxToggle)
                with LayoutManager(cmds.rowColumnLayout(numberOfColumns = 4, parent = "MirrotoptionLayout", adjustableColumn = 1, columnAttach = (1, "left", 5))):
                    cmds.text("Translate", align = "left")
                    cmds.button("TX", label = "X", enable = False, noBackground = True, command = select.TransformXToggle)
                    cmds.button("TY", label = "Y", enable = False, command = select.TransformYToggle)
                    cmds.button("TZ", label = "Z", enable = False, command = select.TransformZToggle)
                    cmds.text("Rotate", align = "left")
                    cmds.button("RX", label = "X", enable = False, command = select.RotateXToggle)
                    cmds.button("RY", label = "Y", enable = False, noBackground = True, command = select.RotateYToggle)
                    cmds.button("RZ", label = "Z", enable = False, noBackground = True, command = select.RotateZToggle)
                    cmds.text("Scale", align = "left")
                    cmds.button("SX", label = "X", enable = False, command = select.ScaleXToggle)
                    cmds.button("SY", label = "Y", enable = False, command = select.ScaleYToggle)
                    cmds.button("SZ", label = "Z", enable = False, command = select.ScaleZToggle)
                with LayoutManager(cmds.columnLayout(parent = "MirrotoptionLayout", adjustableColumn = 1)):
                    cmds.textField("MirrotoptionTextField", enable = False )
    
    select.TransformXToggle()
    select.RotateYToggle()
    select.RotateZToggle()
    select.ListRefresh()
    cmds.showWindow(winMyWindow)


    
if __name__ == "__main__":
    createwindow()


