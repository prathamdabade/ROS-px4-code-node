#! /usr/bin/env python

import rospy
import mavros
from math import pi
from math import cos,sin
from geometry_msgs.msg import TwistStamped

rospy.init_node("circle_node", anonymous=True)
r = rospy.Rate(20)

def draw():
  vel_pub = rospy.Publisher("/mavros/setpoint_velocity/cmd_vel",TwistStamped, queue_size=20)

  t0  = rospy.Time.now().to_sec()
  vel = TwistStamped()
  speed = 2
  radius = float(input("Input radius"))
  angle = 0
  while angle<2*pi:
    vel.twist.linear.x = speed*(cos(angle))
    vel.twist.linear.y = speed*(sin(angle)) 
    t1 = rospy.Time.now().to_sec()
    vel_pub.publish(vel)
    angle = speed*(t1-t0)/radius
    r.sleep()

if __name__ == "__main__":
  try:
    draw()
  except rospy.ROSInterruptException:
    pass

    
