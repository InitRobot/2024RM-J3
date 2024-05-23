class PID:
	last_error = 0
	sum_error = 0

	def __init__(self, Kp, Ki, Kd):
		self.Kp = Kp
		self.Ki = Ki
		self.Kd = Kd

	def pid_control(self, error):
		self.sum_error += error
		output = self.Kp * error + self.Ki * self.sum_error + self.Kd * (2 * self.last_error - error)
		self.last_error = error
		return output
