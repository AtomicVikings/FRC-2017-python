import wpilib
import logging
import ctre
from wpilib import RobotDrive

def main(auton_opt, robot_drive):
		if auton_opt == 1:
			auton_left(robot_drive)
		if auton_opt == 2:
			auton_middle(robot_drive)
		if auton_opt == 3:
			auton_right(robot_drive)
def auton_travel(dist, direc):
	"""
	dist = distance in feet
	direc 1 = x axis
	direc 2 = y axis
	direc 3 = z axis
	
	value before dist = seconds per foot
	"""
	if direc == 1:
		return 1/3 * dist
	if direc == 2:
		return 1/3 * dist
	if direc == 3:
		return 1/3 * dist
def auton_left(robot_drive):
	while wpilib.Timer.getMatchTime() < auton_travel(10, 1):
		robot_drive.mecanumDrive_Cartesian(0.5, 0, 0, 0)
	while wpilib.Timer.getMatchTime() < auton_travel(10, 1) + auton_travel(1/12, 3):
		robot_drive.mecanumDrive_Cartesian(0, 0, 0.5, 0)
	while wpilib.Timer.getMatchTime() < auton_travel(10, 1) + auton_travel(1/12, 3) + auton_travel(3, 2):
		robot_drive.mecanumDrive_Cartesian(0, 0.5, 0, 0)
def auton_middle(robot_drive):
	while wpilib.Timer.getMatchTime() < auton_travel(5, 2):
		robot_drive.mecanumDrive_Cartesian(0, 0.5, 0, 0)
def auton_right(robot_drive):
	while wpilib.Timer.getMatchTime() < auton_travel(10, 1):
		robot_drive.mecanumDrive_Cartesian(-0.5, 0, 0, 0)
	while wpilib.Timer.getMatchTime() < auton_travel(10, 1) + auton_travel(1/12, 3):
		robot_drive.mecanumDrive_Cartesian(0, 0, -0.5, 0)
	while wpilib.Timer.getMatchTime() < auton_travel(10, 1) + auton_travel(1/12, 3) + auton_travel(3, 2):
		robot_drive.mecanumDrive_Cartesian(0, 0.5, 0, 0)