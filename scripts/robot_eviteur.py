#!/usr/bin/env python
# coding: utf-8
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import numpy as np

VIT_AVANT = 0.3
VIT_TOURNE = 0.2
SEUIL = 1  # On détecte un obstacle quand il est à moins de SEUIL m
ANGLE_DETECTION = 30  # On regarde devant dans unintervalle de [-ANGLE_DETECTION° , ANGLE_DETECTION°]
DROITE = -1
GAUCHE = 1

class RobotEviteur:
    def __init__(self):
        rospy.init_node('detection_obstacle')
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=5)
        rospy.Subscriber("/scan", LaserScan, self.traiterScan)
        self.twist = Twist()
        self.twist.linear.y = 0;
        self.twist.linear.z = 0
        self.twist.angular.x = 0;
        self.twist.angular.y = 0;

    def stop(self):
        self.twist.linear.x = 0;
        self.twist.angular.z = 0
        self.pub.publish(self.twist)

    def move(self):
        self.twist.linear.x = VIT_AVANT;
        self.twist.angular.z = 0
        self.pub.publish(self.twist)

    def turn(self,sens):
        self.twist.linear.x = 0;
        self.twist.angular.z = sens * VIT_TOURNE
        self.pub.publish(self.twist)

    def traiterScan(self, scan):
        ranges = np.array(scan.ranges)  # Toutes les données (720 pt , 4pt / °)
        bInf = int(len(ranges)/2 - ANGLE_DETECTION * 4)
        bSup = int(len(ranges)/2 + ANGLE_DETECTION * 4)
        ranges = ranges[bInf:bSup]   # On ne garde que les pt dans le champ de détection
        plusProche = np.argmin(ranges)
        if ranges[plusProche] < SEUIL:  # Il y a un obstacle
            if plusProche > int(len(ranges)/2):  # il est à droite
                self.turn(GAUCHE)
            else:
                self.turn(DROITE)
        else:
            self.move()  # Pas d'obstacle, on avance


if __name__ == "__main__":
    robot = RobotEviteur()
    try:
        while True:
            rospy.sleep(0.1)
    except Exception as e:
        print(e)
    finally:
        robot.stop()
