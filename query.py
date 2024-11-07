# when ever this dictionary is call this function with date argument

def get_queries(report_date):
    queries={}
#   provide your quiries here
    queries['query1']=f'''
            select *
                from table_name
                where date='{report_date}' 
                order by report_date,users.id
            '''
    queries['query2']=f'''
            --query2
            '''
    queries['query3']=f'''
            --query3
            '''
    
    return queries