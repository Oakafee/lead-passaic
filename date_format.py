import datetime

def date_format(dr):
	start = []
	end = []

	dr = dr.split("--")
	dr[0] = dr[0].split("/")
	dr[1] = dr[1].split("/")

	for i in dr[0]:
		start.append(int(i))

	for i in dr[1]:
		end.append(int(i))

	start = datetime.datetime(start[2], start[0], start[1])
	end = datetime.datetime(end[2], end[0], end[1])
		
	return(start, end)