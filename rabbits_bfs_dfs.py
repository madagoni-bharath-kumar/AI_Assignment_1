class State:
    def __init__(self, config):
        self.config = tuple(config)

    def goalTest(self):
        return self.config == ('W', 'W', 'W', '_', 'E', 'E', 'E')

    def moveGen(self):
        children = []
        config = list(self.config)
        blank_index = config.index('_')

        def swap_and_create(i):
            new_config = config.copy()
            new_config[blank_index], new_config[i] = new_config[i], '_'
            return State(new_config)

        # Move or jump to the left
        if blank_index - 1 >= 0 and config[blank_index - 1] in ('E', 'W'):
            children.append(swap_and_create(blank_index - 1))
        if blank_index - 2 >= 0 and config[blank_index - 2] in ('E', 'W') and config[blank_index - 1] != '_':
            children.append(swap_and_create(blank_index - 2))

        # Move or jump to the right
        if blank_index + 1 < 7 and config[blank_index + 1] in ('E', 'W'):
            children.append(swap_and_create(blank_index + 1))
        if blank_index + 2 < 7 and config[blank_index + 2] in ('E', 'W') and config[blank_index + 1] != '_':
            children.append(swap_and_create(blank_index + 2))

        return children

    def __str__(self):
        return ''.join(self.config)

    def __eq__(self, other):
        return isinstance(other, State) and self.config == other.config

    def __hash__(self):
        return hash(self.config)


def removeSeen(children, OPEN, CLOSED):
    open_nodes = [node for node, _ in OPEN]
    closed_nodes = [node for node, _ in CLOSED]
    return [c for c in children if c not in open_nodes and c not in closed_nodes]


def reconstructPath(node_pair, CLOSED):
    path = []
    parent_map = {node: parent for node, parent in CLOSED}
    node, parent = node_pair
    path.append(node)
    while parent is not None:
        path.append(parent)
        parent = parent_map[parent]
    return path


def bfs(start):
    OPEN = [(start, None)]
    CLOSED = []

    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair

        if N.goalTest():
            print("Goal found (BFS):")
            path = reconstructPath(node_pair, CLOSED)
            path.reverse()
            for p in path:
                print("->", p)
            return

        CLOSED.append(node_pair)
        children = N.moveGen()
        new_nodes = removeSeen(children, OPEN, CLOSED)
        new_pairs = [(c, N) for c in new_nodes]
        OPEN = OPEN + new_pairs


def dfs(start):
    OPEN = [(start, None)]
    CLOSED = []
    steps = 0
    max_steps = 1000

    while OPEN:
        if steps > max_steps:
            print("Too many steps. Likely infinite loop.")
            return

        node_pair = OPEN.pop(0)
        N, parent = node_pair

        if N.goalTest():
            print("Goal found (DFS):")
            path = reconstructPath(node_pair, CLOSED)
            path.reverse()
            for p in path:
                print("->", p)
            return

        CLOSED.append(node_pair)
        children = N.moveGen()
        new_nodes = removeSeen(children, OPEN, CLOSED)
        new_pairs = [(c, N) for c in new_nodes]
        OPEN = new_pairs + OPEN
        steps += 1


start_state = State(['E', 'E', 'E', '_', 'W', 'W', 'W'])

print("------ BFS ------")
bfs(start_state)

print("\n------ DFS ------")
dfs(start_state)
