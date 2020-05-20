#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__ = 'Výška a označenie\nprierazov'
__doc__ = """Sets distance of Sill Height of Windows from Project zero to parameter "SH prierazu".
Sets Level number to parameter "Poschodie" to Windows and Generic Models
Sets Level elevation to parameter "ref od 0" to Windows.
Sets Mark to Windows and Generic Models in xxx format f.e. 001

Only Windows and Generic Models with Type Comments == "stavebne upravy" are processed.
You need to add theese Shared Parameters: Poschodie, SH prierazu, Offset Shared, Priemer, ref od 0."""

__helpurl__ = "https://youtu.be/2LBi9p3gPiY"

# for timing------
from pyrevit.coreutils import Timer
from pyrevit import coreutils, forms
from custom_output import hmsTimer
timer = Timer()
# ----------------

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, \
                Transaction, Document, BuiltInParameter
from pyrevit import revit, DB
from pyrevit import script

doc = __revit__.ActiveUIDocument.Document


# dialog
dialog = forms.alert("Chceš naoaj prepísať všetky prierazy?",
                  ok=False, yes=True, no=True)
if dialog:
    # /////// COLLECTORS /////////
    # collecting windows
    windows_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows) \
        .WhereElementIsNotElementType() \
        .ToElements()

    # collecting generic models
    genericModel_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel) \
        .WhereElementIsNotElementType() \
        .ToElements()

    output = script.get_output()

    # /////// FUNCTIONS /////////
    #converts milimeters to feets
    def mm2feet(a):
        b = a*0.00328084
        return b

    #converts feets to milimeters and makes rounded integer from the result
    def feet2mm(a):
        b = a/0.00328084
        return int(round(b))

    # highlights text using html string with css
    def text_highligter(a):
            content = str(a)
            html_code = "<p class='elementlink'>"+content+"</p>"
            return coreutils.prepare_html_str(html_code)

    # error handling
    def skipped(element,parameterName):
        # notprocessed.append(element.Id.IntegerValue)
        # notprocessed.append(element.Id)
        elemID = element.Id
        elemName = element.Name
        paramList = [output.linkify(elemID), elemName]
        # paramList = [elemID, elemName]
        notprocessed.append(paramList)

        parameter = element.LookupParameter(parameterName)
        if parameter:
            parameter.Set("no data")

    # level number extraction
    def levelNameExtraction(levelName):
        # searching for dot in name of level
        try:
            index = levelName.index(".")
            levelNumber = levelName[0:index]
        # when there is no dot in name returns frist 2 characters
        except:
            levelNumber = levelName[0:2]
        return levelNumber

    # adding 0 to one digit numbers in level names
    def zeros(levelNumber):
        try:
            # positive numbers
            if int(levelNumber) < 10 and int(levelNumber) >= 0:
                levelNumberSet = "0" + levelNumber
            # negative numbers
            else:
                levelNumberSet = levelNumber
        # strings - non numbers
        except:
            levelNumberSet = levelNumber
        return levelNumberSet

    # adding 00 to one digit numbers
    def zerosNum(a):
        if a < 10 and a > 0:
            a = "00"+str(a)
        elif a < 100:
            a = "0"+str(a)
        return str(a)

    def poschodieSetter(element,levelElement):
        elementTypeId = element.GetTypeId()
        elementType = Document.GetElement(doc,elementTypeId)
        # filtering elements
        filterp = elementType.LookupParameter('Type Comments')
        if filterp and filterp.AsString() == "stavebne upravy":    
            try:
                # setting parameters
                levelName = levelElement.LookupParameter('Name').AsString()
                # getting Number string from Level Name
                levelNumber = levelNameExtraction(levelName)
                # adding 0 to one digit numbers
                levelNumberSet = zeros(levelNumber)
                # setting parameter "Poschodie"
                levelNameP = element.LookupParameter("Poschodie")
                if levelNameP:
                        levelNameP.Set(levelNumberSet)
                else:
                    skipped(element,"Poschodie")
            except:
                skipped(element,"Poschodie")

    # numbers openings by type, every new type will have new Mark number
    # atributes names:
    # circular: diameter name, circular mark f.e. "wc"
    # rectangular: width, height or depth, rectangular mark f.e. "wr"
    def markSetter(element,DiameterName,CircularMark,WidthName,HeightDepthName,RectMark):
    # # filter by Type Comments == stavebne upravy
        elementTypeId = element.GetTypeId()
        elementType = Document.GetElement(doc,elementTypeId)
        filterp = elementType.LookupParameter('Type Comments')

        if filterp and filterp.AsString() == "stavebne upravy":
            # setting Mark values
            try:
                try:
                    # circular windows
                    diameter_param = element.LookupParameter(DiameterName).AsDouble()
                    # print("diameter = " +str(diameter_param))
                    diameterValue = feet2mm(diameter_param)
                    # wc = wall circular
                    dimensionsList = [diameterValue,CircularMark]
                except:
                    # rectengular windows
                    width_param = element.LookupParameter(WidthName).AsDouble()
                    heightDepth_param = element.LookupParameter(HeightDepthName).AsDouble()

                    widthValue = feet2mm(width_param)
                    heightDepthValue = feet2mm(heightDepth_param)
                    # RectMark >>> wr = wall rectengular
                    dimensionsList = [widthValue,heightDepthValue,RectMark]
                # checking if it is known type
                if dimensionsList in elementTypes:
                    index = elementTypes.index(dimensionsList)
                    a = index + 1
                # if it is new type adding to the list of types
                else:
                    elementTypes.append(dimensionsList)
                    a = len(elementTypes)
                mark_param = element.LookupParameter('Mark')
                # adding zeros 001, 015, 156 etc
                a=zerosNum(a)
                mark_param.Set(a)
            except:
                pass

    # getting levels from generic models and other elements
    def GetLevel(item):
        #if hasattr(item, "LevelId"): return item.Document.GetElement(item.LevelId)
        if hasattr(item, "Level"): return item.Level
        elif hasattr(item, "GenLevel"): return item.GenLevel
        else:
            try: return item.Document.GetElement(item.get_Parameter(BuiltInParameter.INSTANCE_REFERENCE_LEVEL_PARAM).AsElementId())
            except: 
                try: return item.Document.GetElement(item.get_Parameter(BuiltInParameter.INSTANCE_SCHEDULE_ONLY_LEVEL_PARAM).AsElementId())
                except: pass

    t = Transaction(doc, "Vyska a oznacenie prierazov")
    t.Start()

    notprocessed = []
    # creating lists - just for debugging
    # sill_height_values_list=[]
    # sill_height_values_list=[]
    # level_ids_list=[]
    # level_elevation_list=[]
    # sill_height_zeroMM_list=[]
    # offset_shared_values_list=[]

    # creating lists - just for debugging
    # level_ids_list=[]
    # level_name_list=[]
    # indexlist=[]

    # /////// WINDOW SILL HEIGHT /////////
    # getting window parameters
    for window in windows_collector:
        # filter by Type Comments == stavebne upravy
        elementTypeId = window.GetTypeId()
        elementType = Document.GetElement(doc,elementTypeId)
        filterp = elementType.LookupParameter('Type Comments')

        if filterp and filterp.AsString() == "stavebne upravy":
            try:
                try:
                    # hosted elements with Sill Height
                    # geting Sill Height from windows
                    sillHeightFt = window.LookupParameter('Sill Height')
                    sill_height_value = sillHeightFt.AsDouble()
                    # sill_height_values_list.append(feet2mm(sill_height_value))

                except:
                    # nonhosted elements with Offset Shared
                    # geting Offset Shared from windows
                    OffsetSharedFt = window.LookupParameter('Offset Shared')
                    offset_shared_value = OffsetSharedFt.AsDouble()
                    # offset_shared_values_list.append(feet2mm(offset_shared_value))

                # geting levels from windows
                level = window.LevelId
                # level_ids_list.append(level)

                # getting elevation of levels from project zero +0.000
                level_element = Document.GetElement(doc,level)
                level_elevation = level_element.Elevation
                # level_elevation_list.append(feet2mm(level_elevation))

                # write Level Height Values to "ref od 0" parameter of windows
                level_height_param = window.LookupParameter('ref od 0')
                if level_height_param:
                        level_height_param.Set(level_elevation)

                # add Level Height Values to Sill Height Values of windows
                try:
                    sill_height_zero = level_elevation + sill_height_value
                    # sill_height_zeroMM = round(feet2mm(sill_height_zero))
                    # sill_height_zeroMM_list.append(sill_height_zeroMM)
                except:
                    sill_height_zero = level_elevation + offset_shared_value

                # writing "SH prierazu" parameters
                custom_param = window.LookupParameter('SH prierazu')
                if custom_param:
                    custom_param.Set(sill_height_zero)

            except:
                # notprocessed.append(window.Id.IntegerValue)
                # custom_param = window.LookupParameter('SH prierazu')
                skipped(window,'SH prierazu')

    # /////// POSCHODIE PARAMETER ASIGNMENT /////////
    for window in windows_collector:
        try:
            level = window.LevelId
            levelElement = Document.GetElement(doc,level)
            # setting parameters
            poschodieSetter(window,levelElement)
        except:
            skipped(window,"Poschodie")

    for element in genericModel_collector:
        try:
            levelElement = GetLevel(element)
            # setting parameters
            poschodieSetter(element,levelElement)
        except:
            skipped(element,"Poschodie")


    # /////// UNIQUE MARK PARAMETER ASIGNMENT /////////
    # Types of openings used in markSetter function, a is used as Mark sequence
    elementTypes = []
    a = 0
    for element in windows_collector:
        # setting Mark values - atributes are parameters names, wc = window circular
        markSetter(element,"Priemer","wc","Width","Height","wr")

    for element in genericModel_collector:
        # setting Mark values - atributes are parameters names, gmc = generic model circular
        markSetter(element,"Diameter","gmc","Width","Depth","gmr")

    t.Commit()

    # just for debuging window sill height
    # print("control lists for debugging")
    # print(sill_height_values_list)
    # print(level_ids_list)
    # print(level_elevation_list)
    # print(sill_height_zeroMM_list)
    # print(offset_shared_values_list)

    # debuging poschodie
    # print(level_name_list)
    # print(indexlist)

    # Final Claims

    countOfSkippedElms = len(notprocessed)
    print(text_highligter(str(countOfSkippedElms) +" elements were skipped"))
    # print(notprocessed)
    if countOfSkippedElms>0:
        output.print_table(table_data = notprocessed,
                           title = "Skipped elements",
                           columns=["Element Id", "Name"],
                           formats=['', ''])

    # for timing------
    endtime = timer.get_time()
    print(hmsTimer(endtime))
    # endtimeRound = round(endtime*1000)/1000
    # print("\nTime "+str(endtimeRound)+" seconds.")
    # --------------