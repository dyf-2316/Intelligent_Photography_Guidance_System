# -*- coding:utf-8 -*-
# @Time： 3/3/21 11:23 PM
# @Author: dyf-2316
# @FileName: Guidance.py
# @Software: PyCharm
# @Project: Intelligent_Photography_Guidance_System
# @Description: 人像模式指导的生成模块


from enum import Enum

from OpenposeAPI import get_pose_keypoints


class Portrait(Enum):
    WholeBody = 0
    UpperBody = 1
    UpperBreast = 2


class People:
    def __init__(self, pose_keypoint):
        body_seqs = ["Nose", "Neck", "RShoulder", "RElbow", "RWrist", "LShoulder", "LElbow", "LWrist", "MidHip",
                     "RHip", "RKnee", "RAnkle", "LHip", "LKnee", "LAnkle", "REye", "LEye", "REar", "LEar",
                     "LBigToe", "LSmallToe", "LHeel", "RBigToe", "RSmallToe", "RHeel"]
        self.body_points = {}
        for index, body_seq in enumerate(body_seqs):
            self.body_points[body_seq] = (pose_keypoint[index][0], pose_keypoint[index][1])

        if self.body_points['MidHip'] == (0, 0):
            self.mode = Portrait.UpperBreast
        elif self.body_points['RKnee'] == (0, 0) and self.body_points['LKnee'] == (0, 0):
            self.mode = Portrait.UpperBody
        else:
            self.mode = Portrait.WholeBody


class PortraitGuidance:
    def __init__(self):
        self.peopleList = []
        self.image_path = ""

    def input_photo(self, image_path):
        self.image_path = image_path
        self.extract_people_info()

    def extract_people_info(self):
        poseKeypoints = get_pose_keypoints(self.image_path)
        for poseKeypoint in poseKeypoints:
            self.peopleList.append(People(poseKeypoint))

    def output_photo(self):
        print('照片中的人物个数：', len(self.peopleList))
        for index, people in enumerate(self.peopleList):
            print('第', index + 1, '个人的姿势信息:')
            print("人像的策略模式：", people.mode)
            print(people.body_points)


guidance = PortraitGuidance()
guidance.input_photo("./source/自拍/3.jpg")
guidance.output_photo()

