def has_cycle(graph, node, visited, stack, cyclic_path):
    visited[node] = True
    stack[node] = True
    cyclic_path.append(node)

    for neighbor in graph.get(node, []):
        if not visited[neighbor]:
            if has_cycle(graph, neighbor, visited, stack, cyclic_path):
                return True
        elif stack[neighbor]:
            # Cyclic path found, print it
            index = cyclic_path.index(neighbor)
            cyclic_path.append(node)
            print("Cyclic Path:", " -> ".join(cyclic_path[index:]))
            return True

    stack[node] = False
    cyclic_path.pop()
    return False

def check_dependency_graph(dependency_graph):
    visited = {node: False for node in dependency_graph}
    stack = {node: False for node in dependency_graph}

    for node in dependency_graph:
        if not visited[node]:
            cyclic_path = []
            if has_cycle(dependency_graph, node, visited, stack, cyclic_path):
                return "The dependency graph contains cyclic dependencies."
    
    return "The dependency graph does not contain cyclic dependencies."

dependency_graph = {
    'COMS0': [],
    'COMS1': ['COMS0'],
    'COMS2': ['COMS1'],
    'COMS3': ['COMS2'],
    'COMS4': ['COMS1', 'COMS3'],
    'COMS5': ['COMS4'],
    'COMS6': ['COMS1', 'COMS2', 'COMS3', 'COMS4'],
    'COMS7': ['COMS2', 'COMS6'],
    'COMS8': ['COMS4', 'COMS7', 'COMS5'],
    'COMS9': ['COMS3', 'COMS6', 'COMS5'],
    'COMS10': ['COMS3', 'COMS8'],
    'COMS11': ['COMS8'],
    'COMS12': ['COMS1', 'COMS11', 'COMS9'],
    'COMS13': ['COMS0', 'COMS3', 'COMS9', 'COMS11'],
    'COMS14': ['COMS13', 'COMS12'],
    'COMS15': ['COMS13', 'COMS14'],
    'COMS16': ['COMS13', 'COMS15'],
    'COMS17': ['COMS15', 'COMS16'],
    'COMS18': ['COMS12', 'COMS13', 'COMS14'],
    'COMS19': ['COMS6', 'COMS9', 'COMS14', 'COMS16']
}




result = check_dependency_graph(dependency_graph)
print(result)
