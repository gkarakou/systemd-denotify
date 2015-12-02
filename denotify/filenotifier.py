#!/usr/bin/python2
import pyinotify
from .ConfigReader import ConfigReader
from .EventHandler import EventHandler

class FileNotifier():
    def __init__(self):
        c_read = ConfigReader()
        dictio = c_read.get_notification_entries()
        mappings = {"WRITE":8, "MODIFY":2, "DELETE":512, "ATTRIBUTE":4}
        mask = []
        for k, v in enumerate(dictio['conf_files_events']):
            for key, value in mappings.iteritems():
                if v == key:
                    mask.append(value)
        mask_ = 0
        for v in mask:
            mask_ |= v
        wm = pyinotify.WatchManager()
        notifier = pyinotify.ThreadedNotifier(wm, EventHandler())
        notifier.start()
        # Start watching  paths
        for d in dictio['conf_files_directories']:
            wm.add_watch(d, mask_, rec=True)

