import datetime
import os
import xbmc
import xbmcgui
import source as src

from strings import *


class Notification(object):
    def __init__(self, database, addonPath):
        """
        @param database: source.Database
        """
        self.database = database
        self.addonPath = addonPath
        self.icon = os.path.join(self.addonPath, 'icon.png')

    def createAlarmClockName(self, programTitle, startTime):
        return 'tvguide-%s-%s' % (programTitle, startTime)

    def scheduleNotifications(self):
        xbmc.log("[script.tvguide] Scheduling notifications")
        for channelTitle, programTitle, startTime in self.database.getNotifications():
            self._scheduleNotification(channelTitle, programTitle, startTime)

    def _scheduleNotification(self, channelTitle, programTitle, startTime):
        t = startTime - datetime.datetime.now()
        timeToNotification = ((t.days * 86400) + t.seconds) / 60
        if timeToNotification < 0:
            return

        name = self.createAlarmClockName(programTitle, startTime)

        description = strings(NOTIFICATION_5_MINS, channelTitle)
        xbmc.executebuiltin('AlarmClock(%s-5mins,Notification(%s,%s,10000,%s),%d,True)' %
            (name.encode('utf-8', 'replace'), programTitle.encode('utf-8', 'replace'), description.encode('utf-8', 'replace'), self.icon, timeToNotification - 5))

        description = strings(NOTIFICATION_NOW, channelTitle)
        xbmc.executebuiltin('AlarmClock(%s-now,Notification(%s,%s,10000,%s),%d,True)' %
                            (name.encode('utf-8', 'replace'), programTitle.encode('utf-8', 'replace'), description.encode('utf-8', 'replace'), self.icon, timeToNotification))

    def _unscheduleNotification(self, programTitle, startTime):
        name = self.createAlarmClockName(programTitle, startTime)
        xbmc.executebuiltin('CancelAlarm(%s-5mins,True)' % name.encode('utf-8', 'replace'))
        xbmc.executebuiltin('CancelAlarm(%s-now,True)' % name.encode('utf-8', 'replace'))

    def addNotification(self, program):
        self.database.addNotification(program)
        self._scheduleNotification(program.channel.title, program.title, program.startDate)

    def removeNotification(self, program):
        self.database.removeNotification(program)
        self._unscheduleNotification(program.title, program.startDate)


if __name__ == '__main__':
    database = src.Database()

    def onNotificationsCleared():
        xbmcgui.Dialog().ok(strings(CLEAR_NOTIFICATIONS), strings(DONE))

    def onInitialized(success):
        if success:
            database.clearAllNotifications()
            database.close(onNotificationsCleared)
        else:
            database.close()

    database.initialize(onInitialized)
