import queue
from node import TreeNode


class BFS(object):

    def __init__(self, world, start_node):
        self.world = world  # BlocksWorld
        self.expansion_count = 0
        self.current = start_node  # TreeNode
        self.q = queue.Queue()
        self.q.put(start_node)
        self.max_stored_nodes = 1

    def search(self):
        while self.next():
            self.expansion_count += 1
            # print(self.expansion_count)
            if self.q.qsize() > self.max_stored_nodes:
                self.max_stored_nodes = self.q.qsize()
        return self.current

    def next(self):
        self.current = self.q.get()
        # self.print_status()
        if self.world.is_solved(self.current.world_state):
            return False
        new_world_states = self.world.get_moves(self.current.world_state)
        for state in new_world_states:
            node = TreeNode(self.current, state)
            self.q.put(node)
        return True

    # For testing purposes
    def print_status(self):
        print(self.expansion_count, "|", self.current.world_state["agent"], self.current.world_state["a"],
              self.current.world_state["b"], self.current.world_state["c"], "|", self.q.qsize())


class BFSBidirectional(object):

    def __init__(self, world, head_node, tail_node):
        self.world = world  # BlocksWorld
        self.expansion_count = 0
        self.head_node = head_node  # TreeNode
        self.tail_node = tail_node  # TreeNode
        self.tail_q = queue.Queue()
        self.tail_q.put(tail_node)
        self.explored_by_tail = {}
        self.head_q = queue.Queue()
        self.head_q.put(head_node)
        self.explored_by_head = {}
        self.max_stored_nodes = 2

    def search(self):
        while self.next():
            if self.head_q.qsize()+self.tail_q.qsize() > self.max_stored_nodes:
                self.max_stored_nodes = self.head_q.qsize()+self.tail_q.qsize()

        # Reverse the tail and append it to head_node
        self.head_node = self.head_node.parent  # get rid of the duplicate
        while True:
            if self.tail_node.parent is None:
                if self.tail_node != self.head_node:
                    self.tail_node.parent = self.head_node
                    self.head_node = self.tail_node
                break
            node = self.tail_node.parent
            self.tail_node.parent = self.head_node
            self.head_node = self.tail_node
            self.tail_node = node

        return self.head_node

    def next(self):
        self.head_node = self.head_q.get()
        str_world_state = str(self.head_node.world_state)
        if str_world_state not in self.explored_by_head:
            self.explored_by_head[str_world_state] = self.head_node
        self.expansion_count += 1
        if str_world_state in self.explored_by_tail:
            self.tail_node = self.explored_by_tail[str_world_state]
            return False

        self.tail_node = self.tail_q.get()
        str_world_state = str(self.tail_node.world_state)
        if str_world_state not in self.explored_by_tail:
            self.explored_by_tail[str_world_state] = self.tail_node
        self.expansion_count += 1
        if str_world_state in self.explored_by_head:
            self.head_node = self.explored_by_head[str_world_state]
            return False

        new_world_states = self.world.get_moves(self.head_node.world_state)
        for state in new_world_states:
            node = TreeNode(self.head_node, state)
            self.head_q.put(node)

        new_world_states = self.world.get_moves(self.tail_node.world_state)
        for state in new_world_states:
            node = TreeNode(self.tail_node, state)
            self.tail_q.put(node)

        return True
