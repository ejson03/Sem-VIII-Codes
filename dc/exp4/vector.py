from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime
from time import sleep


def local_time(counter):
    return " (VECTOR_TIME={}, LOCAL_TIME={})".format(counter, datetime.now())


def event(pid, counter):
    counter[pid] += 1
    print("Something happened in {} !".format(pid) + local_time(counter))
    return counter


def calc_recv_timestamp(recv_time_stamp, counter):
    for id in range(len(counter)):
        counter[id] = max(recv_time_stamp[id], counter[id])
    return counter


def send_message(pipe, pid, counter):
    counter[pid] += 1
    pipe.send(("Empty shell", counter))
    print("Message sent from " + str(pid) + local_time(counter))
    return counter


def recv_message(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    counter[pid] += 1
    print("Message received at " + str(pid) + local_time(counter))
    return counter


def process_one(pipe12, pipe13):
    pid = 0
    counter = [0, 0, 0]
    counter = event(pid, counter)
    counter = send_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)
    counter = event(pid, counter)


def process_two(pipe21, pipe23):
    pid = 1
    counter = [0, 0, 0]
    counter = event(pid, counter)
    counter = recv_message(pipe21, pid, counter)
    counter = recv_message(pipe23, pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = event(pid, counter)


def process_three(pipe32, pipe31):
    pid = 2
    counter = [0, 0, 0]
    counter = send_message(pipe32, pid, counter)
    counter = event(pid, counter)


if __name__ == "__main__":
    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()
    oneandthree, threeandone = Pipe()

    process1 = Process(target=process_one, args=(oneandtwo, oneandthree))
    process2 = Process(target=process_two, args=(twoandone, twoandthree))
    process3 = Process(target=process_three, args=(threeandtwo, threeandone))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()

# VECTOR OUTPUT
# Something happened in 0 ! (VECTOR_TIME=[1, 0, 0], LOCAL_TIME=2021-03-25 20:43:32.215746)
# Something happened in 1 ! (VECTOR_TIME=[0, 1, 0], LOCAL_TIME=2021-03-25 20:43:32.215778)
# Message sent from 0 (VECTOR_TIME=[2, 0, 0], LOCAL_TIME=2021-03-25 20:43:32.215812)
# Something happened in 0 ! (VECTOR_TIME=[3, 0, 0], LOCAL_TIME=2021-03-25 20:43:32.215819)
# Message received at 1 (VECTOR_TIME=[2, 2, 0], LOCAL_TIME=2021-03-25 20:43:32.215836)
# Message sent from 2 (VECTOR_TIME=[0, 0, 1], LOCAL_TIME=2021-03-25 20:43:32.216401)
# Message received at 1 (VECTOR_TIME=[2, 3, 1], LOCAL_TIME=2021-03-25 20:43:32.216416)
# Something happened in 2 ! (VECTOR_TIME=[0, 0, 2], LOCAL_TIME=2021-03-25 20:43:32.216421)
# Message sent from 1 (VECTOR_TIME=[2, 4, 1], LOCAL_TIME=2021-03-25 20:43:32.216440)
# Something happened in 1 ! (VECTOR_TIME=[2, 5, 1], LOCAL_TIME=2021-03-25 20:43:32.216445)
# Message received at 0 (VECTOR_TIME=[4, 4, 1], LOCAL_TIME=2021-03-25 20:43:32.216479)
# Something happened in 0 ! (VECTOR_TIME=[5, 4, 1], LOCAL_TIME=2021-03-25 20:43:32.216492)
