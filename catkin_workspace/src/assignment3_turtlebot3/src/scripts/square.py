#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt, pi


class TurtleBot:

	def __init__(self):
		# Creates a node with name 'turtlebot_controller' and make sure it is a
		# unique node (using anonymous=True).
		rospy.init_node('turtlebot_controller', anonymous=True)

		# Publisher which will publish to the topic '/turtle1/cmd_vel'.
		#self.velocity_publishern = rospy.Publisher('/turtle1/cmd_vel',
		self.velocity_publisher = rospy.Publisher('cmd_vel',
												  Twist, queue_size=10)

		# A subscriber to the topic '/turtle1/pose'. self.update_pose is called
		# when a message of type Pose is received.
		#self.pose_subscriber = rospy.Subscriber('/turtle1/pose',
		self.pose_subscriber = rospy.Subscriber('pose',
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

		i = 0

		print("hello1")

		#velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
		vel_msg = Twist()


		#Loop to move the turtle in an specified distance
		while(i < 5 and not rospy.is_shutdown()):

			print("i:")
			print(i)

			i = i + 1

			#
			vel_msg.linear.x = 0.2
			vel_msg.linear.y = 0
			vel_msg.linear.z = 0

			vel_msg.angular.x = 0
			vel_msg.angular.y = 0
			vel_msg.angular.z = 0


			#Setting the current time for distance calculus
			t0 = rospy.Time.now().to_sec()
			current_distance = 0

			#Loop to move the turtle in an specified distance
			while(current_distance < 2 and 
				  not rospy.is_shutdown()):
				#Publish the velocity
				self.velocity_publisher.publish(vel_msg)
				#Takes actual time to velocity calculus
				t1=rospy.Time.now().to_sec()
				#Calculates distancePoseStamped
				current_distance= 0.2*(t1-t0)
				print(current_distance)

			# Stopping our robot after the movement is over.
			vel_msg.linear.x = 0
			vel_msg.angular.z = 0
			self.velocity_publisher.publish(vel_msg)


			print("between")

			#
			vel_msg.linear.x = 0
			vel_msg.linear.y = 0
			vel_msg.linear.z = 0

			vel_msg.angular.x = 0
			vel_msg.angular.y = 0
			vel_msg.angular.z = 0.2


			#Setting the current time for distance calculus
			t0 = rospy.Time.now().to_sec()
			current_distance = 0

			#Loop to move the turtle in an specified distance
			while(current_distance < pi/2 and 
				  not rospy.is_shutdown()):
				#Publish the velocity
				self.velocity_publisher.publish(vel_msg)
				#Takes actual time to velocity calculus
				t1=rospy.Time.now().to_sec()
				#Calculates distancePoseStamped
				current_distance= 0.2*(t1-t0)
				print(current_distance)
					

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
