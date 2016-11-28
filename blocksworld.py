from random import randint


class BlocksWorld(object):

    def __init__(self, world_state, goal_world_state, height, width, obstacles):
        self.initial_world_state = world_state
        self.goal_world_state = goal_world_state
        self.h = height
        self.w = width
        self.obstacles = obstacles

    def is_solved(self, world_state):
        for key in self.goal_world_state:
            if self.goal_world_state[key] != world_state[key]:
                return False
        return True

    def get_moves(self, world_state):
        agent = world_state["agent"]
        moves = []
        for i, j in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            pos = (agent[0] + i, agent[1] + j)
            if self.is_valid_pos(pos):
                new_world_state = dict.copy(world_state)
                for key in world_state:
                    if world_state[key] == pos:
                        new_world_state[key] = agent
                        break
                new_world_state["agent"] = pos
                moves.append(new_world_state)
        return moves

    def get_random_move(self, world_state):
        agent = world_state["agent"]
        while True:
            i, j = [(1, 0), (0, 1), (-1, 0), (0, -1)][randint(0, 3)]
            pos = (agent[0] + i, agent[1] + j)
            if self.is_valid_pos(pos):
                break
        new_world_state = dict.copy(world_state)
        for key in world_state:
            if world_state[key] == pos:
                new_world_state[key] = agent
                break
        new_world_state["agent"] = pos
        return new_world_state

    def is_valid_pos(self, pos):
        return (0 <= pos[0] < self.w) & (0 <= pos[1] < self.h) & (pos not in self.obstacles)

    def distance_from_goal(self, world_state):
        dist = 0
        for key in self.goal_world_state:
            pos = world_state[key]
            goal_pos = self.goal_world_state[key]
            dist += abs(pos[0] - goal_pos[0]) + abs(pos[1] - goal_pos[1])
        return dist
