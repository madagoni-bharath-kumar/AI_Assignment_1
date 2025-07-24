class State:
    def __init__(self, amogh, ameya, grandma, grandpa, umbrella, time):
        self.amogh = amogh
        self.ameya = ameya
        self.grandma = grandma
        self.grandpa = grandpa
        self.umbrella = umbrella
        self.time = time

    def goalTest(self):
        return self.amogh == self.ameya == self.grandma == self.grandpa == 'R' and self.time <= 60

    def moveGen(self):
        children = []
        times = {
            'Amogh': 5,
            'Ameya': 10,
            'Grandma': 20,
            'Grandpa': 25
        }

        people = ['Amogh', 'Ameya', 'Grandma', 'Grandpa']
        positions = {
            'Amogh': self.amogh,
            'Ameya': self.ameya,
            'Grandma': self.grandma,
            'Grandpa': self.grandpa
        }

        if self.umbrella == 'L':
            for i in range(len(people)):
                for j in range(i, len(people)):
                    p1 = people[i]
                    p2 = people[j]
                    if positions[p1] == 'L' and positions[p2] == 'L':
                        new_pos = positions.copy()
                        new_pos[p1] = 'R'
                        new_pos[p2] = 'R'
                        t = max(times[p1], times[p2])
                        new_time = self.time + t
                        if new_time <= 60:
                            new_state = State(
                                amogh=new_pos['Amogh'],
                                ameya=new_pos['Ameya'],
                                grandma=new_pos['Grandma'],
                                grandpa=new_pos['Grandpa'],
                                umbrella='R',
                                time=new_time
                            )
                            children.append(new_state)
        else:
            for p in people:
                if positions[p] == 'R':
                    new_pos = positions.copy()
                    new_pos[p] = 'L'
                    t = times[p]
                    new_time = self.time + t
                    if new_time <= 60:
                        new_state = State(
                            amogh=new_pos['Amogh'],
                            ameya=new_pos['Ameya'],
                            grandma=new_pos['Grandma'],
                            grandpa=new_pos['Grandpa'],
                            umbrella='L',
                            time=new_time
                        )
                        children.append(new_state)

        return children

    def __eq__(self, other):
        return (
            self.amogh == other.amogh and
            self.ameya == other.ameya and
            self.grandma == other.grandma and
            self.grandpa == other.grandpa and
            self.umbrella == other.umbrella and
            self.time == other.time
        )

    def __hash__(self):
        return hash((self.amogh, self.ameya, self.grandma, self.grandpa, self.umbrella, self.time))

    def __str__(self):
        return f"Amogh: {self.amogh} Ameya: {self.ameya} Grandma: {self.grandma} Grandpa: {self.grandpa} Umbrella: {self.umbrella} Time: {self.time}"


def removeSeen(children, OPEN, CLOSED):
    open_nodes = [node for node, _ in OPEN]
    closed_nodes = [node for node, _ in CLOSED]
    return [c for c in children if c not in open_nodes and c not in closed_nodes]


def reconstructPath(node_pair, CLOSED):
    path = []
    parent_map = {}
    for node, parent in CLOSED:
        parent_map[node] = parent

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
            print("Goal found")
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

    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair

        if N.goalTest():
            print("Goal found")
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


# Run
start_state = State('L', 'L', 'L', 'L', 'L', 0)

print("------ BFS ------")
bfs(start_state)

print("\n------ DFS ------")
dfs(start_state)
