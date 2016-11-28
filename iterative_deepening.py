from node import TreeNode


class IDDFS(object):

    def __init__(self, world, start_node):
        self.world = world  # BlocksWorld
        self.expansion_count = 0
        self.initial = start_node
        self.current = start_node  # TreeNode
        self.finished = False
        self.max_stored_nodes = 0

    def search(self):
        depth = 0
        while not self.finished:
            self.dls(self.initial, depth)
            depth += 1
            if depth > self.max_stored_nodes:
                self.max_stored_nodes = depth
        return self.current

    def dls(self, node, limit):
        self.current = node
        # self.print_status(limit)
        self.expansion_count += 1
        if limit == 0 and self.world.is_solved(node.world_state):
            self.finished = True
            return

        if limit > 0:
            for state in self.world.get_moves(node.world_state):
                new_node = TreeNode(node, state)
                self.dls(new_node, limit-1)
                if self.finished:
                    return
                del new_node
        return

    # For testing purposes
    def print_status(self, limit):
        print(self.expansion_count, "|", self.current.world_state["agent"], self.current.world_state["a"],
              self.current.world_state["b"], self.current.world_state["c"], "|", limit)
