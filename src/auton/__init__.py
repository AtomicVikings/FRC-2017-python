import wpilib
import logging
import ctre
import time
from wpilib import RobotDrive

def main(auton_opt, robot_drive):
		time_var = time.time()
		#if auton_opt == 5:
		#	auton_left(robot_drive, time_var)
		if auton_opt == 2:
			auton_middle(robot_drive, time_var)
		if auton_opt == 1:
			auton_line(robot_drive, time_var)
		#if auton_opt == 5:
		#	auton_right(robot_drive, time_var)
		#if auton_opt == 5:
		#	auton_debug(robot_drive, time_var)
def auton_travel(dist, direc):
	"""
	dist = distance in inch
	direc 1 = x axis
	direc 2 = y axis
	direc 3 = z axis
	
	value before dist = seconds per inch
	"""
	if direc == 1:
		return 1/3 * dist
	if direc == 2:
		return 1/100 * dist
	if direc == 3:
		return 1/3 * dist
def auton_left(robot_drive, time_var):
	while wpilib.Timer.getMatchTime() < auton_travel(10, 1):
		robot_drive.mecanumDrive_Cartesian(0.5, 0, 0, 0)
	while wpilib.Timer.getMatchTime() < auton_travel(10, 1) + auton_travel(1/12, 3):
		robot_drive.mecanumDrive_Cartesian(0, 0, 0.3, 0)
	while wpilib.Timer.getMatchTime() < auton_travel(10, 1) + auton_travel(1/12, 3) + auton_travel(3, 2):
		robot_drive.mecanumDrive_Cartesian(0, 0.5, 0, 0)
		
def auton_middle(robot_drive, time_var):
	while time.time() - time_var < 2: #auton_travel(115, 1):
		robot_drive.mecanumDrive_Cartesian(0.4, 0, 0, 0)
	while time.time() - time_var < 15.5: #auton_travel(115, 1) + 1:
		robot_drive.mecanumDrive_Cartesian(0, 0, 0, 0)
		
def auton_line(robot_drive, time_var):
	while time.time() - time_var < 4: #auton_travel(115, 1):
		robot_drive.mecanumDrive_Cartesian(0.4, 0, 0, 0)
	while time.time() - time_var < 5:
		robot_drive.mecanumDrive_Cartesian(0, 0, 0, 0)
	while time.time() - time_var < 9:
		robot_drive.mecanumDrive_Cartesian(-0.4, 0, 0, 0)
	while time.time() - time_var < 15.5: #auton_travel(115, 1) + 1:
		robot_drive.mecanumDrive_Cartesian(0, 0, 0, 0)

def auton_right(robot_drive, time_var):
	while wpilib.Timer.getMatchTime() < auton_travel(10, 1):
		robot_drive.mecanumDrive_Cartesian(-0.5, 0, 0, 0)
	while wpilib.Timer.getMatchTime() < auton_travel(10, 1) + auton_travel(1/12, 3):
		robot_drive.mecanumDrive_Cartesian(0, 0, -0.3, 0)
	while wpilib.Timer.getMatchTime() < auton_travel(10, 1) + auton_travel(1/12, 3) + auton_travel(3, 2):
		robot_drive.mecanumDrive_Cartesian(0, 0.5, 0, 0)
		
def auton_debug(robot_drive, time_var):
	while wpilib.Timer.getMatchTime() < 1:
		robot_drive.mecanumDrive_Cartesian(0.9,0,0,0) # 0.8
		
		
