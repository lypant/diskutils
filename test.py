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

def createBootPartitionFileSystem():
    return Command(
        'mkfs.fat -F16 /dev/sda1',
        'Create boot partition file system')

def mountBootPartition():
    return Command(
        'mount /dev/sda1 /mnt',
        'Mount boot partition')

def createSyslinuxDirectory():
    return Command(
        'mkdir -p /mnt/boot/syslinux',
        'Create syslinux directory')

def copySyslinuxC32Files():
    return Command(
        'cp /usr/lib/syslinux/bios/*.c32 /mnt/boot/syslinux/',
        'Copy syslinux *.c32 files')

def installSyslinux():
    return Command(
        'syslinux --install /dev/sda1',
        'Install syslinux')

def writeMbr():
    return Command(
        'dd bs=440 count=1 if=/usr/lib/syslinux/bios/mbr.bin of=/dev/sda')

def copySyslinuxConfig():
    return Command(
        'cp test_syslinux.cfg /mnt/boot/syslinux/syslinux.cfg',
        'Copy syslinux config')

def unmountBootPartition():
    return Command(
        'umount /dev/sda1',
        'Unmount boot partition')

def getPlan():
    l = Logger('logs/TestPartitioning.log')

    commands = [
            checkInitialPartitionsCount(),
            createPartitions(),
            checkCreatedPartitionsCount(),
            createBootPartitionFileSystem(),
            mountBootPartition(),
            createSyslinuxDirectory(),
            copySyslinuxC32Files(),
            installSyslinux(),
            writeMbr(),
            copySyslinuxConfig(),
            unmountBootPartition()]

    return Plan('TestPartitioning', commands, l)


if __name__ == '__main__':
    getPlan().execute()
    # print(t)
