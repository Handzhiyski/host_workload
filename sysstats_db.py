#!/usr/bin/env python3

import pymysql
import psutil
import argparse
import time


parser = argparse.ArgumentParser()
parser.add_argument("--host", type=str, help="Specify host address", default='127.0.0.1')
parser.add_argument("-pw", "--password", type=str, help="Enter password")


args = parser.parse_args()

error_in_database = False


def system_specs():

    system_stats = {
        "cpu_prc": psutil.cpu_percent(),
        "free_memory_mb": round((psutil.virtual_memory()[1]) / 1024 ** 2)
    }

    try:

        database_connection = pymysql.connect(password=args.password)
        print('Connected to Database')

        cursor = database_connection.cursor()

        use_database = "use menagerie"
        cursor.execute(use_database)
        database_connection.commit()

        sql = "INSERT INTO system_stats VALUES ('{}', {}, {}, CURRENT_TIMESTAMP);".format(args.host,
                                                                                          system_stats.get("cpu_prc"),
                                                                                          system_stats.get("free_memory_mb"))

        cursor.execute(sql)
        database_connection.commit()
        print("The query affected {} rows".format(cursor.rowcount))
        print("Sent data {}, {}, {} ".format(args.host, system_stats.get("cpu_prc"), system_stats.get("free_memory_mb")))

        database_connection.close()

    except Exception as err:

        print('Error: {}'.format(str(err)))
        global error_in_database
        error_in_database = True


try:
    while True:

        if not error_in_database:
            system_specs()
            time.sleep(5)
        else:
            break

except KeyboardInterrupt as e:
    print("Interrupted")


