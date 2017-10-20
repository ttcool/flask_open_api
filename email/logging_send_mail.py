#coding=utf-8  
''''' 
Created on 2016-3-21 
 
@author: Administrator 
'''  
import logging, logging.handlers  
class EncodingFormatter(logging.Formatter):  
    def __init__(self, fmt, datefmt=None, encoding=None):  
        logging.Formatter.__init__(self, fmt, datefmt)  
        self.encoding = encoding  
    def format(self, record):  
        result = logging.Formatter.format(self, record)  
        if isinstance(result, unicode):  
            result = result.encode(self.encoding or 'utf-8')  
              
        return result  
  
#zhangdongsheng@itouzi.com  
errlog = logging.getLogger()  
sh = logging.handlers.SMTPHandler("smtp.163.com", 'xigongda200608@163.com', '381084992@qq.com',  
                "logging from my app",  
                credentials=('xigongda200608', 'password'),  
                secure=())  
errlog.addHandler(sh)  
sh.setFormatter(EncodingFormatter('%(message)s', encoding='utf-8'))  
errlog.error(u'追加文件时出错') 
