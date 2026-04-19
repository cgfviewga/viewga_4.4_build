#v003
#on Windows:  C:/Users/<username>/AppData/Local/Agisoft/Metashape Pro/scripts/
#on Linux:  /home/<username>/.local/share/Agisoft/Metashape Pro/scripts/


   
import sys
import re
import os
import math

import Metashape


	
	
	
	
	
	
def GetDistancePoints3D(A, B):
	return math.sqrt(pow((B[0]-A[0]),2.0)+pow((B[1]-A[1]),2.0)+pow((B[2]-A[2]),2.0))


def RdmRefiner(chunk, points_dist, projection_min):
	chunk.crs = Metashape.CoordinateSystem('LOCAL_CS["Local CS",LOCAL_DATUM["Local Datum",0],UNIT["metre",1]]')
	mrkCounter = 0
	for mrk1 in chunk.markers:
		if(mrk1.label.startswith("vrdma_") and len(mrk1.projections) < projection_min):
			chunk.remove(mrk1)
		if(mrk1.label.startswith("vrdma_") and mrk1.position != None and len(mrk1.projections) >= projection_min):
			#print("m1 ++++" + mrk1.label + "   " + str(len(mrk1.projections)))
			mrk1.label="E_" + mrk1.label
			mrk = chunk.addMarker()
			mrk.label = "vrdm_" + str(mrkCounter)
			mrkCounter+=1
			mrk1Position = chunk.transform.matrix.mulp(mrk1.position)
			for cam in chunk.cameras:
				if(mrk1.projections[cam] != None):
					mrk.projections[cam] = mrk1.projections[cam]
			for mrk2 in chunk.markers:
				if(mrk2.label.startswith("vrdma_") and mrk2.position != None and len(mrk2.projections) >= projection_min):
					#print("m2 ====" + mrk2.label + "   " + str(len(mrk2.projections)))
					mrk2Position = chunk.transform.matrix.mulp(mrk2.position)
					dist = GetDistancePoints3D(mrk1Position, mrk2Position)
					if(dist > 0 and dist < points_dist):
						#print("m2 ====" + mrk2.label + "   " + str(dist))
						mrk2.label="E_" + mrk1.label + "_" + mrk2.label
						for cam in chunk.cameras:
							if(mrk2.projections[cam] != None):
								mrk.projections[cam] = mrk2.projections[cam]
						chunk.remove(mrk2)
							#print(cam.label + "    " + str(mrk1.projections[cam] ) + "    " + str(mrk1.projections[cam] == None))
			chunk.remove(mrk1)
		#print("m1 ----" + mrk1.label + "   " + str(len(mrk1.projections)))

	
	
def ViewgaRdmRefiner():
	print("\n-----ViewgaRdmRefiner START-----")
	
	document = Metashape.app.document
	
	chunksSize = len(document.chunks)
	print("chunksSize: ", chunksSize)
	
	if(chunksSize<1):
		print("Error: chunks < 1")
		Metashape.app.messageBox("Error: chunks < 1")
		print("-----ViewgaRdmRefiner STOP-----")
		return 0
	
	chunk = document.chunk
	print("chunk name used: ", chunk.label)
	
	if(chunk.enabled==False):
		print("Error: chunk.enabled = False")
		Metashape.app.messageBox("Error: chunk.enabled = False")
		print("-----ViewgaRdmRefiner STOP-----")
		return 0
	
	points_dist = Metashape.app.getInt('Points distance (cm)', 2) / 100
	projection_min = Metashape.app.getInt('Projection min', 3)
	
	RdmRefiner(chunk, points_dist, projection_min)
	
	print("-----ViewgaRdmRefiner DONE-----")
	Metashape.app.messageBox("ViewgaRdmRefiner DONE")






def RdmExport(chunk, filePath):
	chunk.crs = Metashape.CoordinateSystem("LOCAL_CS['Local CS',LOCAL_DATUM['Local Datum',0],UNIT['metre',1]]")
	
	f2 = open(filePath + ".vmap", 'w')
	
	f2.write("rename_points\n\n")
	
	f2.write("marker_name:	marker_01\n")
	f2.write("marker_type:	top\n")

	for mrk in chunk.markers:
		if(mrk.label.startswith("vrdm_") and mrk.position != None and len(mrk.projections) > 2):
			#print("m1 ++++" + mrk.label + "   " + str(len(mrk.projections)))
			mrkPos = chunk.transform.matrix.mulp(mrk.position)
			mrkPosStr = str(-round(mrkPos[2], 4)) + "," + str(round(mrkPos[0], 4)) + "," + str(round(mrkPos[1], 4))
			markerInfo = mrk.label + "," + mrkPosStr + ",\n"			
			f2.write(markerInfo)
		#print("m1 ----" + mrk.label + "   " + str(len(mrk.projections)))








def ViewgaRdmExport():
	print("\n-----ViewgaRdmExport START-----")
	
	document = Metashape.app.document
	
	chunksSize = len(document.chunks)
	print("chunksSize: ", chunksSize)
	
	if(chunksSize<1):
		print("Error: chunks < 1")
		Metashape.app.messageBox("Error: chunks < 1")
		print("-----ViewgaRdmExport STOP-----")
		return 0
	
	chunk = document.chunk
	print("chunk name used: ", chunk.label)
	
	if(chunk.enabled==False):
		print("Error: chunk.enabled = False")
		Metashape.app.messageBox("Error: chunk.enabled = False")
		print("-----ViewgaRdmExport STOP-----")
		return 0
		
	filepath = Metashape.app.getSaveFileName("Save Survey File")
	print("export file path: ", filepath)

	if(filepath==""):
		print("Error: filepath False")
		Metashape.app.messageBox("Error: filepath False")
		print("-----ViewgaRdmExport STOP-----")
		return 0
	
	RdmExport(chunk, filepath)
	
	print("-----ViewgaRdmExport DONE-----")
	Metashape.app.messageBox("ViewgaRdmExport DONE")






label1 = "Viewga/RdmRefiner"
Metashape.app.addMenuItem(label1, ViewgaRdmRefiner)

label1 = "Viewga/RdmExport"
Metashape.app.addMenuItem(label1, ViewgaRdmExport)
