#!/usr/bin/env python

"""
test of llh_client/server communication
"""

from __future__ import absolute_import, division, print_function

__author__ = "Aaron Fienberg"

import argparse
import json
import os
import sys
import time
import pickle

import numpy as np

from freedom.llh_service.llh_client import LLHClient

N_ITERATIONS = 3600


def main():
    parser = argparse.ArgumentParser(
        description="Starts an LLH client, which then requests 3600 evals."
    )

    parser.add_argument(
        "-c", "--conf_file", type=str, help="service configuration file", required=True
    )
    parser.add_argument("-d", "--data_file", type=str, help="test data file")
    args = parser.parse_args()

    with open(args.conf_file) as f:
        params = json.load(f)

    client = LLHClient(ctrl_addr=params["ctrl_addr"], conf_timeout=20000)

    with open(args.data_file, "rb") as f:
        event = pickle.load(f)[8]

    hit_data = event["hits"]
    evt_data = event["total_charge"]
    theta = event["params"]

    llhs = []
    start = time.time()
    for i in range(N_ITERATIONS):
        llhs.append(client.eval_llh(hit_data, evt_data, theta))
    delta = time.time() - start

    print(
        f"{N_ITERATIONS} evals took {delta*1000:.3f} ms"
        f" ({delta/N_ITERATIONS*1e3:.3f} ms per eval)"
    )


if __name__ == "__main__":
    sys.exit(main())
