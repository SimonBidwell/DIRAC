""" Transformation Database Client Command Line Interface. """

import re,time,types

from DIRAC import gConfig, gLogger, S_OK, S_ERROR
from DIRAC.Core.Utilities.Subprocess import shellCall

import cmd
import sys, os
import signal
import string
import time

class TransformationDBCLI(cmd.Cmd):

  def __init__( self ):
    cmd.Cmd.__init__( self )

  def setServer(self,oServer):
    self.server = oServer

  def printPair( self, key, value, separator=":" ):
    valueList = value.split( "\n" )
    print "%s%s%s %s" % ( key, " " * ( self.identSpace - len( key ) ), separator, valueList[0].strip() )
    for valueLine in valueList[ 1:-1 ]:
      print "%s  %s" % ( " " * self.identSpace, valueLine.strip() )

  def do_quit( self, *args ):
    """
    Exits the application
        Usage: quit
    """
    sys.exit( 0 )

   # overriting default help command
#  def do_help( self, args ):
#    """
#    Shows help information
#        Usage: help <command>
#        If no command is specified all commands are shown
#    """
#    if len( args ) == 0:
#      print "\nAvailable commands:\n"
#      attrList = dir( self )
#      attrList.sort()
#      for attribute in attrList:
#        if attribute.find( "do_" ) == 0:
#          self.printPair( attribute[ 3: ], getattr( self, attribute ).__doc__[ 1: ] )
#          print ""
#    else:
#      command = args.split()[0].strip()
#      try:
#        obj = getattr( self, "do_%s" % command )
#      except:
#        print "There's no such %s command" % command
#        return
#      self.printPair( command, obj.__doc__[1:] )

  def check_params(self, args, num):
    """Checks if the number of parameters correct"""
    argss = string.split(args)
    length = len(argss)
    if length < num:
      print "Error: Number of arguments provided %d less that required %d, please correct." % (length, num)
      return (False, length)
    return (argss,length)

  def check_id_or_name(self, id_or_name):
      """resolve name or Id by converting type of argument """
      if id_or_name.isdigit():
          return long(id_or_name) # its look like id
      return id_or_name

# not in use
#  def convertIDtoString(self,id):
#    return ("%08d" % (id) )



  ####################################################################
  #
  # These are the methods to transformation manipulation
  #

#  def do_getStatus(self,args):
#    """Get transformation details
#
#       usage: getStatus <transName>
#    """
#    argss = string.split(args)
#    transName = argss[0]
#    res = self.server.getTransformation(transName)
#    if not res['OK']:
#      print "Getting status of %s failed" % transName
#    else:
#      print "%s: %s" % (transName,res['Value'])
#
#  def do_setStatus(self,args):
#    """Set transformation status
#
#       usage: setStatus <transName> <Status>
#       Status <'Active' 'Stopped' 'New'>
#    """
#    argss = string.split(args)
#    transName = argss[0]
#    status = argss[1]
#    res = self.server.setTransformationStatus(transName,status)
#    if not res['OK']:
#      print "Setting status of %s to %s failed" % (transName,status)
#
#  def do_start(self,args):
#    """Start transformation
#
#       usage: start <transName>
#    """
#    argss = string.split(args)
#    transName = argss[0]
#    res = self.server.setTransformationStatus(transName,'Active')
#    if not res['OK']:
#      print "Starting %s failed" % transName
#
#  def do_stop(self,args):
#    """Stop transformation
#
#       usage: stop <transName>
#    """
#    argss = string.split(args)
#    transName = argss[0]
#    res = self.server.setTransformationStatus(transName,'Stopped')
#    if not res['OK']:
#      print "Stopping %s failed" % transName
#
#  def do_flush(self,args):
#    """Flush transformation
#
#       usage: flush <transName>
#    """
#    argss = string.split(args)
#    transName = argss[0]
#    res = self.server.setTransformationStatus(transName,'Flush')
#    if not res['OK']:
#      print "Flushing %s failed" % transName
#
#  def do_get(self,args):
#    """Get transformation definition
#
#    usage: get <transName>
#    """
#    argss = string.split(args)
#    transName = argss[0]
#    res = self.server.getTransformationDefinition(transName)
#    if not res['OK']:
#      print "Failed to get %s" % transName
#    else:
#      istream = res['InputStreams']
#      print transName,istream.keys()[0],istream.values()[0]
#
#  def do_getStat(self,args):
#    """Get transformation statistics
#
#    usage: getStat <transName>
#    """
#    argss = string.split(args)
#    transName = argss[0]
#    res = self.server.getTransformationStats(transName)
#    if not res['OK']:
#      print "Failed to get statistics for %s" % transName
#    else:
#      print res['Value']
#
#  def do_modMask(self,args):
#    """Modify transformation input definition
#
#       usage: modInput <transName> <mask>
#    """
#    argss = string.split(args)
#    transName = argss[0]
#    mask = argss[1]
#    res = self.server.modifyTransformationInput(transName,mask)
#    if not res['OK']:
#      print "Failed to modify input stream for %s" % transName
#
#  def do_getall(self,args):
#    """Get transformation details
#
#       usage: getall
#    """
#    res = self.server.getAllTransformations()
#
#  def do_shell(self,args):
#    """Execute a shell command
#
#       usage !<shell_command>
#    """
#    comm = args
#    res = shellCall(0,comm)
#    if res['OK']:
#      returnCode,stdOut,stdErr = res['Value']
#      print "%s\n%s" % (stdOut,stdErr)
#    else:
#      print res['Message']
#
#  def do_exit(self,args):
#    """ Exit the shell.
#
#    usage: exit
#    """
#    sys.exit(0)
#
#  ####################################################################
#  #
#  # These are the methods to file manipulation
#  #
#
#  def do_addFiles(self,args):
#    """Add new file list
#
#    usage: addFiles <file_list_file> [force]
#    """
#    argss = string.split(args)
#    fname = argss[0]
#    force = 0
#    if len(argss) == 2:
#      if argss[1] == 'force':
#        force = 1
#
#    files = open(fname,'r')
#    lfns = []
#    for line in files.readlines():
#      if line.strip():
#        if not re.search("^#",line):
#          lfn = line.split()[1].strip()
#          se = line.split()[0].strip()
#          lfns.append((se,lfn))
#          print se,lfn
#
#    result = self.procdb.addFiles(lfns,force)
#    if result['Status'] != "OK":
#      print "Failed to add files",fname

#  def do_addPfn(self,args):
#    """Add new replica
#
#    usage: addPfn <lfn> <se>
#    """
#
#    argss = string.split(args)
#    lfn = argss[0]
#    se = argss[1]
#    result = self.procdb.addPfn(lfn,'',se)
#    if result['Status'] != "OK":
#      print "Failed to add replica",lfn,'on',se
#
#  def do_removeFile(self,args):
#    """Remove file specified by its LFN from the Processing DB
#
#    usage: removeFile <lfn>
#    """
#
#    argss = string.split(args)
#    lfn = argss[0]
#    result = self.procdb.rmFile(lfn)
#    if result['Status'] != "OK":
#      print "Failed to remove file",lfn
#
#  def do_addDirectory(self,args):
#    """Add files from the given catalog directory
#
#    usage: addDirectory <directory> [force]
#    """
#
#    argss = string.split(args)
#    directory = argss[0]
#    force = 0
#    if len(argss) == 2:
#      if argss[1] == 'force':
#        force = 1
#
#    # KGG checking if directory has / at the end, if yes we remove it
#    directory=directory.rstrip('/')
#
#    result = self.procdb.addDirectory(directory)
#    if result['Status'] != "OK":
#      print result['Message']
#    else:
#      print result['Value']
#
#  def do_setReplicaStatus(self,args):
#    """Set replica status, usually used to mark a replica Problematic
#
#    usage: setReplicaStatus <lfn> <status> [<site>]
#
#    The <site> can be ANY
#    """
#
#    argss = string.split(args)
#    lfn = argss[0]
#    status = argss[1]
#    if len(argss) > 2:
#      site = argss[2]
#    else:
#      site = "ANY"
#
#    try:
#      result = self.procdb.setReplicaStatus(lfn,status,site)
#      if result['Status'] == "OK":
#        print "Updated status for replica of",lfn,'at',site,'to',status
#      else:
#        print 'Failed to update status for replica of',lfn,'at',site,'to',status
#    except Exception, x:
#      print "setReplicaStatus failed: ", str(x)
#
#  def do_replicas(self,args):
#    """ Get replicas for <path>
#
#        usage: replicas <path>
#    """
#    path = string.split(args)[0]
#    #print "lfn:",path
#    try:
#      result =  self.catalog.getReplicaStatus(path)
#      if result['Status'] == 'OK':
#        ind = 0
#        for se,(entry,status) in result['ReplicaStatus'].items():
#          ind += 1
#          print ind,se.ljust(15),status.ljust(10)
#      else:
#        print "Replicas: ",result['Message']
#    except Exception, x:
#      print "replicas failed: ", str(x)
#
#  def do_addFile(self,args):
#    """Add new file
#
#    usage: addFile <lfn> <se> [force]
#    """
#    argss = string.split(args)
#    lfn = argss[0]
#    se = argss[1]
#    force = 0
#    if len(argss) == 3:
#      if argss[2] == 'force':
#        force = 1
#
#    fileTuples = [(lfn,'',0,se,'',force)]
#    res = self.server.addFile(fileTuples)
#    if not res['OK']:
#      print "Failed to add %s" %lfn
#    elif not res['Value']['Successful'].has_key(lfn):
#      print "Failed to add %s" %lfn
#
#  def do_getFiles(self,args):
#    """Get files for the given production
#
#    usage: getFiles <production> [-j] [> <file_name>]
#
#    Flags:
#
#      -j  order output by job ID ( default order by file LFN )
#    """
#
#    argss = string.split(args)
#    prod = argss[0]
#    order_by_job = False
#    if len(argss) >= 2:
#      if argss[1] == '-j':
#        order_by_job = True
#
#    ofname = ''
#    if len(argss) >= 2:
#      if argss[-2] == '>':
#        ofname = argss[-1]
#        ofile = open(ofname,'w')
#
#    result = self.procdb.getFilesForTransformation(prod,order_by_job)
#    if result['Status'] == "OK":
#      files = result['Files']
#      if files:
#        #print "          LFN                                         ", \
#        #      "Status        Stream     JobID                  Used SE"
#        for f in files:
#          lfn = f['LFN']
#          status = f['Status']
#          stream = f['Stream']
#          jobid = f['JobID']
#          usedse = f['UsedSE']
#          if ofname:
#            ofile.write(lfn.ljust(50)+' '+status.rjust(10)+' '+stream.rjust(12)+' '+ \
#                        jobid.rjust(19)+' '+usedse.rjust(16)+'\n')
#          else:
#            print lfn.ljust(50),status.rjust(10),stream.rjust(12), \
#                jobid.rjust(19),usedse.rjust(16)
#
#    if ofname:
#      print "Output is written to file",ofname
#      ofile.close()
#
#  def do_setFileStatus(self,args):
#    """Set file status for the given production
#
#    usage: setFileStatus <production> <lfn> <status>
#    """
#
#    argss = string.split(args)
#    if len(argss) != 3:
#      print "usage: setFileStatus <production> <lfn> <status>"
#      return
#
#    prod = argss[0]
#    lfn = argss[1]
#    status = argss[2]
#
#    result = self.procdb.setFileStatus(prod,lfn,status)
#    if result['Status'] != "OK":
#      print "Failed to update status for file",lfn

if __name__ == "__main__":

    import DIRAC
    cli = TransformationDBCLI()
    cli.cmdloop()
