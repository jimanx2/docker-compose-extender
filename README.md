# docker-compose-extender

A bash function to shorten `docker-compose -f 1.yaml -f 2.yaml -f 3.yaml` into `@compose`. Also adds extensibility by wrapping the docker-compose command.

## Requirements

1. bash
2. python3
3. `pip3 install -r requirements.txt`

## Usage

1. clone this repo somewhere accessible (eg: $HOME/docker-compose-extender)
2. create or modify `.composes` file (optional)
3. run the following:
```
source $HOME/docker-compose-extender/docker-compose-extender.bash
```

Note: Add above line to .bashrc for easy access

## Existing Plugins

### `down`

This action will cause the script to ask user confirmation before proceeding with the  
actual `down` action

Sample run:
```sh
$ @compose up -d
[+] Running 2/2
 ⠿ hello Pulled                                10.4s
 ⠿ b237fe92c417 Pull complete                   6.5s
[+] Running 2/2
 ⠿ Network docker-compose-extender_default    Created                                                                                                                                                                                                                                                                           0.0s
 ⠿ Container docker-compose-extender-hello-1  Started                                                                                                                                                                                                                                                                           0.8s
$ @compose down
This will remove all associated resources to this docker-compose project (such as volumes and networks). Re-run with --force switch to skip this message.
$ @compose down --force
[+] Running 2/2
 ⠿ Container docker-compose-extender-hello-1  Removed                                                                                                                                                                                                                                                                           0.0s
 ⠿ Network docker-compose-extender_default    Removed
```

### `recreate`

This action will run both `docker-compose down` and `docker-compose up -d` in single command

Sample run:
```sh
$ @compose up -d
[+] Running 2/2
 ⠿ Network docker-compose-extender_default    Created                                                                                                                                                                                                                                                                           0.0s
 ⠿ Container docker-compose-extender-hello-1  Started                                                                                                                                                                                                                                                                           0.5s
$ @compose recreate
[+] Running 1/1
 ⠿ Container docker-compose-extender-hello-1  Started
```

### `xrun`

This action will execute a `docker run <image> <entrypoint:default:/bin/sh>` and automatically  
mount current directory to /app inside the container

Sample run:
```sh
$ @compose xrun php:alpine
Unable to find image 'php:alpine' locally
alpine: Pulling from library/php
7264a8db6415: Already exists 
404102781aa3: Already exists 
7410f32c8672: Already exists 
956dc56ebfa1: Already exists 
ab667de42022: Already exists 
f3bae9f71b13: Already exists 
32b0a344272d: Already exists 
9c4e0b6e75a2: Already exists 
535c52f5d5e7: Already exists 
Digest: sha256:5497eac8cf1089126bf5ea906abffcb69f6129286921ed1a679290d558047c55
Status: Downloaded newer image for php:alpine
/app # 
```

## Plugin development

Refer `$HOME/docker-compose-extender/actions` folder
