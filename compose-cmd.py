#!/usr/bin/env python3

import sys, logging, subprocess

from os import path
from datetime import datetime
from optparse import (OptionParser,BadOptionError,AmbiguousOptionError)
import actions

print(actions)

class PassThroughOptionParser(OptionParser):
    """
    An unknown option pass-through implementation of OptionParser.

    When unknown arguments are encountered, bundle with largs and try again,
    until rargs is depleted.  

    sys.exit(status) will still be called if a known argument is passed
    incorrectly (e.g. missing arguments or bad argument types, etc.)        
    """
    def _process_args(self, largs, rargs, values):
        while rargs:
            try:
                OptionParser._process_args(self,largs,rargs,values)
            except (BadOptionError, AmbiguousOptionError) as e:
                largs.append(e.opt_str)

# Create and configure logger
rundate = datetime.now().strftime("%Y%m%d")
logging.basicConfig(filename=f"/tmp/compose-{rundate}.log",
format='%(asctime)s %(message)s',
filemode='a+')

# options
usage = "usage: @compose [options] args"
parser = PassThroughOptionParser(usage)
parser.add_option("-f", "--file", dest="composes_filename", help="read data from COMPOSES_FILENAME (default: .composes)")
(options, args) = parser.parse_args()

def find_in_parent(file, dir = path.realpath('.'), level = 0):
    filename = path.join(dir, file)
    parent = path.realpath(path.join(dir, ".."))
    if not path.isfile(filename):
        if dir == path.splitdrive(dir)[0] or dir == "/":
            logger.error("Already at root directory!")
            return False
        return find_in_parent(file, parent, level + 1)
    return filename
    
def known_local_action(action):
    return False

def execute_local_action(action):
    return action

if __name__ == "__main__":
    # Creating an object
    logger = logging.getLogger()

    # Setting the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)
    
    composes_filename = ".composes"
    if (options.composes_filename != None):
        composes_filename = options.composes_filename

    compose_path = find_in_parent(composes_filename)

    # if not compose_path:
    #    raise Exception(f"Failed to find {composes_filename} file in current directory or parent directories.")

    docker_compose_cmd = [
        "/usr/bin/docker",
        "compose"
    ]

    if compose_path != False:
        logger.debug(f"Using {composes_filename} file from {compose_path}")

        with open(compose_path) as f_composes:
            yaml_files = map(lambda x: x.strip(), f_composes.readlines())

        for filename in yaml_files:
            print(f"Loading yaml: {filename}")
            docker_compose_cmd = docker_compose_cmd + ["-f", filename]

    logging.debug(f"Docker Compose CMD: {docker_compose_cmd}")

    local_cmd_action = args.pop(0)
    logging.debug(f"Action: {local_cmd_action}, args: {args}")

    docker_cmd_action = local_cmd_action
    if (known_local_action(local_cmd_action)):
        docker_cmd_action = execute_local_action(local_cmd_action)

    docker_compose_cmd = docker_compose_cmd + [docker_cmd_action] + args
    
    logging.debug(f"Docker Compose CMD: {docker_compose_cmd}")

    stdout = open('/dev/stdout', 'a')
    stderr = open('/dev/stderr', 'a')
    stdin = open('/dev/stdin', 'r')

    subprocess.run(docker_compose_cmd, stdout=stdout, stderr=stderr, stdin=stdin)

    stdin.close()
    stderr.close()
    stdout.close()