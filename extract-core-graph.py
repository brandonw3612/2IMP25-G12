import re

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
    # catalog = []
    # for line in lines:
    #     if not line.startswith("+"):
    #         catalog.append(line.strip())
    # return catalog

def catalog_contains(catalog, file_path):
    for item in catalog:
        if item.endswith(file_path):
            return True

def filter_graph(catalog, graph_file_path):
    output = ""
    input_lines = open(graph_file_path, "r", encoding="utf-8").readlines()
    clusters = {}
    edges = set()
    current_section = 0
    for line in input_lines:
        if len(line.strip()) == 0:
            if current_section == 3:
                for group, files in clusters.items():
                    output += f'subgraph cluster_{group} {{\n'
                    output += f'label="{group}"\n'
                    for file in files:
                        output += file
                    output += '}\n'
            elif current_section == 4:
                for edge in edges:
                    output += edge
            current_section += 1
            output += line
        elif current_section == 3: # Nodes
            match = re.match(r'^"([^"]*\.tsx?)"', line.strip())
            if match:
                for group, files in catalog.items():
                    if catalog_contains(files, match.group(1)):
                        entry = f'"{match.group(1)}" [shape = record];\n'
                        if clusters.get(group):
                            clusters[group].add(entry)
                        else:
                            clusters[group] = {entry}
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
                    entry = f'"{match.group(1)}" -> "{match.group(2)}" [color = "#595959", style = solid, arrowtail = tee, arrowhead = none, taillabel = "", label = "", headlabel = ""];\n'
                    edges.add(entry)
        else:
            output += line
    return output


if __name__ == "__main__":
    catalog = read_catalog("catalog-filtered.txt")
    out_graph = filter_graph(catalog, "dep-web-original.dot")
    with open("dep-web-core.dot", "w", encoding="utf-8") as f:
        f.write(out_graph)