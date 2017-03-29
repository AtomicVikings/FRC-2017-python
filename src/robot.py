# Look up on steam
# leonix_wolflion

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
	lf_motor 		= 0 #left front motor (0)8a
	rf_motor 		= 1 #right front motor (1)
	lr_motor 		= 2 #left rear motor (3)
	rr_motor 		= 3 #right rear motor (2) #?

	# These are mechs (pwm) 
	climer_motor 	= 4 # Motor used for climming (Sparks)
	intake_motor	= 5 # Motor for the inkate mech (Sparks)
	ha_motor		= 7 # Motor used to agitat the hopper(Victor)	

	# Mechs can
	shooter_motor	= 1 # motor used to shoot the balls (Talon SRX)
	but1channel		= 0 # Pot channel used to get auton.
	but1channel2	= 1 # Pot channel used to get auton.
	js_channel 		= 0
	
	#Relay
	rha_channel		= 1
	
	def robotInit(self):
		#cam.main()
		self.robot_drive = wpilib.RobotDrive(wpilib.Spark(self.lf_motor), wpilib.Spark(self.rf_motor), wpilib.Spark(self.lr_motor), wpilib.Spark(self.rr_motor))
		
		self.robot_drive.setExpiration(0.1)
		self.robot_drive.setInvertedMotor(RobotDrive.MotorType.kFrontLeft, True)
		self.robot_drive.setInvertedMotor(RobotDrive.MotorType.kRearLeft, True)  
		
		self.js 		= wpilib.Joystick(self.js_channel)

		# Mechs
		self.climer 	= wpilib.Spark(self.climer_motor)
		self.intake 	= wpilib.Spark(self.intake_motor)
		self.shootor 	= ctre.cantalon.CANTalon(self.shooter_motor, controlPeriodMs=10, enablePeriodMs=50)
		self.ha 		= wpilib.Victor(self.ha_motor)		
		self.switch1	= wpilib.DigitalInput(self.but1channel) 
		self.switch2	= wpilib.DigitalInput(self.but1channel2)
		
		#Relay
		#self.rha		= wpilib.Relay(self.rha_channel, direction=None)
		
		#Switch
		#self.switch1.free()
		
		self.shootor.changeControlMode(ctre.CANTalon.ControlMode.Position)
		self.shootor.setFeedbackDevice(ctre.CANTalon.FeedbackDevice.QuadEncoder)
        # This sets the basic P, I , and D values (F, Izone, and rampRate can also
        #   be set, but are ignored here).
        # These must all be positive floating point numbers (reverseSensor will
        #   multiply the sensor values by negative one in case your sensor is flipped
        #   relative to your motor).
        # These values are in units of throttle / sensor_units where throttle ranges
        #   from -1023 to +1023 and sensor units are from 0 - 1023 for analog
        #   potentiometers, encoder ticks for encoders, and position / 10ms for
        #   speeds.
		self.shootor.setPID(1.0, 0.0, 0.0)
		
	def autonomousInit(self):
		self.auto_loop_counter = 0
	def autonomousPeriodic(self):
		timer = wpilib.Timer()
		timer.start()
		auton.main(2, self.robot_drive)
		#auton.main(int(self.switch1.get()) + 1, self.robot_drive) #auton_opt 1 = start left, 2 = middle, 3 = right
		#int(self.switch1.get()) + 2 * int(self.switch2.get())
		#auton.main(5, self.robot_drive) # uncomment to enable debug
		# When debug is enabled telop will not work
		
	def teleopPeriodic(self):
		while self.isOperatorControl() and self.isEnabled():
					
			#self.robot_drive.mecanumDrive_Cartesian(self.js.getY()**2), (self.js.getX()/(math.fabs(self.js.getX())+.001)*self.js.getX()**2), -(self.js.getZ()/(math.fabs(self.js.getZ())*self.js.getZ()+.001)**2), 0) 
			self.robot_drive.mecanumDrive_Cartesian(self.js.getY(), self.js.getX(), -self.js.getZ(), 0)
			#was /1.25
		
			if self.js.getRawButton(8) == True:
				self.climer.set(1)	#  -1.0 to 1.0
				#was .76
			else:
				self.climer.set(0)

			if self.js.getRawButton(3) == True:
				self.intake.set(.9)	#  -1.0 to 1.0
			else:
				self.intake.set(0)
	
			if self.js.getRawButton(4) == True:
				self.ha.set(-1)	#  -1.0 to 1.0
				#self.rha.set(12)
			else:
				self.ha.set(0)
				#self.rha.set(0)
				
			# In closed loop mode, this sets the goal in the units mentioned above.
            # Since we are using an analog potentiometer, this will try to go to
            #   the middle of the potentiometer range.
			if self.js.getRawButton(7) == True:
				self.shootor.set(900) # 0 - 1023
				#was 800
				self.ha.set(-1)	#  -1.0 to 1.0
				#self.rha.set(12)
			else:
				self.shootor.set(0)
				self.ha.set(0)
				#self.rha.set(0)
			
		# was 0.005
		wpilib.Timer.delay(0.003)		
	def testPeriodic(self):
		wpilib.LiveWindow.run()
	
if __name__ == "__main__":
	wpilib.run(MyRobot, physics_enabled = False)
