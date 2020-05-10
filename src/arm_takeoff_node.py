#!/usr/bin/env python

import rospy
import mavros
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, SetMode


current_State = State()

def callback(msg):
  global current_State
  current_State = msg
  
def main():
  global current_State

  rospy.init_node('offboard', anonymous=True)
  r = rospy.Rate(20)
  pos_pub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size=20)
  rospy.Subscriber('/mavros/state', State, callback)
  arming = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
  setmode = rospy.ServiceProxy('/mavros/set_mode', SetMode)

  pos = PoseStamped()
  height = float(input("Enter takeoff Height:"))
  pos.pose.position.z = height
  prev_state = current_State

  for _i in range(50):
    pos_pub.publish(pos)
    r.sleep()

  while not current_State.connected:
    r.sleep()
  
  t0 = rospy.get_rostime()

  while not rospy.is_shutdown():
    now = rospy.get_rostime()

    if current_State.mode != "OFFBOARD" and (now-t0 > rospy.Duration(5)):
      setmode(base_mode=0, custom_mode="OFFBOARD")
      t0=now

    else:
      if not current_State.armed and(now-t0 > rospy.Duration(5)):
        arming(True)
        t0=now

    if prev_state.armed != current_State.armed:
      rospy.loginfo("Vehicle armed: %r" % current_State.armed)
    if prev_state.mode != current_State.mode:
      rospy.loginfo("current mode: %s" % current_State.mode)
    prev_state = current_State

    pos.header.stamp = rospy.Time.now()
    pos_pub.publish(pos)
    
    r.sleep()

if __name__ == "__main__":
  try:
    main()
  except rospy.ROSInterruptException:
    pass