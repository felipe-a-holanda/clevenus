import swisseph as swe
from datetime import datetime, timedelta





vitor = datetime(1988, 8, 19, 0, 30)

def date_range(start, end):
	date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days)]
	return date_generated
	



def calc(datetime_obj, planet_index):
	return swe.calc(swe.julday(datetime_obj.year, datetime_obj.month, datetime_obj.day, datetime_obj.hour + datetime_obj.minute/60.0), planet_index)[0]


#v = 30*5+13+21/60.0
v = calc(vitor, 1)
print(v)
prev = 0
for date in date_range(datetime(2012,1,1), datetime(2017,12,31)):
	p = calc(date, 8)
	angle = abs(p-v)
	diff = 120-angle
	
	if prev*diff < 0:
		print(date.strftime('%d/%m/%Y'))	
	prev = diff
	
	#if  abs(diff)< 0.5:
	#	print(date.date(), diff)


