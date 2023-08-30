import subprocess
from os import path

def handle(args, stdout: None, stdin: None, stderr: None, docker_composes: [], env: None):
    if len([x for x in args if x.startswith('-')]) > 0:
        print(f"Unknown parameters in {args}")
        return False

    curdir = path.realpath('.')
    docker_run_cmd = [
        "/usr/bin/docker",
        "run", "-it", "--rm", "-v", f"{curdir}:/app", "-w", "/app"
    ]

    entrypoint = "/bin/sh"
    if len(args) > 1:
        entrypoint = args.pop()
        docker_run_cmd += [entrypoint]
    
    docker_run_cmd += ["--entrypoint", entrypoint]

    for key in env:
        docker_run_cmd += ["-e", f"{key}={env[key]}"]
        
    docker_run_cmd += args
    
    subprocess.Popen(docker_run_cmd, stdout=stdout, stderr=stderr, stdin=stdin, env=env).wait()

    return True