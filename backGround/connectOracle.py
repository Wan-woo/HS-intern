#import pymysql
import cx_Oracle
#v_var=xxx()
# 打开数据库连接
#db = pymysql.connect("192.168.36.244", "root", "mysql", "hsyq")
#db = pymysql.connect("192.168.36.244", "root", "mysql", "hsyq")

#db = cx_Oracle.connect('faisdb','faisdb','192.168.36.244:1521/fais')
db = cx_Oracle.connect('zwd','123456','127.0.0.1/orcl.hs.handsome.com.cn')
#db = cx_Oracle.connect('zwd/123456@orcl')
#db = connection=cx_Oracle.connect("zwd","123456","127.0.0.1/orcl")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
#cursor.execute("select id,innercode from dw_secumain where rownum<100  ")
#cursor.execute("select sno,sname from Student ")
#cursor.execute("select tname,tsex,cname from teacher left join course on course.tno=teacher.tno where tsex='男'")
cursor.execute("select table_name from user_tables")
# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchall()
print(type(data))
print((data))
print((data[0]))
data2=data[0]
print(data2[0])
for row in data:
    v_id= row[0]
    v_innercode = row[1]
    # 打印结果
    print("v_id=%s,v_innercode=%s" % \
          (v_id, v_innercode))

# 关闭数据库连接
db.close()

