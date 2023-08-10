import requests
import random
from github import Github

# Insert your GitHub tokens here in next format ['token1', 'token2', 'token3']
git_tokens = ['token1', 'token2', 'token3']

# Insert your GitHub names here in next format ['name1', 'name2', 'name3']
git_names = ['name1', 'name2', 'name3']

# Function to generate unique name for the file
def generate_unique_name():
    return f"quote_{random.randint(0, 150000000)}.txt"

# Function to push random quote to the GitHub repo
def push_random_quote(repo_owner, token):
    # API initialization
    g = Github(token)

    try:
        # Get the repo
        repo = g.get_repo(f"{repo_owner}/repo_name")  # Your repo name!!!

        # Get all files from the repo
        branch_files_data = repo.get_contents("", "main")

        # Get random quote
        response = requests.get("https://api.quotable.io/random")
        quote = response.json()["content"]

        # Generate unique name for the file
        random_name = generate_unique_name()

        # Check if file name is unique in the repo
        is_already_file_name_exist = any(user.path == random_name for user in branch_files_data)

        # If file name is not unique, generate new name
        if is_already_file_name_exist:
            push_random_quote(repo_owner, token)

        # Push file to the repo
        repo.create_file(
            path=random_name,
            message="Another great day with a great quote",
            content=quote,
            branch="main",
        )

        print("Pushed quote to randomQuotes")
    except Exception as e:
        print(f"Error pushing quote to randomQuotes: {e}")

# Function to start execution
def start_execution():
    for index, token in enumerate(git_tokens):
        push_random_quote(git_names[index], token)

# Start execution
start_execution()
