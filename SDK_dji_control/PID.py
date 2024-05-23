class PID:
	sum_error = 0
	last_error = 0

	def __init__(self, Kp, Ki, Kd):
		self.Kp = Kp
		self.Ki = Ki
		self.Kd = Kd

	def control(self, error):
		d_error = 2 * error - self.last_error
		self.sum_error += error
		result = self.Kp * error + self.Ki * self.sum_error + self.Kd * d_error
		self.last_error = error
		return result
