import os

def find_ts_files(root_directory, subdirectories, output_file):
    ts_files = []

    for subdirectory in subdirectories:
        directory = os.path.join(root_directory, subdirectory)
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".ts") or file.endswith(".tsx"):
                    relative_path = os.path.relpath(os.path.join(root, file), root_directory)
                    ts_files.append(relative_path)

    with open(output_file, "w", encoding="utf-8") as f:
        for file in ts_files:
            f.write(file + "\n")

    print(f"Found {len(ts_files)} TypeScript files. Paths saved in {output_file}")


if __name__ == "__main__":
    # Indicate root directory of the hoarder project
    root_directory = "path_to_hoarder_project"
    # Subdirectories to search for TypeScript files
    subdirectories_to_search = ["apps/web", "packages/db", "packages/shared", "packages/shared-react", "packages/trpc"]
    # Output file name
    output_file = "catalog-raw.txt"
    find_ts_files(root_directory, subdirectories_to_search, output_file)
