"""Tags all Rooms within Selected Views from a Linked Model"""
# This file contains a set of functions used to run in the Revit Python Shell
# Required functions are then copied and pasted into the necessary 'script.py' file
# with the required conventions altered

# Made in HHA

__title_ = "Tag Rooms\nFrom Linked Document"
# Essential Imports and Elements
from distutils.log import set_verbosity
import clr

try:
	doc = __revit__.ActiveUIDocument.Document
except:
	print("The document could not be initialized")
	raise ValueError("Could not find current document")

clr.AddReference("RevitAPI")
clr.AddReference("System.Windows.Forms")
clr.AddReference("IronPython.Wpf")
from Autodesk import Revit
from Autodesk.Revit.DB import *
from datetime import date, datetime
from pyrevit import script
import wpf
from System import Windows
# Defined certain default categories that will be used throughout the project
getSortedInstances = lambda document, className : FilteredElementCollector(document).OfClass(className)
roomcat = BuiltInCategory.OST_Rooms
errorreporttxt = "report.txt"



# A decorator that handles several types of errors
def textouput_errorcheck (func):
	def inner_func(*args, **kwargs):
		try:
			funcval =  [func(*args, **kwargs)]
			if len(funcval) == 1:
				returnval = funcval
				outputval = "WARNING: Function does not have built in errorchecking - {} was executed.".format(func.__name__)
			elif len(funcval) == 2:
				returnval = funcval[0]
				outputval = funcval[1]
			else:
				raise TypeError("Output of function should contain 2 values - expected return value and a log report string. Expected 2 values, got {}".format(len(funcval)))
			file_obj = open(errorreporttxt, "a")
			today = date.today().isoformat()
			time = datetime.now().strftime("%H:%M:%S")
			file_obj.write("{} {}: OUTPUT: {}".format(today, time, outputval[1]))
			file_obj.close()
			return returnval
		except Exception as e:
			import traceback, sys
			file_obj = open(errorreporttxt, "a")
			today = date.today().isoformat()
			time = datetime.now().strftime("%H:%M:%S")
			file_obj.write("{} {}: ERROR: {}".format(today, time, e))
			file_obj.close()
			traceback.print_exc(file=sys.stdout)
	return inner_func

# A decorator that handles several types of errors
def errorcheck (func):
	def inner_func(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except:
			import traceback, sys
			traceback.print_exc(file=sys.stdout)
	return inner_func
			
# Returns every linked instance in the current rvt project
@errorcheck
def getLinkedInstances():
	# Getting the current Document to find a list of linked services
	# NTS: Document Manager Retrieves current File
	currentdocument = doc
	# General Functions to sort instances of Revit Documents
	getLinkedInstances = lambda document : getSortedInstances(document, Revit.DB.RevitLinkInstance)
	
	# function: 
	instances = []
	for instance in getLinkedInstances(currentdocument):
		instances.append({"Document": instance.GetLinkDocument(), "Name": instance.Name, "Instance": instance})
	if len(instances) <= 0:
		raise ValueError("No Linked Instances were found in the given document")
	return instances

# Returns the elements from a linked instance
@errorcheck
def getElementsfromLinkedInstance (document, category): 
	# Grabs a filtered version of the document
	collector = FilteredElementCollector(document)
	# Narrows down list to category Rooms
	elementlist =  collector.OfCategory(category).WhereElementIsNotElementType().ToElements()
	if len(elementlist) <= 0:
		raise ValueError("No Elements of the defiend category were foud in the instance")
	return elementlist

#Returns a list of non-null ViewPlans
@errorcheck
def getViewPlans():
	# Following line finds all of the lins
	collector = FilteredElementCollector(doc).OfClass(ViewPlan).ToElements()
	# Following checks to make sure ViewPlans are found in the room, and that nonnull rooms are returned
	if len(collector) <= 0:
		raise ValueError("No ViewPlans were found in the document - FilteredElementCollector found no ViewPlans")
	namelist = [vp.Name for vp in collector]
	# List of flagged indexes are stored in errls, transformed into a string-index string dictionary, for filtering
	errls = []
	for i in range(len(namelist)):
		if not namelist[i]:
			errls.append(i)
	if len(errls) == len(namelist):
		raise ValueError("All Viewplans in the document are unnamed - Named Views may be selected for tagging")
	colldict = {str(i) : collector[i] for i in range(len(namelist))}
	for val in errls:
		colldict.drop[str(val)]
	# returns a list of the values from the dictionary only
	return list(colldict.values())

# A function that grabs existing roomtags in order to avoid "retagging"

# General class for wpf powered ui windows
class UIWindow (Windows.Window):
	def __init__ (self, xamlfile):
		wpf.LoadComponent(self, xamlfile)


# Function to tag all rooms in Linked Model
@errorcheck
def tagViewsinLinkedElements(tagAll = False):
	# Call necessary functions and define the variables
	linkedinst = getLinkedInstances()[0]
	elements = getElementsfromLinkedInstance(linkedinst["Document"], roomcat)
	viewplans = getViewPlans()

	# Key mistake madee when referring to models in a Linked model: use the LinkedInstance.GetTransform() function
	transform = linkedinst["Instance"].GetTransform()

	if tagAll:
		selviews = viewplans
	else : selviews = [0]

	t = Transaction(doc, "Tag Rooms in Linked Models")
	t.Start()
	for view in viewplans:
		for i in range(len(elements)):
			if isinstance(view, (ViewSection, ViewPlan)):
				el = elements[i]
				point = transform.OfPoint(el.Location.Point)
				tagPoint = UV(point.X, point.Y)
				roomId = LinkElementId(linkedinst["Instance"].Id, el.Id)
				rtag = doc.Create.NewRoomTag(
					roomId,
					tagPoint,
					view.Id
				)
	t.Commit()
	
tagViewsinLinkedElements()