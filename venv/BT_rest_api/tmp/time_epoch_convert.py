import time

# Require only 10 digits from the right, 1587656421184.0, need to get rid of "184.0"
timestamp="1588644097993.0"
newtime = int(timestamp[:10])

time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(newtime))
print(time)

