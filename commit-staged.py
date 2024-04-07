import subprocess
import openai
import os
import yaml
from openai import Client

# Default token threshold
TOKEN_THRESHOLD = 10000

# Check for dev.config.yaml and override TOKEN_THRESHOLD if present
config_path = 'dev.config.yaml'
if os.path.exists(config_path):
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
        TOKEN_THRESHOLD = config.get('token_threshold', TOKEN_THRESHOLD)

# Setup OpenAI Client
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
client = Client()

def estimate_token_count(text):
    """Estimate the number of tokens in a given text."""
    # Roughly estimate token count. This is a simplification.
    return len(text.split())

def get_staged_files():
    """Get a list of staged files."""
    staged_files = subprocess.check_output(['git', 'diff', '--cached', '--name-only'], text=True)
    return staged_files.strip().split('\n')

def get_staged_files_diff():
    """Get the diff of staged files."""
    diff = subprocess.check_output(['git', 'diff', '--cached'], text=True)
    return diff

def generate_commit_message(diff):
    """Generate a commit message based on the diff using OpenAI."""
    # Define the role and instructions specifically for the task
    role = """
    As an AI specialized in understanding code changes, your role is to analyze 
    the differences in code files and generate a concise, meaningful commit message. 
    You should consider the context and purpose of the changes, focusing on 
    summarizing the modifications in a way that is clear and useful for other 
    developers reviewing the commit history.
    """

    instructions = """
    Given the provided diff of staged files, your task is to generate a commit 
    message that begins with a brief narrative paragraph summarizing the overall 
    purpose and impact of the changes. This paragraph should provide a clear, 
    high-level overview suitable for developers reviewing the commit history.

    If there are multiple distinct changes, follow the narrative paragraph with 
    a bulleted list that details each specific change:
    
    - Describe the motivation behind each change.
    - Outline what specific modifications were made.
    - Explain how these changes impact the functionality or structure of the code.

    The initial narrative should set the context, while the bulleted list (if 
    applicable) breaks down the specifics, ensuring the message is informative 
    and organized. Emphasize brevity and clarity throughout the message.
    """

    courtesy = """
    Your expertise in translating code changes into clear, descriptive commit 
    messages is greatly appreciated. Thank you for assisting in maintaining a 
    coherent and informative commit history.
    """

    # Estimate token count for the operation
    total_tokens = sum(map(estimate_token_count, [role, instructions, courtesy, diff]))
    print(f"Estimated token count for this operation: {total_tokens}")
    print("API Provider: OpenAI")
    print("Model: gpt-4")

    # Check if the estimated token count exceeds the threshold
    if total_tokens > TOKEN_THRESHOLD:
        confirmation = input(f"The estimated token count ({total_tokens}) exceeds the threshold of {TOKEN_THRESHOLD}. Do you want to proceed? (y/n): ")
        if confirmation.lower() not in ["y", "yes"]:
            print("Operation canceled by the user.")
            return None

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": role},
            {"role": "system", "content": instructions},
            {"role": "user", "content": f"diff:\n{diff}"},
            {"role": "user", "content": courtesy} 
        ]
    )

    # Assuming the response structure fits your needs, extract the commit message
    commit_message = response.choices[0].message.content  # Adjust based on actual response structure
    return commit_message.strip()

def commit_changes(commit_message):
    """Commit the staged changes with the generated commit message."""
    subprocess.run(['git', 'commit', '-m', commit_message], check=True)

def user_confirmation(staged_files, commit_message):
    """Ask user for confirmation to proceed with the commit."""
    # ANSI color codes
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'  # Reset to default color

    # Displaying "Staged files:" label in green and bold
    print(BOLD + GREEN + "Staged files:" + ENDC)
    # Displaying the list of staged files in cyan
    print(CYAN + "\n".join(staged_files) + ENDC)
    # Displaying proposed commit message in yellow
    print(YELLOW + "\nProposed commit message:\n" + commit_message + ENDC)
    # Making the confirmation prompt bold and green for visual distinction
    confirmation = input(BOLD + GREEN + "Do you want to proceed with this commit? (y/n): " + ENDC)
    return confirmation.lower() in ["y", "yes"]

def main():
    staged_files = get_staged_files()
    if not staged_files:
        print("No changes staged for commit.")
        return
    diff = get_staged_files_diff()
    commit_message = generate_commit_message(diff)
    if user_confirmation(staged_files, commit_message):
        commit_changes(commit_message)
        print(f"Committed with message: {commit_message}")
    else:
        print("Commit canceled by the user.")

if __name__ == "__main__":
    main()