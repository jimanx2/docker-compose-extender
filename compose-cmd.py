#!/usr/bin/env python3

from os import path
from datetime import datetime
from optparse import OptionParser

import sys, logging, subprocess

# Create and configure logger
rundate = datetime.now().strftime("%Y%m%d")
logging.basicConfig(filename=f"/tmp/compose-{rundate}.log",
format='%(asctime)s %(message)s',
filemode='a+')

# options
usage = "usage: @compose [options] args"
parser = OptionParser(usage)
parser.add_option("-f", "--file", dest="composes_filename", help="read data from COMPOSES_FILENAME (default: .composes)")
(options, args) = parser.parse_args()

print(args)
sys.exit(0)

def find_in_parent(file, dir = path.realpath('.'), level = 0):
    filename = path.join(dir, file)
    parent = path.realpath(path.join(dir, ".."))
    if not path.isfile(filename):
        if dir == path.splitdrive(dir)[0] or dir == "/":
            logger.error("Already at root directory!")
            return False
        return find_in_parent(file, parent, level + 1)
    return filename

if __name__ == "__main__":
    # Creating an object
    logger = logging.getLogger()

    # Setting the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)
    
    composes_filename = ".composes"
    if (options.composes_filename != None):
        composes_filename = options.composes_filename

    compose_path = find_in_parent(composes_filename)

    if not compose_path:
        raise Exception(f"Failed to find {composes_filename} file in current directory or parent directories.")

    logger.debug(f"Using {composes_filename} file from {compose_path}")

    with open(compose_path) as f_composes:
        yaml_files = map(lambda x: x.strip(), f_composes.readlines())

    docker_compose_cmd = [
        "/usr/bin/docker",
        "compose"
    ]

    for filename in yaml_files:
        print(f"Loading yaml: {filename}")
        docker_compose_cmd = docker_compose_cmd + ["-f", filename]

    logging.debug(f"Docker Compose CMD: {docker_compose_cmd}")

    stdout = open('/dev/stdout', 'a')
    stderr = open('/dev/stderr', 'a')
    stdin = open('/dev/stdin', 'r')

    subprocess.run(docker_compose_cmd, stdout=stdout, stderr=stderr, stdin=stdin)

    stdin.close()
    stderr.close()
    stdout.close()