import subprocess

def handle(args, stdout: None, stdin: None, stderr: None, docker_composes: []):
    return ('up', ['-d', '--force-recreate'] + args)