# from time import time, sleep
# while True:
# 	sleep(6 - time() % 6)
# 	print('OK')


# itemlist = [];

# if 'big' not in itemlist:
# 	itemlist.append('big')
# 	print(itemlist)

s = 'movie.jpg'
parts = s.split('.')
if parts[-1].lower() == 'mp4':
	print(s)