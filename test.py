#!/usr/bin/env python2

from __future__ import print_function
from bcf.logger import Logger
from bcf.command import Command
from bcf.plan import Plan
from fdisk import Fdisk


# Helper functions - preparing bash command strings

def checkPartitionsCountString(disk, count):
    return 'if [[ `lsblk "{disk}" | wc -l` -ne "{lineCount}" ]]; then exit 1; else exit 0; fi'.format(disk=disk, lineCount=count+2)

# Command preparation functions

def checkInitialPartitionsCount():
    return Command(
        checkPartitionsCountString('/dev/sda', 0),
        'Check initial partitions count')

def createPartitions():
    sda = Fdisk('/dev/sda')
    sda.addPrimaryPartition('+128M', '83')
    sda.addPrimaryPartition('+80G', '83')
    sda.addPrimaryPartition('+6G', '82')
    sda.addExtendedPartition()
    sda.addLogicalPartition('+20G', '83')
    sda.addLogicalPartition('+20G', '83')
    sda.addLogicalPartition('', '83')
    sda.setPartitionBootable(1)
    sda.writePartitionTable()
    return Command(
        sda.getBashCommandString(),
        'Create partitions') 

def checkCreatedPartitionsCount():
    return Command(
        checkPartitionsCountString('/dev/sda', 7),
        'Check created partitions count')

def getPlan():
    l = Logger('logs/diskutils.log')

    commands = [
            checkInitialPartitionsCount(),
            createPartitions(),
            checkCreatedPartitionsCount()]

    return Plan('TestPlan', commands, l)


if __name__ == '__main__':
    getPlan().execute()
    # print(t)
