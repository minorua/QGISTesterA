# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QGISTestResult
                                 A QGIS plugin
 Make testing on various platforms easy and reliable
                             -------------------
        begin                : 2014-11-12
        copyright            : (C) 2014 Minoru Akagi
        email                : akaginch@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import sys
import unittest

class QGISTestResult(unittest.TestResult):

  _html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    "\n": "<br>"
    }

  _style = """
<style>
table {border: 1px black solid; width: 100%; table-layout: fixed;}
td, th {border: 1px black solid; word-wrap: break-word;}
table th:nth-child(1) {max-width: 160px;}
table th:nth-child(2) {width: 40%;}
table th:nth-child(3) {width: 55px;}
td.info {background-color: #ffffcc;}
td.success {background-color: lightcyan;}
td.fail {background-color: pink;}
td.error {background-color: red;}
td.skip {background-color: lightgray;}
div.error {color: red;}
</style>"""  #TODO: ef, ues

  def __init__(self, stream=None, descriptions=None, verbosity=None):
    unittest.TestResult.__init__(self, stream, descriptions, verbosity)
    self.buffer = True
    self.testResults = []
    self.logs = []

  # this is not called?
  def startTestRun(self):
    unittest.TestResult.startTestRun(self)
    self.appendLog("startTestRun")

  # this is not called?
  def stopTestRun(self):
    unittest.TestResult.stopTestRun(self)
    self.appendLog("stopTestRun")

  def startTest(self, test):
    unittest.TestResult.startTest(self, test)
    self.appendLog("startTest: {}".format(str(test)))

  def stopTest(self, test):
    unittest.TestResult.stopTest(self, test)
    self.appendLog("stopTest")
    self.appendLog("\n")

  def html_escape(self, text):
    return "".join(self._html_escape_table.get(c, c) for c in text)

  def appendLog(self, innerText, error=False, escape=True):
    style = " class='error'" if error else ""
    text = self.html_escape(innerText) if escape else innerText
    self.logs.append(u"<div{}>{}</div>".format(style, text))

  def _readStdout(self):
    if not self.buffer:
      return "", ""

    output = self._stdout_buffer.getvalue()
    error = self._stderr_buffer.getvalue()
    if output:
      if not output.endswith('\n'):
        output += '\n'
      self.appendLog(output)
    if error:
      if not error.endswith('\n'):
        error += '\n'
      self.appendLog(error, error=True)

    self._stdout_buffer.seek(0)
    self._stdout_buffer.truncate()
    self._stderr_buffer.seek(0)
    self._stderr_buffer.truncate()
    return output, error

  # override
  def _restoreStdout(self):
    self._readStdout()

  def addSuccess(self, test):
    unittest.TestResult.addSuccess(self, test)
    out, err = self._readStdout()
    out = "\n".join([s for s in out.split("\n") if not s.startswith("#")])
    err = "\n".join([s for s in err.split("\n") if not s.startswith("#")])
    msg = u"<div>{}</div>".format(self.html_escape(out)) if out else ""
    if err:
      msg += "<div class='error'>{}</div>".format(self.html_escape(err))
    self.testResults.append([test, "success", msg])
    self.appendLog("Success")

  def addFailure(self, test, err):
    unittest.TestResult.addFailure(self, test, err)
    self.testResults.append([test, "fail", "\n".join([str(e) for e in err if e])])
    self._readStdout()
    self.appendLog("Failure")

  def addError(self, test, err):
    unittest.TestResult.addError(self, test, err)
    self.testResults.append([test, "error", "\n".join([str(e) for e in err if e])])
    self._readStdout()
    self.appendLog("Error")

  def addSkip(self, test, reason):
    unittest.TestResult.addSkip(self, test, reason)
    self.testResults.append([test, "skip", reason])
    self._readStdout()
    self.appendLog("Skipped")

  def addExpectedFailure(self, test, err):
    unittest.TestResult.addExpectedFailure(self, test, err)
    self.testResults.append([test, "ef", "\n".join([str(e) for e in err if e])])
    self._readStdout()
    self.appendLog("Expected Failure")

  def addUnexpectedSuccess(self, test):
    unittest.TestResult.addUnexpectedSuccess(self, test)
    self.testResults.append([test, "ues", ""])
    self._readStdout()
    self.appendLog("Unexpected Success")

  def html(self):
    doc = []
    if len(self.testResults):
      doc.append(self._style)
      doc.append("<h1>Test Results</h1>")

      last_testcase = None
      for test, result, message in self.testResults:
        #test01_Test (QGISTester.tests.test_test.UnitTestTest)
        #test01_Test (test_test.UnitTestTest)
        testname, a = str(test)[:-1].split(" (")
        a = a.split(".")
        testcase = a.pop()
        mod = a[0] if len(a) == 1 else ".".join(a[2:])

        if testcase != last_testcase:
          if last_testcase is not None:
            doc.append("</table>")
          doc.append("<h2>{0}::{1}</h2>".format(mod, testcase))
          doc.append("<table>")
          doc.append("<tr><th>Test</th><th>Description</th><th>Result</th><th>Message</th></tr>")

        desc = test.shortDescription() or ""
        if "[INFO]" in desc:
          desc = desc.replace("[INFO]", "").strip()
          result = "info"

        doc.append(u"<tr><td>{}</td><td>{}</td><td class='{}'>{}</td><td>{}</td></tr>".format(testname, desc, result, result, message))
        last_testcase = testcase
      doc.append("</table>")
      doc.append("<br><hr>")
    doc.append("<h1>Logs</h1>")
    doc += self.logs
    return "".join(doc)
