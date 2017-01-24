import wpilib
import logging
import ctre

#P is proportional. It is literally how far away you are from your setpoint.
#I is integral. It is the sum of all P values, and acculumates over time.
#D is derivative. It is the "slope" or the change in P from the last loop.
#F is used as the Kv constant for velocity feed-forward. Typically this is hardcoded to the a particular slot, but you are free gain schedule if need be.

from wpilib import RobotDrive

class MyRobot(wpilib.IterativeRobot):
	#0-3 pwm mecanum reserved
	lf_motor = 0 #left front motor
	rf_motor = 1 #right front motor
	lr_motor = 2 #left rear motor
	rr_motor = 3 #right rear motor
	
	joystick_channel = 0
	
	def robotInit(self):
		self.robot_drive = wpilib.RobotDrive(self.lf_motor, self.rf_motor, self.lr_motor, self.rr_motor)
		
		self.robot_drive.setExpiration(0.1)
		self.robot_drive.setInvertedMotor(RobotDrive.MotorType.kFrontLeft, True)
		self.robot_drive.setInvertedMotor(RobotDrive.MotorType.kRearLeft, True)
		
		self.xbox =  wpilib.XboxController(self.joystick_channel)
		
		
	def autonomousInit(self):
		self.auto_loop_counter = 0
	def autonomousPeriodic(self):
		timer = wpilib.Timer()
		timer.start()
	def teleopPeriodic(self):
		while self.isOperatorControl() and self.isEnabled():
			
			if self.xbox.getRawButton(9) == True:
				self.robot_drive.mecanumDrive_Cartesian(self.xbox.getRawAxis(1), self.xbox.getRawAxis(0), self.xbox.getRawButton(6)-self.xbox.getRawButton(5), 0 ) 
			else:
				self.robot_drive.mecanumDrive_Cartesian(-self.xbox.getRawAxis(1), -self.xbox.getRawAxis(0), -self.xbox.getRawButton(5)-self.xbox.getRawButton(6), 0 ) 
				
				
		wpilib.Timer.delay(0.005)		
	def testPeriodic(self):
		wpilib.LiveWindow.run()
	
if __name__ == "__main__":
	wpilib.run(MyRobot, physics_enabled = False)
	
