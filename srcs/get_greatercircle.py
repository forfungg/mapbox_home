import math

# https://www.movable-type.co.uk/scripts/latlong.html
# To prevent longitude snapping I should find exact location on 180 degrees and transform the linestring to multi linesting.
# https://gis.stackexchange.com/questions/144007/project-location-on-a-great-circle-path

def split_line(p1, p2):
	error_margin = 0.00000000001
	tmp = get_greatercircle(p1, p2, 2)
	while 180 * (1 - error_margin) > abs(tmp[1][0]):
		if (tmp[1][0] >= 0 and p1[0] >= 0) or (tmp[1][0] <= 0 and p1[0] <= 0):
			tmp = get_greatercircle(tmp[1], tmp[2], 2)
		else:
			tmp = get_greatercircle(tmp[0], tmp[1], 2)
		if not tmp:
			print("Error spliting LineString")
			return None
	return tmp[1]

def check_values(greater_circle):
	l = len(greater_circle)
	i = 0
	while i < l - 1:
		p1 = greater_circle[i]
		p2 = greater_circle[i + 1]
		if (math.radians(p1[0]) > math.pi/2 and math.radians(p2[0]) < -1 * math.pi/2) or (math.radians(p2[0]) > math.pi/2 and math.radians(p1[0]) < -1 * math.pi/2):
			sp = split_line(p1, p2)
			left = greater_circle[:(i + 1)]
			right = greater_circle[(i + 1):]
			if (sp[0] >= 0 and p1[0] >= 0) or (sp[0] <= 0 and p1[0] <= 0):
				left.append(sp)
				r_sp = split_line(sp, p2)
				right.insert(0, r_sp)
			else:
				right.insert(0, sp)
				l_sp = split_line(p1, sp)
				left.append(l_sp)
			return True, [left, right]
		i += 1
	return False, greater_circle

def get_greatercircle(point1, point2, steps):
	rp1 = list()
	rp2 = list()
	#normalization for longitudes
	#(lon+540)%360-180
	rp1.append(math.radians((point1[0] + 540) % 360 - 180))
	rp2.append(math.radians((point2[0] + 540) % 360 - 180))
	rp1.append(math.radians(point1[1]))
	rp2.append(math.radians(point2[1]))
	fract = 1.0 / steps

	distr = 2 * math.asin(math.sqrt((math.sin((rp1[1] - rp2[1]) / 2)) ** 2) + math.cos(rp1[1]) * math.cos(rp2[1]) * (math.sin((rp1[0] - rp1[0]) / 2)) ** 2)
	if math.sin(distr) == 0:
		return None
	
	f = fract
	greater_circle = list()
	while f < 1:
		A = math.sin((1 - f) * distr) / math.sin(distr)
		B = math.sin(f * distr) / math.sin(distr)
		x = A * math.cos(rp1[1]) * math.cos(rp1[0]) + B * math.cos(rp2[1]) * math.cos(rp2[0])
		y = A * math.cos(rp1[1]) * math.sin(rp1[0]) + B * math.cos(rp2[1]) * math.sin(rp2[0])
		z = A * math.sin(rp1[1]) + B * math.sin(rp2[1])
		n_lat = math.atan2(z, math.sqrt(x ** 2 + y ** 2))
		n_lon = math.atan2(y, x)
		new = [math.degrees(n_lon), math.degrees(n_lat)]
		greater_circle.append(new)
		f += fract
	
	greater_circle.insert(0, point1)
	greater_circle.append(point2)
	return greater_circle

def greatcircle(point1, point2, steps=100):
	result = get_greatercircle(point1, point2, steps)
	multi, result = check_values(result)
	return multi, result

if __name__ == "__main__":
	#point 1
	p1 = [178.64209184022712, 2.598731224318669] 

	#point 2
	p2 = [-178.55927895810618, -8.60694107338936]

	b, ret = check_values([p1, p2])

	print(b)
	print(ret)
	