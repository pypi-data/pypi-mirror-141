# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

import os
import logging
from time import gmtime, strftime

from cegalprizm.hub import HubConnector

from . import logger
from .task_registry import get_task_registry

import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--name', help='Name to be assigned to the scripting environment', required=True, default='python')
parser.add_argument('--logdir', help='Path to directory in which to write the logfile', required=False)
parser.add_argument('--loglevel', help='Level of logging [D, I, W, E]', required=False, default='I')

args = parser.parse_args()

if args.loglevel == 'D':
    level = logging.DEBUG
elif args.loglevel == 'W':
    level = logging.WARNING
elif args.loglevel == 'E':
    level = logging.ERROR
else:
    level = logging.INFO

if args.logdir is not None:
    if not os.path.isdir(args.logdir):
        print("Error: Specified logdir does not exist")
        exit(0)

    filename = f"scripting-server_{strftime('%Y-%m-%d_%H-%M-%S', gmtime())}.log"

    logging.basicConfig(
        handlers=[logging.FileHandler(filename=os.path.join(args.logdir, filename), encoding='utf-8', mode='a+')],
        format='%(asctime)s [%(levelname)-8s] %(message)s',
        level=level,
        datefmt='%Y-%m-%d %H:%M:%S')
else:
    logging.basicConfig(level=level)

try:
    join_token = os.environ["CEGAL_HUB_CONNECTOR_JOIN_TOKEN"]
except:
    join_token = ""

logging.getLogger("cegalprizm.keystone_auth").setLevel(level)
logging.getLogger("cegalprizm.hub").setLevel(level)

logger.info("Starting Scripting Server")

labels = {
    "scripting-environment": args.name
}

connector = HubConnector(wellknown_identifier="cegal.scripting_server",
                         friendly_name="Cegal Scripting Server",
                         description="A Cegal provided server allowing python code to be executed remotely using Cegal Hub",
                         version="0.0.1",
                         build_version="local",
                         supports_public_requests=True,
                         join_token=join_token,
                         additional_labels=labels)

connector.start(get_task_registry())
