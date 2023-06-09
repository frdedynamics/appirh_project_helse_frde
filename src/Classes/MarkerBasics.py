#!/usr/bin/env python3

import rospy
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
import tf
import numpy
from std_msgs.msg import String
from gazebo_msgs.msg import ContactsState
import math

class MarkerBasics(object):
    def __init__(self, topic_id, type="arm"):
        marker_topic = topic_id+'marker'
        self.marker_objectlisher = rospy.Publisher(marker_topic, Marker, queue_size=1)
        self.rate = rospy.Rate(25)
        if type == "arm":
            self.init_arm_marker(index=0)
        elif type == "score":
            self.init_score_marker()
        elif type == "regular_str":
            text = " "
            self.init_str_marker(text)
        elif type == "progress_bar":
            self.init_bar_marker()
        else:
            raise NameError("Marker basic type is not defined properly")


    def init_arm_marker(self, index=0):
        self.marker_object = Marker()
        self.change_frame(frame="human_base_link", index=0)
        self.marker_object.type = Marker.ARROW
        self.marker_object.action = Marker.ADD
        self.marker_object.scale.x = 0.4
        self.marker_object.scale.y = 0.1
        self.marker_object.scale.z = 0.1

        self.marker_object.color.r = 50
        self.marker_object.color.g = 0
        self.marker_object.color.b = 255
        # This has to be, otherwise it will be transparent
        self.marker_object.color.a = 1.0


        # self.change_position(x=0.0, y=0.0, z=0.0)
        # self.change_orientation(pitch=0.0, yaw=0.0)
        # self.change_scale()
        # self.change_colour(R=1.0, G=0.0, B=0.0)

        # If we want it for ever, 0, otherwise seconds before desapearing
        self.marker_object.lifetime = rospy.Duration(0)
    

    def init_score_marker(self):
        self.marker_idx = 0
        self.marker_object = Marker()
        for i in range(1):
            # self.marker_object.clear()
            self.marker_object.header.frame_id = "human_base_link"
            self.marker_object.type = self.marker_object.TEXT_VIEW_FACING
            self.marker_object.text = str(600)
            self.marker_object.action = self.marker_object.ADD
            self.marker_object.scale.x = 1.0
            self.marker_object.scale.y = 1.0
            self.marker_object.scale.z = 1.0
            self.marker_object.color.a = 1.0
            self.marker_object.color.r = 1.0
            self.marker_object.color.g = 0.0
            self.marker_object.color.b = 1.0
            self.marker_object.pose.orientation.w = 1.0
            self.marker_object.pose.position.x = 1.5
            self.marker_object.pose.position.y = 1.5
            self.marker_object.pose.position.z = 1.5
            self.marker_object.id = i
    
    def update_score_marker(self, score):
        self.marker_object.text = str(score)

    
    def init_str_marker(self, text="*"):
        self.marker_idx = 1
        self.marker_object = Marker()
        for i in range(1):
            # self.marker_object.clear()
            self.marker_object.header.frame_id = "human_base_link"
            self.marker_object.type = self.marker_object.TEXT_VIEW_FACING
            self.marker_object.text = text
            self.marker_object.action = self.marker_object.ADD
            self.marker_object.scale.x = 0.4
            self.marker_object.scale.y = 0.4
            self.marker_object.scale.z = 0.4
            self.marker_object.color.a = 1.0
            self.marker_object.color.r = 1.0
            self.marker_object.color.g = 0.0
            self.marker_object.color.b = 1.0
            self.marker_object.pose.orientation.w = 1.0
            self.marker_object.pose.position.x = 0.0
            self.marker_object.pose.position.y = 0.0
            self.marker_object.pose.position.z = 1.2
            self.marker_object.id = i

    def init_bar_marker(self):
        self.marker_idx = 1
        self.marker_object = Marker()
        for i in range(1):
            # self.marker_object.clear()
            self.marker_object.header.frame_id = "human_base_link"
            self.marker_object.type = self.marker_object.CYLINDER
            self.marker_object.action = self.marker_object.ADD
            self.marker_object.scale.x = 0.4
            self.marker_object.scale.y = 0.4
            self.marker_object.scale.z = 0.4
            self.marker_object.color.a = 1.0
            self.marker_object.color.r = 1.0
            self.marker_object.color.g = 0.0
            self.marker_object.color.b = 1.0
            self.marker_object.pose.orientation.w = 1.0
            self.marker_object.pose.position.x = 0.0
            self.marker_object.pose.position.y = 0.0
            self.marker_object.pose.position.z = 1.2
            self.marker_object.id = i
            
    
    def update_str_marker(self, text, R=255, G=255, B=255):

        # R = 1.0
        # G = 0.0
        # B = 0.0
        # really no idea why it doesn't accept 255 and gives black if the value is not 1.0. But, well...
        self.marker_object.text = text
        self.marker_object.color.a = 1.0
        self.marker_object.color.r = R/255
        self.marker_object.color.g = G/255
        self.marker_object.color.b = B/255


    def change_orientation(self, pitch, yaw):
        """
        Roll doesnt make any sense in an arrow
        :param pitch: Up Down. We clip it to values [-1.5708,1.5708]
        :param yaw: Left Right , No clamp
        :return:
        """
        pitch = numpy.clip(pitch, -1.5708,1.5708)

        q = tf.transformations.quaternion_from_euler(0.0, pitch, yaw)

        self.marker_object.pose.orientation.x = q[0]
        self.marker_object.pose.orientation.y = q[1]
        self.marker_object.pose.orientation.z = q[2]
        self.marker_object.pose.orientation.w = q[3]


    def change_position(self, x, y, z):
        """
        Position of the starting end of the arrow
        :param x:
        :param y:
        :param z:
        :return:
        """

        my_point = Point()
        my_point.x = x
        my_point.y = y
        my_point.z = z
        self.marker_object.pose.position = my_point
        #rospy.loginfo("PositionMarker-X="+str(self.marker_object.pose.position.x))


    def set_visible(self, transparancy=1.0):
        self.marker_object.color.a = transparancy


    def set_invisible(self):
        self.marker_object.color.a = 0.0


    def change_colour(self, R, G, B, a=1.0):
        """
        All colours go from [0.0,1.0].
        :param R:
        :param G:
        :param B:
        :return:
        """

        self.marker_object.color.r = R/255.0
        self.marker_object.color.g = G/255.0
        self.marker_object.color.b = B/255.0
        # This has to be, otherwise it will be transparent
        self.marker_object.color.a = a

        # print(R, "--", G, "--", B, "--")


    def change_scale(self, s_x=0.4, s_y=0.4, s_z=0.1):
        """
        :param s_x:
        :param s_y:
        :param s_z:
        :return:
        """

        self.marker_object.scale.x = s_x
        self.marker_object.scale.y = s_y
        self.marker_object.scale.z = s_z


    def change_frame(self, frame, ns="human", index=0):
        """
        :param frame:
        :return:
        """
        self.marker_object.header.frame_id = frame
        self.marker_object.header.stamp = rospy.get_rostime()
        self.marker_object.ns = ns
        self.marker_object.id = index


    def update_marker(self, frame, ns, index, position, orientation, pressure, min_pressure=0.0, max_pressure=10.0):
        """
        :param position: [X,Y,Z] in the world frame
        :param pressure: Magnitude
        :param orientation: [Pitch,Yaw]
        :return:
        """
        #self.change_frame(frame=frame, ns=ns, index=index)
        self.change_position(x=position[0], y=position[1], z=position[2])
        self.change_orientation(pitch=orientation[0], yaw=orientation[1])
        self.change_scale(s_x = pressure)

        R,G,B = self.pressure_to_wavelength_to_rgb(pressure=pressure,
                                                   min_pressure=min_pressure,
                                                   max_pressure=max_pressure,
                                                   gamma=0.8)

        rospy.logdebug("R,G,B=["+str(R)+", "+str(G)+", "+str(B)+"]")

        self.change_colour(R=R, G=G, B=B)

        self.marker_objectlisher.publish(self.marker_object)