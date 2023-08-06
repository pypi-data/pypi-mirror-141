import sys
import os


"""
	自动引入上级的Common组件
"""


path=''
flag=False
# 循环向上级目录查找Common
for i in range(10):
	tempStr='/'.join(['..' for i in range(i)])
	path=os.path.abspath(os.path.join(os.getcwd(),tempStr))
	if os.path.exists(path+'/Common') and os.path.exists(path+'/Common/__common__.py'):
		flag=True
		break


# 正常找到Common
if flag:
	sys.path.append(path+r'\Common')

else:
	raise Exception("Can't find Common!")
