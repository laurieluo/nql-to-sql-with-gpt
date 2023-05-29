import pymysql.cursors

# Connection parameters
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '9900'
DB_SMALL_NAME = 'smallRelations'
DB_BIG_NAME = 'bigRelations'

# Connect to the DB
conn_small = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    db=DB_SMALL_NAME,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
conn_big = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    db=DB_BIG_NAME,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# Query function
def executeSQL(sql, db='small'):
    # Detect the connected database type
    if db == 'big':
        cursor = conn_big.cursor()
    else:
        cursor = conn_small.cursor()

    # Execute the query and fetch the results
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()

    # Create the table header
    html_table = '<table>\n'
    html_table += '<tr>'
    for column_name in cursor.description:
        html_table += '<th>{}</th>'.format(column_name[0])
    html_table += '</tr>\n'

    # Create the table rows
    for row in rows:
        html_table += '<tr>'
        for (key, value) in row.items():
            html_table += '<td>{}</td>'.format(value)
        html_table += '</tr>\n'

    # End of the table header
    html_table += '</table>'
    
    return html_table
