import subprocess

def handle(args, stdout: None, stdin: None, stderr: None):
    # with open('/dev/stdout', 'a'):
    #     with open('/dev/stderr', 'a'):
    #         with open('/dev/stdin', 'r'):
    #             pass
    return ('up', ['-d', '--force-recreate'])