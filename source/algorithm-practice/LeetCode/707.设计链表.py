#
# @lc app=leetcode.cn id=707 lang=python3
#
# [707] 设计链表
#

# @lc code=start


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

        if index < self.size / 2:
            curr = self.first
            for _ in range(index):
                curr = curr.next
        else:
            curr = self.last
            for _ in range(index, self.size - 1):
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
            if index < self.size / 2:
                succ_node = self.first
                for _ in range(index):
                    succ_node = succ_node.next
            else:
                succ_node = self.last
                for _ in range(index, self.size - 1):
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
        if index < self.size / 2:
            succ_node = self.first
            for _ in range(index):
                succ_node = succ_node.next
        else:
            succ_node = self.last
            for _ in range(index, self.size - 1):
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


# @lc code=end

if __name__ == '__main__':
    link_list = MyLinkedList()
    link_list.addAtHead(1)
    link_list.addAtTail(3)
    print(link_list)
    link_list.addAtIndex(1, 2)
    print(link_list)
    print(link_list.get(1))
    link_list.deleteAtIndex(1)
    print(link_list)
    print(link_list.get(1))

    link_lis2 = MyLinkedList()
    link_lis2.addAtHead(1)
    link_lis2.deleteAtIndex(0)
    print(link_lis2)

    link_list3 = MyLinkedList()
    link_list3.addAtHead(7)
    link_list3.addAtHead(2)
    link_list3.addAtHead(1)
    link_list3.addAtIndex(3, 0)
    link_list3.deleteAtIndex(2)
    link_list3.addAtHead(6)
    link_list3.addAtTail(4)
    link_list3.get(4)
    link_list3.addAtHead(4)
    link_list3.addAtIndex(5, 0)
    link_list3.addAtHead(6)

    link_list4 = MyLinkedList()
    link_list4.addAtHead(2)
    link_list4.deleteAtIndex(1)
    link_list4.addAtHead(2)
    link_list4.addAtHead(7)
    link_list4.addAtHead(3)
    link_list4.addAtHead(2)
    link_list4.addAtHead(5)
    link_list4.addAtTail(5)
    link_list4.get(5)
    link_list4.deleteAtIndex(6)
    link_list4.deleteAtIndex(4)
    print(link_list4)
