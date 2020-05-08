#! /usr/bin/env python

import rospy
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool
from mavros_msgs.srv import CommandTOL

def arm():
  rospy.wait_for_service('/mavros/cmd/arming')
  try:
    arm = rospy.ServiceProxy('/mavros/cmd/arming',CommandBool)
    arm(True)
  except rospy.ServiceException:
    print('could not arm')


def takeoff():
  rospy.wait_for_service('/mavros/cmd/takeoff')
  try:
    takeoff = rospy.ServiceProxy('/mavros/cmd/takeoff',CommandTOL)
    takeoff(altitude=10)
  except rospy.ServiceException:
    print('could not takeoff')

def main():
  pass



if __name__ == "__main__":
  try:
    main()
  except rospy.ROSInterruptException:
    pass