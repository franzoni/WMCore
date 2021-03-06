#!/usr/bin/env python
"""
_Request.FindByPrepID_

API for finding a new request by Prep ID
"""

from WMCore.Database.DBFormatter import DBFormatter

class FindByPrepID(DBFormatter):
    def execute(self, prepID, conn = None, trans = False):
        """ returns a list of RequestIDs"""
        self.sql = """
         SELECT req.request_id from reqmgr_request req
           WHERE req.prep_id = :prepid"""

        result = self.dbi.processData(self.sql, binds = {"prepid": prepID},
                                      conn = conn, transaction = trans)
        output = [x[0] for x in self.format(result)]
        return output
