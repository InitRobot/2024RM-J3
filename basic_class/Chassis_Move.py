speed = 30


def move(TCP, wheel, printing=True):
	wheel = [i * 1000 / 100 * speed for i in wheel]
	chassis = "chassis wheel w2 " + str(wheel[0]) + " w1 " + str(wheel[1]) + " w3 " + str(wheel[2]) + " w4 " + str(
		wheel[3]) + ";"
	TCP.IN_OUT(chassis, printing=printing)
