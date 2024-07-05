import json
import os

from dotenv import dotenv_values, load_dotenv

load_dotenv()
config = dotenv_values(".env")

def get_repos_be(be_mode):
    # Load JSON data from the file
    with open('data/repo.json', 'r') as f:
        data = json.load(f)
    
    # Get the list of repositories based on the `be_mode`
    list_of_repo = data['be'].get(be_mode, [])
    
    return list_of_repo

def get_repos_fe():
    # Load JSON data from the file
    with open('data/repo.json', 'r') as f:
        data = json.load(f)

    
    # Get the list of repositories based on the `be_mode`
    list_of_repo = data.get('fe', [])
    
    return list_of_repo

def get_repos_infra():
    # Load JSON data from the file
    with open('data/repo.json', 'r') as f:
        data = json.load(f)

    
    # Get the list of repositories based on the `be_mode`
    list_of_repo = data.get('infra', [])
    
    return list_of_repo