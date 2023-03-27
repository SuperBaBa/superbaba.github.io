
class Node:
    def __init__(self, next=None, key=None, value=None, hash=None) -> None:
        """
        
        """
        self.__next = next
        self.__key = key
        self.__value = value
        self.__hash = hash

    def __str__(self) -> str:
        return '{key} = {value}'.format(key=self.__key, value=self.__value)

    __repr__ = __str__
    """
    将输出方法赋值给reper方法
    相对来说 __reper__ 方法比 __str__ 方法更便于调试
    1. __repr__正式, __str__ 非正式。
    2. __str__主要由 str(),format()和print()三个方法调用。
    3. 若定义了__repr__没有定义__str__, 那么本该由__str__展示的字符串会由__repr__代替。
    4. __repr__主要用于调试和开发, 而__str__用于为最终用户创建输出。
    5. __repr__看起来更像一个有效的 Python 表达式，可用于重新创建具有相同值的对象（给定适当的环境）
    可以使用 pprint(ts) 方法查看调用
    """

    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, next):
        self.__next = next

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, key):
        self.__key = key

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    @property
    def hash(self):
        return self.__hash

    @hash.setter
    def hash(self, hash):
        self.__hash = hash


class MyNode:
    def __init__(self, key, val, prev=None, succ=None):
        self.key = key
        self.val = val
        # 前驱
        self.prev = prev
        # 后继
        self.succ = succ

    def __repr__(self):
        return str(self.val)


class HashMap:
    def __init__(self, capacity=16, load_factor=0.75) -> None:
        self.__capacity = capacity  # 初始化容量
        self.__load_factor = load_factor  # 负载因子
        self.__tab = [Node() for _ in range(capacity)]

    def __str__(self):
        return 'Student object (tab=%s)' % self.__tab

    '''
    这里采用位运算是因为容量是2的n次方
    '''

    def get_hash_key(self, key):
        return hash(key) & (self.__capacity - 1)

    '''
    填充
    '''

    def put(self, key, val):
        if self.__tab.__len__ == 0:
            self.resize()
        hash_key = self.get_hash_key(key)
        if self.__tab[hash_key].key is None:
            self.__tab[hash_key] = Node(None, key, val, hash(key))

    '''
    初始化或者扩容表容量
    Initializes or doubles table size. If null, allocates in accord with initial capacity target held in field threshold. Otherwise,
    because we are using power-of-two expansion, the elements from each bin must either stay at same index, or move with a power of two offset in the new table.
    '''

    def resize(self):
        tab = [Node() for i in range(self.__capacity * 2)]
        cap = self.__capacity
        self.__capacity = self.__capacity * 2
        for i in range(cap):
            linked_list = self.__tab[i]
            nodes = linked_list.get_list()
            for u in nodes:
                hash_key = self.get_hash_key(u.key)
                head = tab[hash_key]
                head.append(u)
        self.__tab = tab


hash_map = HashMap()
hash_map.put('这是一个key', '这是一个value值')
print(hash_map)
