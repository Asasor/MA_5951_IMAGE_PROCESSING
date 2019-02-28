#!/usr/bin/env python3
#
# This is a demo program showing CameraServer usage with OpenCV to do image
# processing. The image is acquired from the USB camera, then a rectangle
# is put on the image and sent to the dashboard. OpenCV has many methods
# for different types of processing.
#
# Warning: If you're using this with a python-based robot, do not run this
# in the same program as your robot code!
#

import cv2
import numpy as np
from networktables import NetworkTables
from cscore import CameraServer, UsbCamera, CvSource
from networktables import NetworkTablesInstance


def main():
    img = np.zeros(shape=(480, 640, 3), dtype=np.uint8)

    cs = CameraServer.getInstance()
    cs.enableLogging()

    camera0 = cs.startAutomaticCapture(dev=0)
    camera1 = UsbCamera("cam1", 1)
    camera2 = UsbCamera("cam2", 2)

    # Get a CvSink. This will capture images from the camera
    cvSink = cs.getVideo()

    cvSink.setSource(camera0)

    # (optional) Setup a CvSource. This will send images back to the Dashboard
    smartDash = networktables.NetworkTables.getTable('SmartDashboard')

    def _listener(source, key, value, isNew):
        if value == 0:
            cvSink.setSource(camera0)
        elif value == 1:
            cvSink.setSource(camera1)
        elif value == 2:
            cvSink.setSource(camera2)

    smartDash.putNumber("Num", 0)
    outputStream = cs.putVideo("Out", 320, 240)

    while True:

        smartDash.addEntryListener(_listener, key="Num")
        time, img = cvSink.grabFrame(img)
        if time == 0:
            # Send the error.
            outputStream.notifyError(cvSink.getError())
            # skip the rest of the current iteration
            continue

        # display a new image on the outputStream
        outputStream.putFrame(img)


if __name__ == "__main__":

    # To see messages from networktables, you must setup logging
    import logging

    logging.basicConfig(level=logging.DEBUG)

    # You should uncomment these to connect to the RoboRIO
    import networktables
    networktables.NetworkTables.initialize(server='10.59.51.2')

    main()
