import datetime

import psycopg2
from psycopg2 import Error

connection = None
cursor = None


def romanToInt(s):
    """
   :type s: str
   :rtype: int
   """
    roman = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000, 'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90,
             'CD': 400, 'CM': 900}
    i = 0
    num = 0
    while i < len(s):
        if i + 1 < len(s) and s[i:i + 2] in roman:
            num += roman[s[i:i + 2]]
            i += 2
        else:
            # print(i)
            num += roman[s[i]]
            i += 1
    return num


try:
    # Connect to an existing database
    connection = psycopg2.connect(user="postgres",
                                  password="root",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="xmldb")

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details ODHC01sr_noyear, (cibil_t)
    # Executing a SQL query
    cursor.execute(
        "SELECT * FROM information_schema.columns WHERE table_schema = 'public' AND table_name   = 'cause_list';")

    cursor.execute("INSERT INTO public.cause_list (causelist_date, court_no, cino, ctype, case_no, cause_reg_year, reg_dt, causelist_type, sr_no, purpose_priority, case_remark) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (datetime.date(2023, 5, 1), 0, 'ODHC0111222023', 1, 123, 2050, '2022-11-24', 1, 110011, 1, 'case_remark'))

    # Fetch result
    arrColumns = []
    record = cursor.fetchall()
    for r in record:
        arrColumns.append(r[3])
    print(arrColumns)

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
