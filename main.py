from depth_first_search import DFS
from breadth_first_search import BFS, BFSBidirectional
from blocksworld import BlocksWorld
from a_star_heuristics_seach import AStar
from image_generator import ImgGen
from iterative_deepening import IDDFS
from node import TreeNode
import signal
import time
import timeout_decorator


def grid_gen(puzzle_size):
    grid = ""
    goal = {}
    for i in range(puzzle_size-1):
        for j in range(puzzle_size):
            grid += "0"
        grid += "\n"
    for j in range(puzzle_size-1):
        grid += chr(ord('a') + j)
        goal[str(chr(ord('a') + j))] = (1, j+1)
    grid += "@"
    return grid, goal


def generate_blocks_world(puzzle_size):
    grid, goal = grid_gen(puzzle_size)
    height = len(grid.split('\n')[0])
    width = len(grid.split('\n'))
    obstacles = []
    world_state = {}

    y = 0
    for row in grid.split('\n'):
        for x in range(len(row)):
            if row[x].isalpha():  # if is a letter of the alphabet
                world_state[row[x]] = (x, y)

            elif row[x] == "@":
                world_state["agent"] = (x, y)

            elif row[x] == "#":
                obstacles.append((x, y))
        y += 1

    return BlocksWorld(world_state, goal, height, width, obstacles)


#@timeout_decorator.timeout(10,  use_signals=False)  # 5min
def search(obj):
    try:
        my_node = obj.search()
    except MemoryError:
        my_node = None
    my_count = obj.expansion_count
    return my_count, my_node


results = {"DFS": [], "BFS": [], "BFSBI": [], "AStar": [], "IDDFS": []}


for k in range(3, 6):
    # print("\nPuzzle size:", str(k), "x", str(k))

    world = generate_blocks_world(k)

    #img_gen = ImgGen(size*50, size*50)
    j = 0
    for i in range(0):
        start_node = TreeNode(None, dict.copy(world.initial_world_state))
        dfs = DFS(world, start_node)
        count, node = search(dfs)
        if node is not None:
            if len(results["DFS"]) <= k-3:
                print("DFS", end="\t")
                results["DFS"].append(count)
            else:
                results["DFS"][k-3] += count
            j += 1

    if j > 0:
        results["DFS"][k-3] /= j

    for i in range(0):
        print("BFS", end="\t")
        start_node = TreeNode(None, dict.copy(world.initial_world_state))
        bfs = BFS(world, start_node)
        count, node = search(bfs)
        results["BFS"].append(count)
        print(count)
        #img_gen.draw(world, node, "BFS", 0)


    for i in range(0):
        print("BFSBI", end="\t")
        head_node = TreeNode(None, dict.copy(world.initial_world_state))
        goal_world_state = dict.copy(world.goal_world_state)
        goal_world_state["agent"] = (0, 2)  # Add end position of the agent found by the AStar and IDDFS for 4x4 puzzle
        tail_node = TreeNode(None, goal_world_state)
        bfs_bi = BFSBidirectional(world, head_node, tail_node)
        count, node = search(bfs_bi)
        results["BFSBI"].append(count)
        print(count)
        #img_gen.draw(world, head_node, "BFSHeadTail", 0)

    for i in range(1):
        print("AStar", end="\t")
        start_node = TreeNode(None, dict.copy(world.initial_world_state))
        astar = AStar(world, start_node)
        count, node = search(astar)
        results["AStar"].append(count)
        print(count)
        #img_gen.draw(world, node, "AStar", 0)

    for i in range(0):
        print("IDDFS", end="\t")
        start_node = TreeNode(None, dict.copy(world.initial_world_state))
        iddfs = IDDFS(world, start_node)
        count, node = search(iddfs)
        results["IDDFS"].append(count)
        print(count)
        #img_gen.draw(world, node, "IDDFS", 0)

# TODO: obstacle and puzzle size investigation


print("\nFinished\n")

for key in results.keys():
    print(key, end="\t")
    for result in results[key]:
        print(result, end="\t")
    print("")