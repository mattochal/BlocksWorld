from random import randint
from blocksworld import BlocksWorld
from node import TreeNode


class DFS(object):

    def __init__(self, world, start_node):
        self.world = world  # BlocksWorld
        self.expansion_count = 0
        self.current = start_node  # TreeNode
        self.max_stored_nodes = 0

    def search(self):
        while not self.world.is_solved(self.current.world_state):
            # self.print_status()
            self.next()
            self.expansion_count += 1
            self.max_stored_nodes = self.expansion_count
        return self.current

    def next(self):
        new_world_state = self.world.get_random_move(self.current.world_state)
        self.current = TreeNode(self.current, new_world_state)

    # For testing purposes
    def print_status(self):
        print(self.expansion_count, "|", self.current.world_state["agent"], self.current.world_state["a"],
              self.current.world_state["b"], self.current.world_state["c"])