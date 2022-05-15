#
# @lc app=leetcode.cn id=707 lang=python3
#
# [707] 设计链表
#

# @lc code=start


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


# Your MyLinkedList object will be instantiated and called as such:
# obj = MyLinkedList()
# param_1 = obj.get(index)
# obj.addAtHead(val)
# obj.addAtTail(val)
# obj.addAtIndex(index,val)
# obj.deleteAtIndex(index)
# @lc code=end


if __name__ == "__main__":
    link_list = MyLinkedList()
    link_list.addAtHead(2)
    link_list.deleteAtIndex(1)
    link_list.addAtHead(2)
    link_list.addAtHead(7)
    link_list.addAtHead(3)
    link_list.addAtHead(2)
    link_list.addAtHead(5)
    link_list.addAtTail(5)
    link_list.get(5)
    link_list.deleteAtIndex(6)
    link_list.deleteAtIndex(4)
   
