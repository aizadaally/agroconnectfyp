# Create this file as: manage_translations.py in the project root

import os
import subprocess
import argparse

def run_command(command):
    print(f"Running: {command}")
    subprocess.run(command, shell=True, check=True)

def make_messages(languages):
    for lang in languages:
        run_command(f"django-admin makemessages -l {lang}")

def compile_messages():
    run_command("django-admin compilemessages")

def main():
    parser = argparse.ArgumentParser(description='Manage translations for AgroConnect')
    parser.add_argument('action', choices=['make', 'compile'], 
                        help='Action to perform: make (create message files) or compile')
    
    args = parser.parse_args()
    
    # Create locale directory if it doesn't exist
    if not os.path.exists('locale'):
        os.makedirs('locale')
        print("Created locale directory")
    
    languages = ['ru', 'ky']
    
    if args.action == 'make':
        make_messages(languages)
    elif args.action == 'compile':
        compile_messages()

if __name__ == '__main__':
    main()