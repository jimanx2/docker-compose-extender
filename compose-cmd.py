#!/usr/bin/env python3

import sys, logging, subprocess

from os import path, environ
from datetime import datetime
from optparse import (OptionParser,BadOptionError,AmbiguousOptionError)
from dotenv import dotenv_values
from actions import *

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
    if (f"actions.{action}" in sys.modules):
        return True
    return False

def execute_local_action(action, args, **kwargs):
    return sys.modules[f"actions.{action}"].handle(args, **kwargs)

if __name__ == "__main__":
    # Creating an object
    logger = logging.getLogger()

    # Setting the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)
    
    composes_filename = ".composes"
    if (options.composes_filename != None):
        composes_filename = options.composes_filename

    compose_path = find_in_parent(composes_filename)

    env_path = path.join(path.realpath("."), ".env")
    env_sub = {}
    if path.isfile(env_path):
        env_sub = dotenv_values(env_path)

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
            yaml_files = [x for x in yaml_files if len(x) > 0 and x[0] != '#']

    else:
        yaml_files = ["docker-compose.yaml"]

    for filename in yaml_files:
        logging.debug(f"Loading yaml: {filename}")
        docker_compose_cmd = docker_compose_cmd + ["-f", filename]

    logging.debug(f"Docker Compose CMD: {docker_compose_cmd}")

    meta = {
        'stdout': open('/dev/stdout', 'a'),
        'stderr': open('/dev/stderr', 'a'),
        'stdin' : open('/dev/stdin', 'r'),
        'docker_composes': yaml_files,
        'env': env_sub
    }

    if len(args) > 0:
        local_cmd_action = args.pop(0)
        logging.debug(f"Action: {local_cmd_action}, args: {args}")

        docker_cmd_action = local_cmd_action
        if (known_local_action(local_cmd_action)):
            ret = execute_local_action(local_cmd_action, args, **meta)
            if ret == False or ret == True:
                sys.exit(0)
            (docker_cmd_action, args) = ret
            

        docker_compose_cmd = docker_compose_cmd + [docker_cmd_action] + args

    docker_compose_cmd = docker_compose_cmd + args
    
    logging.debug(f"Docker Compose CMD: {docker_compose_cmd}")

    subprocess.run(docker_compose_cmd, stdout=meta['stdout'], stderr=meta['stderr'], stdin=meta['stdin'], env=env_sub)

    for handle in meta:
        if not hasattr(meta[handle], 'close'):
            continue
        meta[handle].close()