# Troubleshooting Guide for Developing PyRevit Plugins

## Tool Installation:

#### **PyRevit does not show up in the tabs:**
 - Try using the "admin" installer for PyRevit (note: some files may be installed into the AppData folder under the Admin user)
 - Check to make sure that a .addin file with the appropriately named plugin can be foud at C:\ProgramData\Autodesk\Revit\Addins\20XX. If the file is not found, try running the installer again or make a .addin file that points to the appropriate file location in the assembly tags. 
 ```
 <Assembly>C:\Program Files\pyRevit-Master\bin\engines\IPY277\pyRevitLoader.dll</Assembly>
 ```

#### **RevitPythonShell does not show up in Add-ins tab after installing:**
 - Ensure that the right version of the shell is installed
 - Check that RevitPythonShell is installed in the correct location:
   - `C:\Program Files (x86)\RevitPythonShell\20XX\` for 2020 and later
   - `C:\Program Files (x86)\RevitPythonShell20XX\` for 2019 and later
 - Check to make sure that a .addin file with the appropriately named plugin can be foud at `C:\ProgramData\Autodesk\Revit\Addins\20XX` or at `C:\Users\varunan.varathan\AppData\Roaming\Autodesk\Revit\Addins\20XX`. If not found at either location, place a new .addin file and accompanying files in the following file structure: 
 ```
 - 20XX
   | RevitPythonShell20XX.addin
   | RevitPythonShell20XX
   | | init.py
   | | RevitPythonShell.xml
   | | startup.py

(py and xml files can be found at: https://github.com/architecture-building-systems/revitpythonshell/tree/master/RevitPythonShell/DefaultConfig)
 ```
 - Ensure that the .addin file points to the RevitPythonShell.dll file in the appropriate file location as seen in the second point

## Development

#### **DocumentManager is not available/returns NoneType:** and 
#### **RevitServices does not work:**
 - RevitServices may work when Dynamo is running in the background, but will not return when added as a reference through CLR. RevitServices is a core part of Dynamo, but does not come standard with Revit and the RevitAPI
 - Use `__revit__.ActiveUIDocument.Document` insted of `CurrentDBDocument` to extract data from a Revit Model

#### **Code does not run/compile**
 - The original set of HHA Revit Tools was written in IronPython, which compiles from Python 2.7.x. Newer versions of PyRevit primarily use CPython, which compiles from Python 3.x.x. Ensure that any code is written to compile in Python 3
 - (See Above) PyRevit does not support RevitServices. 
 - Ensure that the filestructure for an element looks like this:
 ```
 - command.pushbutton
   | script.py
   | icon.png
   | bundle.yaml
   | _____.xaml (for wpf)
 ```

####