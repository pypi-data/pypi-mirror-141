import leveldb
from loguru import logger

try:
    db=leveldb.LevelDB('/Users/chenzongwei/pythoncode/LevelDB')
    logger.success('数据连接成功🎈')
except Exception as e:
    logger.error('⚠️数据连接失败，请检查后重试，错误原因如下')
    logger.error(e)

def get(x):
    return db.Get(bytes(x,'utf-8')).decode()

def put(x,y):
    db.Put(bytes(x,'utf-8'),bytes(y,'utf-8'))

def delete(x):
    db.Delete(bytes(x,'utf-8'))

def display(x):
    di=dict(db.RangeIter())
    return di






