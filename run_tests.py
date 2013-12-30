#!/usr/bin/python2.7


import logging
import nose
import nose.plugins.logcapture


# stuff to disable builtin logcapture
nose.plugins.logcapture.LogCapture.orig_options = \
        nose.plugins.logcapture.LogCapture.options
nose.plugins.logcapture.LogCapture.enabled = False
delattr(nose.plugins.logcapture.LogCapture, 'options')


class LogCapture(nose.plugins.logcapture.LogCapture):
    name = 'logcapture-enhanced'
    enabled = True

    def options(self, parser, env):
        return self.orig_options(parser, env)

    def set_log_format(self, format):
        fmt = logging.Formatter(format, self.logdatefmt)
        self.handler.setFormatter(fmt)

    def beforeTest(self, test):
        if hasattr(test.test, 'log_format'):
            self.set_log_format(test.test.log_format)
        else:
            self.set_log_format(self.logformat)
        super(LogCapture, self).beforeTest(test)


nose.main(addplugins=[LogCapture()])


