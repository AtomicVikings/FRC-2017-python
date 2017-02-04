import wpilib
import logging
import ctre
import auton
import math
from wpilib import RobotDrive

# https://github.com/robotpy/robotpy-ctre/blob/master/examples/CANTalonPID/robot.py
# https://github.com/robotpy/robotpy-ctre/blob/master/examples/CANTalonVelocityClosedLoop/robot.py


#P is proportional. It is literally how far away you are from your setpoint.
#I is integral. It is the sum of all P values, and acculumates over time.
#D is derivative. It is the "slope" or the change in P from the last loop.
#F is used as the Kv constant for velocity feed-forward. Typically this is hardcoded to the a particular slot, but you are free gain schedule if need be.

class MyRobot(wpilib.IterativeRobot):
	#0-3 pwm mecanum reserved
	lf_motor 		= 0 #left front motor (0)
	rf_motor 		= 1 #right front motor (1)
	lr_motor 		= 2 #left rear motor (3)
	rr_motor 		= 3 #right rear motor (2)

	# These are mechs (pwm) 
	climer_motor 	= 4 # Motor used for climming (Sparks)
	intake_motor	= 5 # Motor for the inkate mech (Sparks)
	ha_motor		= 6 # Motor used to agitat the hopper(Victor)	

	# Mechs can
	shooter_motor	= 1 # motor used to shoot the balls (Talon SRX)

	potChannel		= 1 # Pot channel used to get auton.
	
	js_channel 		= 0
	
	def robotInit(self):
		self.robot_drive = wpilib.RobotDrive(wpilib.Spark(self.lf_motor), wpilib.Spark(self.rf_motor), wpilib.Spark(self.lr_motor), wpilib.Spark(self.rr_motor))
		
		self.robot_drive.setExpiration(0.1)
		#self.robot_drive.setInvertedMotor(RobotDrive.MotorType.kFrontLeft, True)
		self.robot_drive.setInvertedMotor(RobotDrive.MotorType.kRearLeft, True)
		#self.robot_drive.setInvertedMotor(RobotDrive.MotorType.kFrontRight, True)
		self.robot_drive.setInvertedMotor(RobotDrive.MotorType.kRearRight, True)
		
		self.js 		= wpilib.Joystick(self.js_channel)

		# Mechs
		self.climer 	= wpilib.Spark(self.climer_motor)
		self.intake 	= wpilib.Spark(self.intake_motor)
		self.shootor 	= ctre.cantalon.CANTalon(self.shooter_motor, controlPeriodMs=10, enablePeriodMs=50)
		self.ha 		= wpilib.Victor(self.ha_motor)		

		self.pot		= wpilib.AnalogInput(self.potChannel) 
		
	def autonomousInit(self):
		self.auto_loop_counter = 0
	def autonomousPeriodic(self):
		timer = wpilib.Timer()
		timer.start()
		auton.main(int(math.floor((self.pot.getVoltage() / 5) * 2 + 1.5)), self.robot_drive) #auton_opt 1 = start left, 2 = middle, 3 = right
	def teleopPeriodic(self):
		while self.isOperatorControl() and self.isEnabled():
			
			self.robot_drive.mecanumDrive_Cartesian(self.js.getX(), self.js.getY(), -self.js.getZ(), 0) 
		
			if self.js.getRawButton(2) == True:
				self.climer.set(.76)	#  -1.0 to 1.0
			else:
				self.climer.set(0)

			if self.js.getRawButton(3) == True:
				self.intake.set(.5)	#  -1.0 to 1.0
			else:
				self.intake.set(0)

			if self.js.getRawButton(4) == True:
				self.ha.set(.5)	#  -1.0 to 1.0
			else:
				self.ha.set(0)

		# was 0.005
		wpilib.Timer.delay(0.003)		
	def testPeriodic(self):
		wpilib.LiveWindow.run()
	
if __name__ == "__main__":
	wpilib.run(MyRobot, physics_enabled = False)
