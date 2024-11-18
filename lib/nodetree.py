from PySide6.QtGui import QStandardItem


class Node(QStandardItem):
    def __init__(self, parent, child, data, _next):
        super().__init__()
        self.parentNode = parent
        self.childNode = child
        self.nextNode = _next
        self.data = data


class ContainerNode(Node):
    def __init__(self, parent, child, data, _next, num_children):
        super().__init__(parent, child, data, _next)
        self.numChildren = num_children


class ItemNode(Node):
    def __init__(self, parent, child, data, _next, index):
        super().__init__(parent, child, data, _next)
        self.index = index
