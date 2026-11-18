# CS1005 Discrete Structures - Fall 2026 - Course Project
# R = 3259 (916 + 586 + 838 + 919)
# Department pair number = 29 -> (1, 12)
# Random networks = 24
# Swap attempts per network = 6 x number of edges
# Random seed = 3259

import gzip

roll_numbers = [916, 586, 838, 919]

edges_file = "email-Eu-core.txt.gz"
departments_file = "email-Eu-core-department-labels.txt.gz"


def open_text(file_path):
    if file_path.endswith(".gz"):
        return gzip.open(file_path, "rt")
    return open(file_path, "r")


def load_graph(path=edges_file):
    edges = set()

    with open_text(path) as file:
        for line in file:
            parts = line.split()

            if len(parts) != 2:
                continue

            sender = int(parts[0])
            receiver = int(parts[1])

            if sender != receiver:
                edges.add((sender, receiver))

    return sorted(edges)


def load_departments(path=departments_file):
    dept_of = {}

    with open_text(path) as file:
        for line in file:
            parts = line.split()

            if len(parts) != 2:
                continue

            node = int(parts[0])
            department = int(parts[1])

            dept_of[node] = department

    return dept_of


def internal_edge_counts(edges, dept_of):
    counts = {}

    for department in dept_of.values():
        counts[department] = 0

    for sender, receiver in edges:
        if sender in dept_of and receiver in dept_of:
            if dept_of[sender] == dept_of[receiver]:
                counts[dept_of[sender]] += 1

    return counts


def top20(counts):
    ranked = sorted(counts, key=lambda department: (-counts[department], department))
    return ranked[:20]


def derive_parameters(roll_numbers):
    R = sum(roll_numbers)

    pairs = []

    for i in range(20):
        for j in range(i + 1, 20):
            pairs.append((i, j))

    pair_number = R % 190
    i, j = pairs[pair_number]

    parameters = {
        "R": R,
        "pair_number": pair_number,
        "i": i,
        "j": j,
        "num_networks": 20 + (R % 31),
        "attempt_multiplier": 5 + (R % 6),
        "seed": R
    }

    return parameters


def department_nodes(dept_of, department_id):
    nodes = []

    for node, department in dept_of.items():
        if department == department_id:
            nodes.append(node)

    return sorted(nodes)


def build_subgraph(edges, dept_nodes):
    node_set = set(dept_nodes)
    subgraph = []

    for sender, receiver in edges:
        if sender in node_set and receiver in node_set:
            subgraph.append((sender, receiver))

    return subgraph


def main():
    edges = load_graph()
    dept_of = load_departments()

    counts = internal_edge_counts(edges, dept_of)
    top = top20(counts)

    parameters = derive_parameters(roll_numbers)

    dept_a = top[parameters["i"]]
    dept_b = top[parameters["j"]]

    print("T1: Cleaned Graph")
    print("Total nodes:", len(dept_of))
    print("Total edges:", len(edges))
    print("Total departments:", len(counts))

    print("\nTop 20 Departments")

    for index, department in enumerate(top):
        print("Index:", index,
              "| Department:", department,
              "| Internal edges:", counts[department])

    print("\nGroup Parameters")
    print("R:", parameters["R"])
    print("Pair number:", parameters["pair_number"])
    print("Department pair:", (parameters["i"], parameters["j"]))
    print("Department A:", dept_a)
    print("Department B:", dept_b)
    print("Random networks:", parameters["num_networks"])
    print("Swap attempts:", parameters["attempt_multiplier"], "x number of edges")
    print("Random seed:", parameters["seed"])

    print("\nT2: Department Subgraphs")

    department_data = {}

    for name, department_id in [("A", dept_a), ("B", dept_b)]:
        nodes = department_nodes(dept_of, department_id)
        subgraph = build_subgraph(edges, nodes)

        department_data[name] = {
            "department_id": department_id,
            "nodes": nodes,
            "edges": subgraph
        }

        print("\nDepartment", name)
        print("Department ID:", department_id)
        print("Number of nodes:", len(nodes))
        print("Number of edges:", len(subgraph))

    return {
        "edges": edges,
        "dept_of": dept_of,
        "parameters": parameters,
        "top20": top,
        "departments": department_data
    }


if __name__ == "__main__":
    project_data = main()
