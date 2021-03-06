#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt


###
### Couldn't get it to draw a square, but it would go to correct coordinates
### for lower values
###

class TurtleBot:

	def __init__(self):
		# Creates a node with name 'turtlebot_controller' and make sure it is a
		# unique node (using anonymous=True).
		rospy.init_node('turtlebot_controller', anonymous=True)

		# Publisher which will publish to the topic '/turtle1/cmd_vel'.
		self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',
												  Twist, queue_size=10)

		# A subscriber to the topic '/turtle1/pose'. self.update_pose is called
		# when a message of type Pose is received.
		self.pose_subscriber = rospy.Subscriber('/turtle1/pose',
												Pose, self.update_pose)

		self.pose = Pose()
		self.rate = rospy.Rate(10)

	def update_pose(self, data):
		"""Callback function which is called when a new message of type Pose is
		received by the subscriber."""
		self.pose = data
		self.pose.x = round(self.pose.x, 4)
		self.pose.y = round(self.pose.y, 4)

	def euclidean_distance(self, goal_pose):
		"""Euclidean distance between current pose and the goal."""
		return sqrt(pow((goal_pose.x - self.pose.x), 2) +
					pow((goal_pose.y - self.pose.y), 2))

	def linear_vel(self, goal_pose, constant=1.5):
		"""See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
		return constant * self.euclidean_distance(goal_pose)

	def steering_angle(self, goal_pose):
		"""See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
		return atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)

	def angular_vel(self, goal_pose, constant=6):
		"""See video: https://www.youtube.com/watch?v=Qh15Nol5htM."""
		return constant * (self.steering_angle(goal_pose) - self.pose.theta)

	def move2goal(self):
		"""Moves the turtle to the goal."""
		goal_pose = Pose()

		# Get the input from the user.
		#goal_pose.x = float(input("Set your x goal: "))
		#goal_pose.x = rospy.get_param('~x')
		#goal_pose.y = float(input("Set your y goal: "))
		#goal_pose.y = rospy.get_param('~y')

		# Please, insert a number slightly greater than 0 (e.g. 0.01).
		#distance_tolerance = float(input("Set your tolerance: "))
		#distance_tolerance = rospy.get_param('~tol')
		distance_tolerance = 0.5

		x_array = [5,8,8,5,5]
		y_array = [5,5,8,8,5]
		
		#x_array = [0,1,2,3,4]
		#y_array = [0,1,2,3,4]

		#x_array = [3,5,5,3,3]
		#y_array = [3,3,5,5,3]

		i = 0

		vel_msg = Twist()

		while (i < 5 and
			   not rospy.is_shutdown()):

			# Get the input from the user.
			goal_pose.x = x_array[i]
			#goal_pose.x = rospy.get_param('~x')
			goal_pose.y = y_array[i]

			while (self.euclidean_distance(goal_pose) > distance_tolerance and
				   not rospy.is_shutdown()):

				# Porportional controller.
				# https://en.wikipedia.org/wiki/Proportional_control

				# Linear velocity in the x-axis.
				vel_msg.linear.x = self.linear_vel(goal_pose)
				vel_msg.linear.y = 0
				vel_msg.linear.z = 0

				# Angular velocity in the z-axis.
				vel_msg.angular.x = 0
				vel_msg.angular.y = 0
				vel_msg.angular.z = self.angular_vel(goal_pose)


				#print(vel_msg.angular.x)
				#print(vel_msg.angular.z)

				# Publishing our vel_msg
				self.velocity_publisher.publish(vel_msg)

				# Publish at the desired rate.
				self.rate.sleep()

			i = i + 1

		# Stopping our robot after the movement is over.
		vel_msg.linear.x = 0
		vel_msg.angular.z = 0
		self.velocity_publisher.publish(vel_msg)

		# If we press control + C, the node will stop.
		rospy.spin()

if __name__ == '__main__':
	try:
		x = TurtleBot()
		x.move2goal()
	except rospy.ROSInterruptException:
		pass
