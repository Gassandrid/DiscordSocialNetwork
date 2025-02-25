import json
import os
import re

def sanitize_filename(name):
    """Sanitize a filename to remove characters that could cause issues"""
    # Replace characters that aren't allowed in filenames
    return re.sub(r'[\\/*?:"<>|]', "_", name)

def sanitize_tag(name):
    """Sanitize a tag for Obsidian"""
    # Remove spaces and special characters for tags
    # First replace spaces with hyphens
    name = re.sub(r'\s+', "-", name)
    # Then remove any characters that aren't alphanumeric, underscore, or hyphen
    name = re.sub(r'[^\w\-]', "", name)
    # Ensure the tag doesn't start with a number
    if name and name[0].isdigit():
        name = "t" + name
    return name

def create_obsidian_notes(json_file, output_dir):
    """Convert Discord friends JSON to Obsidian markdown notes"""
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    # Load the JSON data
    with open(json_file, 'r', encoding='utf-8') as f:
        friends_data = json.load(f)
    
    print(f"Loaded {len(friends_data)} friends from {json_file}")
    
    # Process each friend
    for friend_name, friend_info in friends_data.items():
        # Sanitize filename
        safe_filename = sanitize_filename(friend_name)
        file_path = os.path.join(output_dir, f"{safe_filename}.md")
        
        # Get mutual friends and servers
        mutual_friends = friend_info.get("mutual_friends", [])
        mutual_servers = friend_info.get("mutual_servers", [])
        
        # Create tag strings for YAML frontmatter
        tags = []
        for server in mutual_servers:
            # Sanitize server names for tags
            tag = sanitize_tag(server)
            if tag:  # Only add non-empty tags
                tags.append(tag)
        
        # Create the markdown content
        content = ["---"]
        content.append(f"name: {friend_name}")
        if tags:
            content.append("tags:")
            for tag in tags:
                content.append(f"  - {tag}")
        content.append("---")
        content.append("")
        content.append(f"# {friend_name}")
        content.append("")
        
        # Add mutual friends section
        if mutual_friends:
            content.append("## Mutual Friends")
            content.append("")
            for mutual_friend in mutual_friends:
                content.append(f"- [[{mutual_friend}]]")
            content.append("")
        
        # Add mutual servers section
        if mutual_servers:
            content.append("## Mutual Servers")
            content.append("")
            for server in mutual_servers:
                content.append(f"- {server}")
        
        # Write the file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        
        print(f"Created note for {friend_name}")
    
    print(f"Conversion complete! {len(friends_data)} notes created in {output_dir}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert Discord friends JSON to Obsidian markdown notes")
    parser.add_argument("--input", default="friends.json", help="Path to the friends.json file")
    parser.add_argument("--output", default="Markdown", help="Output directory for markdown files")
    
    args = parser.parse_args()
    
    create_obsidian_notes(args.input, args.output)
