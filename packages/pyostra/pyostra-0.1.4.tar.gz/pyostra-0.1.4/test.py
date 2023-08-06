from pyostra import extime
import time

timer = time.perf_counter_ns()

a = 0
for i in range(10000):
    a += 1

extime('Loop execution time', timer)
