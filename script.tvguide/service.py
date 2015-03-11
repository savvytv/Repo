import xbmcaddon
import notification
import xbmc
import source


class Service(object):
    def __init__(self):
        self.database = source.Database()
        self.database.initialize(self.onInit)

    def onInit(self, success):
        if success:
            self.database.updateChannelAndProgramListCaches(self.onCachesUpdated)
        else:
            self.database.close()

    def onCachesUpdated(self):

        if ADDON.getSetting('notifications.enabled') == 'true':
            n = notification.Notification(self.database, ADDON.getAddonInfo('path'))
            n.scheduleNotifications()

        self.database.close(None)

try:
    ADDON = xbmcaddon.Addon(id = 'script.tvguide')
    if ADDON.getSetting('cache.data.on.xbmc.startup') == 'true':
        Service()
    if ADDON.getSetting('autostart') == "true":
        xbmc.executebuiltin("RunAddon(script.tvguide)")
except source.SourceNotConfiguredException:
    pass  # ignore
except Exception, ex:
    xbmc.log('[script.tvguide] Uncaugt exception in service.py: %s' % str(ex) , xbmc.LOGDEBUG)
