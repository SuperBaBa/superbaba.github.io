---
title: 双向链表
date: 2020-08-08 21:34:36
categories: 算法
---
### 解题思路
没有哨兵节点的双向链表

### 代码
```python3

class Node(object):
    def __init__(self, val: int) -> None:
        self.val = val
        self.perv = None
        self.next = None

    def __str__(self) -> str:
        return str(self.val)


# @lc code=start
class MyLinkedList:
    def __init__(self):
        self.first = None
        self.last = None
        self.size = 0

    def get(self, index: int) -> int:
        """
        需要判断从头部遍历还是从尾部遍历
        """
        if index < 0 or index >= self.size:
            return -1

        if index < self.size/2:
            curr = self.first
            for _ in range(index):
                curr = curr.next
        else:
            curr = self.last
            for _ in range(index, self.size-1):
                curr = curr.perv
        return curr.val
        
    def addAtHead(self, val: int) -> None:
        new_node = Node(val)
        if self.first:
            new_node.next = self.first
            self.first.perv = new_node
            self.first = new_node
        else:
            self.first = new_node
            self.last = new_node
        self.size += 1
        return

    def addAtTail(self, val: int) -> None:
        """
        没有哨兵节点，因此需要对self.last进行特殊处理
        """
        new_node = Node(val)
        if self.last:
            self.last.next = new_node
            new_node.perv = self.last
            self.last = new_node
        else:
            self.last = new_node
            self.first = new_node
        self.size += 1
        return

    def addAtIndex(self, index: int, val: int) -> None:
        if index < 0 or index > self.size:
            return None

        #如果index是self的容量，则在最后追加上
        if index == self.size:
            self.addAtTail(val)
        else:
            new_node = Node(val)
            #先找到指定节点
            if index < self.size/2:
                succ_node = self.first
                for _ in range(index):
                    succ_node = succ_node.next
            else:
                succ_node = self.last
                for _ in range(index, self.size-1):
                    succ_node = succ_node.perv
            succ_perv = succ_node.perv
            new_node.perv = succ_perv
            new_node.next = succ_node
            succ_node.perv = new_node
            if succ_perv:
                succ_perv.next = new_node
            else:
                self.first = new_node
            self.size += 1
        return

    def deleteAtIndex(self, index: int) -> None:
        if index < 0 or index >= self.size:
            return None
        
        #找到指定节点
        if index < self.size/2:
            succ_node = self.first
            for _ in range(index):
                succ_node = succ_node.next
        else:
            succ_node = self.last
            for _ in range(index, self.size-1):
                succ_node = succ_node.perv

        succ_perv = succ_node.perv
        succ_next = succ_node.next
        #被选中节点的前继节点处理
        if succ_perv:
            succ_perv.next = succ_next
            succ_node.perv = None
        else:
            self.first = succ_next
        
        #被选中节点的后继节点处理
        if succ_next:
            succ_next.perv = succ_perv
            succ_node.next = None
        else:
            self.last = succ_perv

        self.size -= 1
        return        

    def __str__(self) -> str:
        curr = self.first
        print_list = [str(curr)]
        while curr:
            curr = curr.next
            if curr:
                print_list.append(str(curr))
        return str(print_list)

```
没有哨兵节点的双向链表
```python3

class Node(object):

    def __init__(self, val=None) -> None:
        self.val = val
        self.prev = None
        self.next = None


class MyLinkedList:

    def __init__(self):
        self.first = Node()
        self.last = Node()
        self.first.next = self.last  #前驱结点的后继
        self.last.prev = self.first  #后继节点的前驱
        self.size = 0

    def get(self, index: int) -> int:
        """
        判断 index 和 size-index 的大小，决定是从头开始比较快还是从尾开始比较快
        """
        # if index is invalid
        if index < 0 or index >= self.size:
            return -1

        if index + 1 < self.size - index :
            curr = self.first
            for _ in range(index + 1):
                curr = curr.next
        else:
            curr = self.last
            for _ in range(self.size - index):
                curr = curr.prev
        return  curr.val

    def addAtHead(self, val: int) -> None:
        """
        在链表头部元素之前插入一个
        """
        new_node = Node(val)
        pred, succ = self.first, self.first.next
        pred.next = new_node
        new_node.prev = pred
        succ.prev = new_node
        new_node.next = succ
        self.size += 1

    def addAtTail(self, val: int) -> None:
        """
        在尾部插入一个，只需要找到后继节点
        """
        new_node = Node(val)
        pred, succ = self.last.prev, self.last
        new_node.next = succ
        new_node.prev = pred
        pred.next = new_node
        succ.prev = new_node
        self.size += 1

    def addAtIndex(self, index: int, val: int) -> None:
        """
        需要循环查找，查找之前可以进行判断index是前驱遍历还是后继遍历，提升其速度
        """
        if index > self.size:
            return
        if index < 0:
            index = 0
        if index < self.size - index:
            pred = self.first
            for _ in range(index):
                pred = pred.next
            succ = pred.next
        else:
            succ = self.last
            for _ in range(self.size - index):
                succ = succ.prev
            pred = succ.prev
        new_node = Node(val)

        #增加节点
        self.size += 1
        new_node.prev = pred
        new_node.next = succ
        pred.next = new_node
        succ.prev = new_node

       
    def deleteAtIndex(self, index: int) -> None:
        """
        使用index判断
        """
        if index < 0 or (self.size <= index):
            return
        if index < self.size - index:
            pred = self.first
            for i in range(index):
                pred = pred.next
            succ = pred.next.next
        else:
            succ = self.last
            for i in range(self.size - index -1):
                succ = succ.prev
            pred = succ.prev.prev
        self.size-=1
        
        pred.next = succ
        succ.prev = pred

```