class Stack:
    def __init__(self, items=[]):
        self.items = items

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if len(self.items) > 0:
            return self.items[len(self.items)-1]
        else:
            return None

    def size(self):
        return len(self.items)
