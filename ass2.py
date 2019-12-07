f = open("ass2_supp_sample_input.txt", "r")   # read file
num_of_servers = f.readline()
lines = f.readlines()
num_of_people = [[0, 0, 0], [0, 0, 0]]      # Number of people served for each server
flag = [[True, True, True], [True, True, True]]  # flag to see if the counter is empty
queue = [[], []]  # the waiting queue
time = [[0, 0, 0], [0, 0, 0]]  # the time each server finishes its latest customer
idle = [[0, 0, 0], [0, 0, 0]] # total idle time for each server
maxqtime = 0  # max time a customer spends in queue
avaqtime = 0  # Average time a customer spends in queue
waitnum = 0  # number of customers who need to be in queue
maxline = 0  # max length of queue

# function for adding new customer
def inQueue(element):
    global maxline
    haveposition = False     # a flag to justify if the customer is served
    server = int(element[-1])-1
    if len(queue[server]) == 0:  # if there is no people in queue (new customer's type of service)
        for index, servertime in enumerate(time[server]):
            if servertime <= int(element[0]):  # the new customer can be served
                time[server][index] = int(element[1]) + int(element[0])
                flag[server][index] = False
                num_of_people[server][index] += 1
                haveposition = True
                idle[server][index] += int(element[0]) - servertime
                break
    if haveposition is False: # the new customer is not served
        if len(queue[server-1]) == 0: # justify if he can go to another service
            for index, servertime in enumerate(time[server-1]):
                if servertime <= int(element[0]):  # has empty position
                    time[server-1][index] = int(element[1]) + int(element[0])
                    flag[server-1][index] = False
                    num_of_people[server-1][index] += 1
                    haveposition = True
                    idle[server-1][index] += int(element[0]) - servertime
                    break
    if haveposition is False: # the new customer is still not served
        queue[server].append(element)   # be in queue
        if maxline < len(queue[0]) + len(queue[1]):
            maxline = len(queue[0]) + len(queue[1])
    return

# function for update the waiting queue
def updatequeue(i):
    global maxqtime, avaqtime, waitnum
    if len(queue[0]) == 0 and len(queue[1]) == 0:  # no customer is in queue
        return
    for index, item in enumerate(time[0]):  # update the status of each counter at this time
        if i >= item:  # if the work is finished
            flag[0][index] = True
    for index, item in enumerate(time[1]):
        if i >= item:
            flag[1][index] = True
    for index, item in enumerate(flag[0]):
        if item is True:   # if there is a empty counter, select a new customer who is waiting
            if len(queue[0]) != 0:  # select as many people as possible in queue 1
                time[0][index] = i + int(queue[0][0][1])
                flag[0][index] = False
                num_of_people[0][index] += 1
                avaqtime += i - int(queue[0][0][0])
                if maxqtime < i - int(queue[0][0][0]):
                    maxqtime = i - int(queue[0][0][0])
                queue[0].pop(0)                    # First customer out of the queue
                waitnum += 1
    for index, item in enumerate(flag[1]):
        if item is True:
            if len(queue[1]) != 0:  # select as many people as possible in queue 2
                time[1][index] = i + int(queue[1][0][1])
                num_of_people[1][index] += 1
                flag[1][index] = False
                avaqtime += i - int(queue[1][0][0])
                if maxqtime < i - int(queue[1][0][0]):
                    maxqtime = i - int(queue[1][0][0])
                queue[1].pop(0)
                waitnum += 1
    if len(queue[0]) == 0 and len(queue[1]) != 0:  # justify if customer can go to service 1
        for index, item in enumerate(flag[0]):
            if item is True:
                time[0][index] = i + int(queue[1][0][1])
                num_of_people[0][index] += 1
                flag[0][index] = False
                avaqtime += i - int(queue[1][0][0])
                if maxqtime < i - int(queue[1][0][0]):
                    maxqtime = i - int(queue[1][0][0])
                queue[1].pop(0)
                waitnum += 1
    elif len(queue[1]) == 0 and len(queue[0]) != 0:  # justify if customer can go to service 2
        for index, item in enumerate(flag[1]):
            if item is True:
                time[1][index] = i + int(queue[0][0][1])
                num_of_people[1][index] += 1
                flag[1][index] = False
                avaqtime += i - int(queue[0][0][0])
                if maxqtime < i - int(queue[0][0][0]):
                    maxqtime = i - int(queue[0][0][0])
                queue[0].pop(0)
                waitnum += 1
    return

# output the result
for i in range(0, 10000):
    updatequeue(i)      # update the queue at this time
    for line in lines:
        tmp = line.rstrip().split(' ')
        if int(tmp[0]) == i:   # if there is a new customer coming at this time
            inQueue(tmp)
            break
        elif int(tmp[0]) > i:
            break

print("Number of people served for each server")
for i in num_of_people:
    for j in i:
        print(j)

print("finished time of each server")
for i in time:
    for j in i:
        print(j)

print("Average time a customer spends in queue")
print(avaqtime/waitnum)
print("max time a customer spends in queue")
print(maxqtime)
print("max line")
print(maxline)
print("total idle time for each server")
for i in idle:
    for j in i:
        print(j)

f.close()