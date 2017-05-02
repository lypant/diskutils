#!/usr/bin/env python2

from __future__ import print_function


class Fdisk():
    '''
    Composes bash command string capable of creating partitions for given disk
    '''
    def __init__(self, disk):
        self.disk = disk
        self.query = ''
        self.partitionsCount = 0

    def addPrimaryPartition(self, size, type):
        self.partitionsCount += 1

        # Add new partition...
        self.query += 'n\n'
        # ...primary one...
        self.query += 'p\n'
        # ...pick default number...
        self.query += '\n'
        # ...choose default starting sector...
        self.query += '\n'
        # ...set partition size
        self.query += '%s\n' % size

        # Set new partition type...
        self.query += 't\n'
        # ...for partitons other than 1 it is necessary to give the partition number
        if self.partitionsCount != 1:
            self.query += '\n'  # Use default number
        # ...set partition type
        self.query += '%s\n' % type

    def addExtendedPartition(self):
        '''
        Assumption - 3 primary partitions already exist
        '''
        # Add new partition...
        self.query += 'n\n'
        # ...extended one - necessary to select explicitly
        self.query += 'e\n'
        # ...pick partition number - done automatically for partition >=4
        # ...choose default starting sector...
        self.query += '\n'
        # ...set partition size
        self.query += '\n'  # Take all available space for container partition
        # No need to select partition type explicitly

    def addLogicalPartition(self, size, type):
        '''
        Assumption - 3 primary and fourth extended partitions already exist
        '''
        # Add new partition...
        self.query += 'n\n'
        # ...no need to select partition number explicitly
        # ...choose default starting sector...
        self.query += '\n'
        # ...set partition size
        self.query += '%s\n' % size
        # Set new partition type
        self.query += 't\n'
        # ...choose partition number...
        self.query += '\n'  # Use default number
        # ...set partition type
        self.query += '%s\n' % type

    def setPartitionBootable(self, partitionNumber):
        # Toggle bootable flag of a partition...
        self.query += 'a\n'
        if self.partitionsCount != 1:
            self.query += '%s\n' % str(partitionNumber)

    def writePartitionTable(self):
        self.query += 'w\n'

    def getBashCommandString(self):
        # TODO Check if "cat and EOFs" are needed when using python
        return 'cat <<-EOF | fdisk {disk}\n{query}EOF'.format(
                disk=self.disk,
                query=self.query)


if __name__ == '__main__':
    fd = Fdisk('/dev/sda')

    # fd.addPrimaryPartition('+128M', '83')
    # fd.addPrimaryPartition('+80G', '83')
    # fd.addPrimaryPartition('+6G', '82')
    # fd.setPartitionBootable(1)
    # fd.writePartitionTable()

    # fd.addPrimaryPartition('+128M', '83')
    # fd.setPartitionBootable(1)
    # fd.addPrimaryPartition('+80G', '83')
    # fd.addPrimaryPartition('+6G', '82')
    # fd.writePartitionTable()

    fd.addPrimaryPartition('+128M', '83')
    fd.addPrimaryPartition('+80G', '83')
    fd.addPrimaryPartition('+6G', '82')
    fd.addExtendedPartition()
    fd.addLogicalPartition('+20G', '83')
    fd.addLogicalPartition('+20G', '83')
    fd.addLogicalPartition('', '83')
    fd.setPartitionBootable(1)
    fd.writePartitionTable()

    print(fd.getBashCommandString())
