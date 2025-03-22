import re
import numpy as np


def read_catalog(file_path):
    lines = open(file_path, "r", encoding="utf-8").readlines()
    current_group = ""
    groups = {}
    for line in lines:
        if line.startswith("+"):
            current_group = line[1:].strip()
        elif groups.get(current_group):
            groups[current_group].append(line.strip())
        else:
            groups[current_group] = [line.strip()]
    return groups

def catalog_contains(catalog, file_path):
    for item in catalog:
        if item.endswith(file_path):
            return True

def analyze_graph(file_path, catalog):
    output = ""
    input_lines = open(file_path, "r", encoding="utf-8").readlines()

    clusters = {}
    cluster_id = 0
    for group, files in catalog.items():
        clusters[group] = cluster_id
        cluster_id += 1

    nodes = {}
    to_deg = np.zeros((len(clusters), len(clusters)))
    cluster_scale = np.zeros(len(clusters))

    current_section = 0
    for line in input_lines:
        if len(line.strip()) == 0:
            current_section += 1
        elif current_section == 3: # Nodes
            match = re.match(r'^"([^"]*\.tsx?)"', line.strip())
            if match:
                for group, files in catalog.items():
                    if catalog_contains(files, match.group(1)):
                        nodes[match.group(1)] = clusters[group]
                        break
        elif current_section == 4: # Edges
            match = re.match(r'^"([^"]*\.tsx?)"\s*->\s*"([^"]*\.tsx?)"', line.strip())
            if match:
                source_match = False
                target_match = False
                for group, files in catalog.items():
                    if catalog_contains(files, match.group(1)):
                        source_match = True
                    if catalog_contains(files, match.group(2)):
                        target_match = True
                if source_match and target_match:
                    to_deg[nodes[match.group(1)], nodes[match.group(2)]] += 1

    for node, id in nodes.items():
        cluster_scale[id] += 1

    output += "Clusters\n"
    for group, id in clusters.items():
        output += f"{group}: ID = {id}, NodeCount = {int(cluster_scale[id])}\n"

    output += "\n\n\nConnectivity\n"
    for i in range(cluster_id):
        for j in range(cluster_id):
            output += f"{int(to_deg[i][j])}, "
        output += "\n"
    return output

if __name__ == "__main__":
    catalog = read_catalog("catalog-filtered.txt")
    output = analyze_graph("dep-web-original.dot", catalog)
    print(output)
    with open("connectivity.txt", "w", encoding="utf-8") as f:
        f.write(output)