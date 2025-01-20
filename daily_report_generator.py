import googledrive
import constants
from datetime import datetime
import os
import query
import postgres

def createReport(report_date, filename,Query,conn):
    cur = conn.cursor()
    query = Query

    outputquery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(query)

    with open(f"{filename}", 'w') as f:
        cur.copy_expert(outputquery, f)
    print('report generated successfully.')
    return filename



def generate(report_date,report_name,source,Query):
    print(f'{report_name}-genarating...')
    date = datetime.strptime(report_date, "%Y-%m-%d")
    folder_name=googledrive.get_folder_id_else_create(f'''{source}/{date.year}/{date.month}/{date.day}''')
    filename = f'{source}-{report_name}-{report_date}.csv'
    filename = createReport(report_date, filename,Query,conn = constants.DATABASE_CONNECTIONS[source])
    os.chmod(f"{filename}", 0o777)
    googledrive.uploadCSV(folder_name, filename)
    if os.path.exists(f"{filename}"):
        print("file removed from local")
        os.remove(f"{filename}")
    else:
        print("The file does not exist")
        
def report(report_date):
    queries=query.get_queries(report_date)
    for report in queries.keys():
        postgres.init()
        generate(report_date,report,'db',queries[report])