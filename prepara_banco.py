import MySQLdb
print('Conectando...')
conn = MySQLdb.connect(user='root', passwd='admin',database='estoque_2',host='127.0.0.1', port=3306, charset='utf8')

