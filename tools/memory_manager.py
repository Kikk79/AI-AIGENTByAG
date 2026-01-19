import os
import datetime

# Paths
BRAIN_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "brain")
SHORT_TERM = os.path.join(BRAIN_DIR, "short_term.md")
MID_TERM = os.path.join(BRAIN_DIR, "mid_term.md")
LONG_TERM = os.path.join(BRAIN_DIR, "long_term.md")

def read_memory():
    """Reads all memory layers and returns a combined context string."""
    context = ""
    
    try:
        with open(LONG_TERM, 'r', encoding='utf-8') as f:
            context += f"--- LONG TERM MEMORY ---\n{f.read()}\n\n"
        with open(MID_TERM, 'r', encoding='utf-8') as f:
            context += f"--- MID TERM MEMORY ---\n{f.read()}\n\n"
        with open(SHORT_TERM, 'r', encoding='utf-8') as f:
            context += f"--- SHORT TERM MEMORY (ACTIVE) ---\n{f.read()}\n"
    except FileNotFoundError as e:
        print(f"Memory Error: {e}")
        return "System Error: Memory banks inaccessible."

    return context

def update_memory(layer, content, mode='append'):
    """
    Updates a specific memory layer.
    layer: 'short', 'mid', 'long'
    content: The text to write
    mode: 'append' (default) or 'overwrite'
    """
    target_file = None
    if layer == 'short': target_file = SHORT_TERM
    elif layer == 'mid': target_file = MID_TERM
    elif layer == 'long': target_file = LONG_TERM
    else: return False, "Invalid memory layer."

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_content = f"\n[{timestamp}] {content}" if mode == 'append' else content

    try:
        write_mode = 'a' if mode == 'append' else 'w'
        with open(target_file, write_mode, encoding='utf-8') as f:
            f.write(formatted_content)
        return True, f"Memory ({layer}) updated."
    except Exception as e:
        return False, f"Write Error: {e}"

def clear_short_term():
    """Wipes short term memory but keeps the header."""
    header = "# Short-Term Memory (Active Buffer)\n**Retention Policy:** Cleared/Summarized after session end.\n**Current Context:**\n"
    return update_memory('short', header, mode='overwrite')

if __name__ == "__main__":
    # Test
    print(read_memory())
    # update_memory('short', "Testing memory write.")
