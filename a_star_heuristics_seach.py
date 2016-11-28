from queue import PriorityQueue
from node import TreeNode
# from image_generator import ImgGen  # DEBUG


class AStar(object):
    def __init__(self, world, start_node):
        self.world = world  # BlocksWorld
        self.expansion_count = 0
        self.current = start_node  # TreeNode
        self.q = PriorityQueue()
        self.node_count = 0
        self.q.put((world.distance_from_goal(start_node.world_state), self.node_count, start_node))
        self.max_stored_nodes = 1

    def search(self):
        while self.next():
            self.expansion_count += 1
            if self.q.qsize() > self.max_stored_nodes:
                self.max_stored_nodes = self.q.qsize()
        return self.current

    def depth(self, node):
        count = 0
        while node.parent is not None:
            count += 1
            node = node.parent
        return count

    def next(self):
        value, node_count, self.current = self.q.get()
        #self.print_status(value, node_count)

        depth = self.depth(self.current)

        if self.world.is_solved(self.current.world_state):
            return False

        for state in self.world.get_moves(self.current.world_state):
            node = TreeNode(self.current, state)
            self.node_count += 1
            self.q.put((self.world.distance_from_goal(node.world_state) + depth + 1, self.node_count, node))

        return True

    def print_status(self, value, node_count):
        print(self.expansion_count, "&", self.current.world_state["agent"], "&", self.current.world_state["a"], "&",
              self.current.world_state["b"],  "&", self.current.world_state["c"], "&", value, "&", node_count, "&", self.q.qsize(), r"\\")