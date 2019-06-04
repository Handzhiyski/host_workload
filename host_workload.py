#!/usr/bin/env python3

import pymysql
import argparse

average_cpu_workload = 0
average_ram_workload = 0
host_entries = 0
hour = 0
are_entries = False

parser = argparse.ArgumentParser()

parser.add_argument("host", type=str, help="Specify host address")
parser.add_argument("date", type=str, help="Enter date in format YYYY-MM-DD")

args = parser.parse_args()

try:

    connection = pymysql.connect(password='67181df7')

    cursor = connection.cursor()
    cursor.execute("use menagerie")

    while True:

        try:

            cursor.execute("SELECT * FROM system_stats WHERE (host = '{}' AND DATE(stats_on_date)"
                           " = '{}' AND HOUR(stats_on_date) = {});"
                           .format(args.host, args.date, hour))

            rows = cursor.fetchall()

            for row in rows:

                average_cpu_workload += row[1]
                average_ram_workload += row[2]
                host_entries += 1
                date = row[3]

            print("Host : {} had average CPU workload : {} and average available RAM : {} on : {}:00:00 to {}:59:59".
                                                                            format(args.host,
                                                                                   average_cpu_workload/host_entries,
                                                                                   average_ram_workload/host_entries,
                                                                                   str(date)[0:13],
                                                                                   str(date)[11:13]))
            are_entries = True
            average_cpu_workload = 0
            average_ram_workload = 0
            host_entries = 0
            hour += 1

            if hour == 24:
                break

        except ZeroDivisionError as e:

            hour += 1

            if hour == 24:
                if not are_entries:
                    print("No entries found")
                break

except Exception as e:
    print("Error {}".format(e))

