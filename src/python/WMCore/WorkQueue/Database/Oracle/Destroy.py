#/usr/bin/env python2.4
"""
_Destroy_

"""

__revision__ = "$Id: Destroy.py,v 1.1 2009/06/05 17:04:32 sryu Exp $"
__version__ = "$Revision: 1.1 $"

from WMCore.WorkQueue.Database.DestroyWorkQueueBase import DestroyWorkQueueBase
from WMCore.WorkQueue.Database.Oracle.Create import Create

class Destroy(DestroyWorkQueueBase):    
    def __init__(self, logger = None, dbi = None):
        """
        _init_

        Call the base class's constructor and add all necessary tables for 
        deletion,
        """
        print "----"        
        DestroyWorkQueueBase.__init__(self, logger, dbi)
    
        for i in Create.sequenceTables:
            seqname = '%s_SEQ' % i
            self.create["%s%s" % (Create.seqStartNum, seqname)] = \
                           "DROP SEQUENCE %s"  % seqname 