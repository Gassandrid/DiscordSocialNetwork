import json
import argparse
from collections import defaultdict

def merge_user_graphs(file1, file2, output_file):
    """
    Merge two JSON files containing user relationship data into a more complete graph.
    
    Args:
        file1 (str): Path to the first JSON file
        file2 (str): Path to the second JSON file
        output_file (str): Path where the merged JSON will be saved
    
    Returns:
        dict: The merged user graph data
    """
    try:
        # Load the first JSON file
        with open(file1, 'r', encoding='utf-8') as f1:
            data1 = json.load(f1)
        
        # Load the second JSON file
        with open(file2, 'r', encoding='utf-8') as f2:
            data2 = json.load(f2)
        
        # Create a new dictionary for the merged data
        merged_data = defaultdict(lambda: {"mutual_friends": [], "mutual_servers": []})
        
        # Process all users from both files
        for source_data in [data1, data2]:
            for user, relationships in source_data.items():
                # If the user doesn't exist in merged data yet, add them
                if user not in merged_data:
                    merged_data[user] = {
                        "mutual_friends": relationships.get("mutual_friends", []),
                        "mutual_servers": relationships.get("mutual_servers", [])
                    }
                else:
                    # Merge mutual_friends lists (remove duplicates)
                    current_friends = set(merged_data[user]["mutual_friends"])
                    new_friends = set(relationships.get("mutual_friends", []))
                    merged_data[user]["mutual_friends"] = sorted(list(current_friends.union(new_friends)))
                    
                    # Merge mutual_servers lists (remove duplicates)
                    current_servers = set(merged_data[user]["mutual_servers"])
                    new_servers = set(relationships.get("mutual_servers", []))
                    merged_data[user]["mutual_servers"] = sorted(list(current_servers.union(new_servers)))
        
        # Convert defaultdict back to regular dict before saving
        merged_data = dict(merged_data)
        
        # Save the merged data to the output file
        with open(output_file, 'w', encoding='utf-8') as out_file:
            json.dump(merged_data, out_file, ensure_ascii=False, indent=2)
        
        print(f"Successfully merged data from {file1} and {file2} into {output_file}")
        return merged_data
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in one of the input files: {e}")
        return None
    except FileNotFoundError as e:
        print(f"Error: File not found: {e}")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge two user relationship JSON files")
    parser.add_argument("file1", help="Path to the first JSON file")
    parser.add_argument("file2", help="Path to the second JSON file")
    parser.add_argument("--output", "-o", default="merged_graph.json", 
                        help="Output file path (default: merged_graph.json)")
    
    args = parser.parse_args()
    merge_user_graphs(args.file1, args.file2, args.output)
