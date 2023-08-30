import subprocess, yaml, logging

def handle(args, stdout: None, stdin: None, stderr: None, docker_composes: []):
    if not '--force' in args:
        print("This will remove all associated resources to this docker-compose project (such as volumes and networks). Re-run with --force switch to skip this message.")
        return False
        
    return ('down', [])