import initialization
import daily_report_generator
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta,date
import postgres
import sys
import query
import googledrive

def main(report_date):
  """add jobs"""
  initialization.init()
  daily_report_generator.report(report_date)

if __name__ == "__main__":
  try:
    # specify the date using datetime module
    start_date = datetime.strptime('2024-04-30', '%Y-%m-%d')
    end_date = datetime.now()

    print(start_date,end_date)
        
    date_array=[]
        
    for day in range((end_date-start_date).days):
        current_date=start_date+timedelta(days=day)
        date_array.append(datetime.strftime(current_date,'%Y-%m-%d'))
        
    for date in date_array:
      report_date = date
      if len(sys.argv) > 1:
        report_date = sys.argv[1]
        query.report_date=report_date
      print('report date:', report_date)
      main(report_date)
    
    # report_date = (datetime.now()- timedelta(days=4)).strftime('%Y-%m-%d')
    # if len(sys.argv) > 1:
    #   report_date = sys.argv[1]
    #   query.report_date=report_date
    # print('report date:', report_date)
    # main(report_date)
    
  except HttpError as err:
    print(err)
  finally:
    postgres.close_connection()
    