# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import asyncio
from datetime import datetime
import socket
import time

tries = 1
number_of_sites = 1000
async def connect_v4(site_v4):
    try:
        start_t = time.time_ns()
        r, w = await asyncio.open_connection(site_v4[1][0], 80)
        site_v4[2] = time.time_ns() - start_t
    except:
        print("Couldn't connect to" + site[1][0])


async def connect_v6(site_v6):
    try:
        start = time.time_ns()
        r, w = await asyncio.open_connection(site_v6[3][0], 80)
        site_v6[4] = time.time_ns() - start
    except:
        print("Couldn't connect to " + site[3][0])


async def resolve_one(site, loop):
    try:
        domains = await loop.getaddrinfo(site[0], 80)
        for d in domains:
            if d[0] == socket.AddressFamily.AF_INET:
                site[1].append(d[4][0])
            else:
                site[3].append(d[4][0])
    except socket.gaierror as err:
        print(err)


async def resolve(sites, loop):
    i = 0
    tasks = []
    for site in sites:
        site.append([])
        site.append([])
        site.append([])
        site.append([])
        i += 1
        tasks.append(loop.create_task(resolve_one(site, loop)))
    await asyncio.gather(*tasks)

async def connect(sites, loop):
    tasks = []
    for site in sites:
        site[2] = 0
        site[4] = 0
        if len(site[1]) > 0:
            tasks.append(loop.create_task(connect_v4(site)))
        if len(site[3]) > 0:
            tasks.append(loop.create_task(connect_v6(site)))
    await asyncio.gather(*tasks)
    print(sites)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sites = []
    ranking = open("alexa.csv", "r")

    for i in range(number_of_sites):
        site = ranking.readline()
        sites.append([site.split(",")[1].split("\n")[0]])

    print(sites)

    start = time.time_ns()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(resolve(sites, loop))
    loop.run_until_complete(connect(sites, loop))
    loop.close()
    print("Execution done, time taken: " + str((time.time_ns() - start) // 1_000_000))

    results = open("results.csv", "w")
    for site in sites:
        line = site[0] + ";" + str(site[1]) + ";" + str(len(site[1])) + ";" + str(site[2]) + ";" + str(
            site[3]) + ";" + str(len(site[3])) + ";" + str(site[4]) + "\n"
        results.write(line)


