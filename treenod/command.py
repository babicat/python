# -*- coding: utf-8 -*-
import logging
import subprocess
import os

LOGGER = logging.getLogger(__name__)


def run(cmd, input=None, shell=False, env=None):
    cmd = cmd if isinstance(cmd, list) else cmd.split()
    LOGGER.debug('run({0})'.format(cmd))

    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell, env=env) as proc:
        if input:
            proc.stdin.write(input)
            proc.stdin.close()
            proc.stdin = None

        std_out, std_err = proc.communicate()
        returncode = proc.returncode
        LOGGER.debug('stdout: {0}'.format(std_out))

    return returncode, std_out.decode(), std_err.decode()
