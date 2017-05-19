#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qgmap import *

if __name__ == '__main__' :
	import sys

	def goCoords() :
		def resetError() :
			coordsEdit.setStyleSheet('')
		try : latitude, longitude = coordsEdit.text().split(",")
		except ValueError :
			coordsEdit.setStyleSheet("color: red;")
			QtCore.QTimer.singleShot(500, resetError)
		else :
			gmap.centerAt(latitude, longitude)
			gmap.moveMarker("MyDragableMark", latitude, longitude)

	def goAddress() :
		def resetError() :
			addressEdit.setStyleSheet('')
		coords = gmap.centerAtAddress(addressEdit.text())
		if coords is None :
			addressEdit.setStyleSheet("color: red;")
			QtCore.QTimer.singleShot(500, resetError)
			return
		gmap.moveMarker("MyDragableMark", *coords)
		coordsEdit.setText("{}, {}".format(*coords))

	def onMarkerMoved(key, latitude, longitude) :
		print("Moved!!", key, latitude, longitude)
		coordsEdit.setText("{}, {}".format(latitude, longitude))
	def onMarkerRClick(key) :
		print("RClick on ", key)
		gmap.setMarkerOptions(key, draggable=False)
	def onMarkerLClick(key) :
		print("LClick on ", key)
	def onMarkerDClick(key) :
		print("DClick on ", key)
		gmap.setMarkerOptions(key, draggable=True)

	def onMapMoved(latitude, longitude) :
		print("Moved to ", latitude, longitude)
	def onMapRClick(latitude, longitude) :
		print("RClick on ", latitude, longitude)
	def onMapLClick(latitude, longitude) :
		print("LClick on ", latitude, longitude)
	def onMapDClick(latitude, longitude) :
		print("DClick on ", latitude, longitude)

	app = QtWidgets.QApplication(sys.argv)
	w = QtWidgets.QDialog()
	h = QtWidgets.QVBoxLayout(w)
	l = QtWidgets.QFormLayout()
	h.addLayout(l)

	addressEdit = QtWidgets.QLineEdit()
	l.addRow('Address:', addressEdit)
	addressEdit.editingFinished.connect(goAddress)
	coordsEdit = QtWidgets.QLineEdit()
	l.addRow('Coords:', coordsEdit)
	coordsEdit.editingFinished.connect(goCoords)
	gmap = QGoogleMap(w)
	gmap.mapMoved.connect(onMapMoved)
	gmap.markerMoved.connect(onMarkerMoved)
	gmap.mapClicked.connect(onMapLClick)
	gmap.mapDoubleClicked.connect(onMapDClick)
	gmap.mapRightClicked.connect(onMapRClick)
	gmap.markerClicked.connect(onMarkerLClick)
	gmap.markerDoubleClicked.connect(onMarkerDClick)
	gmap.markerRightClicked.connect(onMarkerRClick)
	h.addWidget(gmap)
	gmap.setSizePolicy(
		QtWidgets.QSizePolicy.MinimumExpanding,
		QtWidgets.QSizePolicy.MinimumExpanding)
	w.showFullScreen()

	gmap.waitUntilReady()

	#gmap.centerAt(41.35,2.05)
	gmap.setZoom(15)
	coords = gmap.centerAtAddress("Lima Peru")
	# Many icons at: https://sites.google.com/site/gmapsdevelopment/
	gmap.addMarker("MyDragableMark", *coords, **dict(
		icon="http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png",
		draggable=True,
		title = "Move me!"
		))

	# Some Static points
	for place in [
		"Plaza Ramon Castilla",
		"Plaza San Martin",
		]:
		gmap.addMarkerAtAddress(place,
			icon="http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_gray.png",
			)

	#gmap.setZoom(15)



	sys.exit(app.exec_())



