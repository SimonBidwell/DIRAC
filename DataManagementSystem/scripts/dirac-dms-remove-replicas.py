#!/usr/bin/env python
from DIRAC.Core.Base.Script import parseCommandLine
parseCommandLine()
########################################################################
# $HeadURL$
########################################################################
__RCSID__   = "$Id$"
__VERSION__ = "$ $"

from DIRAC.Core.Utilities.List                        import sortList,breakListIntoChunks
from DIRAC.DataManagementSystem.Client.ReplicaManager import ReplicaManager
rm = ReplicaManager()
import os,sys

if len(sys.argv) < 3:
  print 'Usage: ./dirac-dms-remove-replicas.py <LFN | fileContainingLFNs> SE [SE] ...'
  sys.exit()
else:
  inputFileName = sys.argv[1]
  storageElementNames = sys.argv[2:]

if os.path.exists(inputFileName):
  inputFile = open(inputFileName,'r')
  string = inputFile.read()
  lfns = string.splitlines()
  inputFile.close()
else:
  lfns = [inputFileName]

for lfnList in breakListIntoChunks(sortList(lfns,True),500):
  for storageElementName in storageElementNames:
    res = rm.removeReplica(storageElementName,lfnList)
    if not res['OK']:
      print res['Message']
    for lfn in sortList(res['Value']['Successful'].keys()):
      print 'Successfully removed %s replica of %s' % (storageElementName,lfn)
    for lfn in sortList(res['Value']['Failed'].keys()):
      message = res['Value']['Failed'][lfn]
      print 'Failed to remove %s replica of %s: %s' % (storageElementName,lfn,message)
