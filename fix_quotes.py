import re

JS_FILE_PATH = "js/script.js"

def fix_quotes():
    with open(JS_FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # The issue is specifically in the screen specs where double quotes are used for inches inside double quotes.
    # Example: screen: "6.7" PLS LCD",
    
    # We will look for lines containing 'screen: "' and verify if they have unescaped quotes inside.
    
    # Regex explanation:
    # Look for: screen: "
    # Capture group 1: any characters until the next "
    # Check if followed by more text and another "
    
    # A safer approach for this specific dataset created by me:
    # Replace ` screen: "` followed by a number and a quote, with escaped quote.
    
    # Let's iterate line by line to be safe.
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if 'screen:' in line:
            # Check if line has structure like: screen: "6.7" AMOLED",
            # We want to escape the inner quote.
            # We can replace the inch mark quote " with \" just for the screen line.
            
            # Simple heuristic: If there are more than 2 quotes in the value part, we have a problem.
            # Typical line:            screen: "6.7" PLS LCD",
            
            # Split by screen: to get the value part
            parts = line.split('screen:')
            if len(parts) > 1:
                prefix = parts[0] + 'screen:'
                value_part = parts[1]
                
                # Count quotes in value part
                quote_count = value_part.count('"')
                
                if quote_count > 2:
                    # We have nested quotes.
                    # Assume the outer ones are the boundaries.
                    # We need to escape the inner ones.
                    
                    # Find first and last quote indices
                    first_q = value_part.find('"')
                    last_q = value_part.rfind('"')
                    
                    inner_text = value_part[first_q+1 : last_q]
                    # Escape quotes in inner text
                    fixed_inner = inner_text.replace('"', '\\"')
                    
                    new_value_part = value_part[:first_q+1] + fixed_inner + value_part[last_q:]
                    line = prefix + new_value_part
                    
        new_lines.append(line)

    with open(JS_FILE_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print("✅ Fixed quote escaping in screen specs.")

if __name__ == "__main__":
    fix_quotes()
