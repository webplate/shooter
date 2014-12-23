#!/usr/bin/env python
# -*- coding: utf-8 -*-
import main
import cProfile

if __name__ == "__main__":
    app = main.Shooter()
    cProfile.run('app.on_execute()', sort='cumulative')

#Memory profiling if in main update
#~ if self.now > 60000:
    #~ from guppy import hpy
    #~ h = hpy()
    #~ print h.heap()
    #~ self.running = False
