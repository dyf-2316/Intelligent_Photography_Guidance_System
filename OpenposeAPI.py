# -*- coding:utf-8 -*-
# @Time： 3/3/21 11:39 PM
# @Author: dyf-2316
# @FileName: OpenposeAPI.py
# @Software: PyCharm
# @Project: Intelligent_Photography_Guidance_System
# @Description:
import os
import sys
import cv2
import argparse
from sys import platform

from matplotlib import pyplot as plt

try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Windows Import
        if platform == "win32":
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + '/../../python/openpose/Release')
            os.environ['PATH'] = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' + dir_path + '/../../bin;'
            import pyopenpose as op
        else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('../../python')
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the
            # OpenPose/python module from there. This will install OpenPose and the python library at your desired
            # installation path. Ensure that this is in your python path in order to use it. sys.path.append(
            # '/usr/local/python')
            from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this '
              'Python script in the right folder?')
        raise e

    def get_pose_keypoints(image_path):
        parser = argparse.ArgumentParser()
        parser.add_argument("--image_path", default=image_path,
                            help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
        args = parser.parse_known_args()

        params = dict()
        params["model_folder"] = "/Users/dyf/ml/cv/openpose/models"
        params["face"] = False
        params["hand"] = False
        #     params['write_json']="output/"

        for i in range(0, len(args[1])):
            curr_item = args[1][i]
            if i != len(args[1]) - 1:
                next_item = args[1][i + 1]
            else:
                next_item = "1"
            if "--" in curr_item and "--" in next_item:
                key = curr_item.replace('-', '')
                if key not in params:  params[key] = "1"
            elif "--" in curr_item and "--" not in next_item:
                key = curr_item.replace('-', '')
                if key not in params: params[key] = next_item

        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

        datum = op.Datum()
        imageToProcess = cv2.imread(args[0].image_path)
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop([datum])

        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(datum.cvOutputData, cv2.COLOR_BGR2RGB))

        return datum.poseKeypoints


except Exception as e:
    print(e)
    sys.exit(-1)
