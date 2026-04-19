#v003
#on Windows:  C:/Users/<username>/AppData/Local/Agisoft/Metashape Pro/scripts/
#on Linux:  /home/<username>/.local/share/Agisoft/Metashape Pro/scripts/


   
import sys
import re
import os

import Metashape

	
	
	
	
def TrimbleFileConverter(pathFileMain):
	print("Open Trimble File:", pathFileMain)
	fimeMain = open(pathFileMain)
	
	pathFileTmp = pathFileMain + ".txt"
	print("Create Trimble File Tmp:", pathFileTmp)
	fileTmp = open(pathFileTmp, 'w') 
	
	for fimeMainLine in fimeMain:
	    lst = fimeMainLine.split(',')
	    lst2 = []
	    for l in lst:
	        l2 = l.rstrip()
	        lst2.append(l2)	
	    if len(lst2) >= 4:
	        s = float(lst2[1])
	        s1 = -s
	        line2 = lst2[0] + "," + lst2[2] + "," + lst2[3] + "," + str(s1) + "\n"
	        #print(line2)
	        fileTmp.write(line2)		
	fimeMain.close()
	fileTmp.close()
	
	return pathFileTmp

def ViewgaImportTrimble():
	pathFile = Metashape.app.getOpenFileName("Open Trimble File")
	pathFileTmp = TrimbleFileConverter(pathFile)
	chunk = Metashape.app.document.chunk
	chunk.importReference(pathFileTmp, Metashape.ReferenceFormatCSV, "nxyz", ",", group_delimiters=False, skip_rows=0, ignore_labels=False, create_markers=True)
	chunk.updateTransform()
	
	os.remove(pathFileTmp)
	print("Delete Trimble File Tmp:", pathFileTmp)
	
	print("-----ViewgaImportTrimble DONE-----")
	Metashape.app.messageBox("ViewgaImportTrimble DONE")

	
	
	
	
	
	
	
	
	

	
def get_pixel_error(m):
	chunk = Metashape.app.document.chunk
	err = 0
	i = 0
	for photo in chunk.cameras:	
		if 'NoneType' not in str(type(m.projections[photo])):
			v_proj = m.projections[photo].coord
			v_reproj = photo.project(m.position)
			diff = (v_proj - v_reproj).norm()
			i=i+1		
			#print(photo, round(diff, 3))
			err = err + round(diff, 3)
	print(m, round(err/i, 3))
	return round(err/i, 3)

def ExportTrimble(chunk,filePath,pr,err):
	#print(chunk,path,pr,err)

	chunk.crs = Metashape.CoordinateSystem('LOCAL_CS["Local CS",LOCAL_DATUM["Local Datum",0],UNIT["metre",1]]')

	f2 = open(filePath, 'w')	

	for marker in chunk.markers:
	
		markerLabel = marker.label

		if (len(marker.projections.keys())>=2):	
			markerPosition = chunk.transform.matrix.mulp(marker.position)
			markerPos = str(-(round(markerPosition[2], 4))) + "," + str(round(markerPosition[0], 4)) + "," + str(round(markerPosition[1], 4))
			markerInfo = markerLabel + "," + markerPos + ",\n"			
			f2.write(markerInfo)
			print(markerLabel + " " + markerPos)
		else:
			print(markerLabel+" < 2 projections.keys")
	f2.close()
	#return path
	
	
def ViewgaExportTrimble():
	print("\n-----ViewgaExportTrimble START-----")

	document = Metashape.app.document

	chunksSize = len(document.chunks)
	print("chunksSize: ", chunksSize)
	
	if(chunksSize<1):
		print("Error: chunks < 1")
		Metashape.app.messageBox("Error: chunks < 1")
		print("-----ViewgaExportTrimble STOP-----")
		return 0

	chunk = document.chunk
	print("chunk name used: ", chunk.label)

	if(chunk.enabled==False):
		print("Error: chunk.enabled = False")
		Metashape.app.messageBox("Error: chunk.enabled = False")
		print("-----ViewgaExportTrimble STOP-----")
		return 0
	else:
		if(len(chunk.cameras)<1):
			print("Error: len(chunk.cameras)<1")
			Metashape.app.messageBox("Error: len(chunk.cameras)<1")
			print("-----ViewgaExportTrimble STOP-----")
			return 0

	filepath = Metashape.app.getSaveFileName("Save Trimble File")
	print("export file path: ", filepath)

	if(filepath==""):
		print("Error: filepath False")
		Metashape.app.messageBox("Error: filepath False")
		print("-----ViewgaExportTrimble STOP-----")
		return 0

	pr = Metashape.app.getInt('projections minimum',3)
	err = Metashape.app.getFloat('pixel error',0.45)

	ExportTrimble(chunk,filepath,pr,err)
	
	#chunk.updateTransform()	

	print("-----ViewgaExportTrimble DONE-----")
	Metashape.app.messageBox("ViewgaExportTrimble DONE")


	
	
label1 = "Viewga/Import Trimble"
Metashape.app.addMenuItem(label1, ViewgaImportTrimble)
	
label2 = "Viewga/Export Trimble"
Metashape.app.addMenuItem(label2, ViewgaExportTrimble)