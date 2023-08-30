import subprocess

def handle(args, stdout: None, stdin: None, stderr: None, docker_composes: [], env: None):
    return ('up', ['-d', '--force-recreate'] + args)