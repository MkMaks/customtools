# -*- coding: utf-8 -*-
__context__ = 'zero-doc'
__doc__ = 'Opens settings of CustomTools'

from pyrevit import forms
from pyrevit.userconfig import user_config
from customOutput import def_hookLogs, def_revitBuildLogs, def_revitBuilds, def_massMessagePath
from customOutput import def_syncLogPath, def_openingLogPath, def_dashboardsPath, def_language


class ctSettingsWindow(forms.WPFWindow):
    def __init__(self, xaml_file_name):
        forms.WPFWindow.__init__(self, xaml_file_name)

        # creating sections in pyRevit_config.ini
        try:
            user_config.add_section('CustomToolsSettings')
        except:
            pass

        # reading parameter values from pyRevit_config.ini and setting text box values in GUI
        # if parameter does not exist create one
        # hookLogs
        try:
            self.hookLogs_tb.Text = user_config.CustomToolsSettings.hookLogs
        except:
            user_config.CustomToolsSettings.hookLogs = def_hookLogs
        # revitBuildLogs
        try:
            self.revitBuildLogs_tb.Text = user_config.CustomToolsSettings.revitBuildLogs
        except:
            user_config.CustomToolsSettings.revitBuildLogs = def_revitBuildLogs
        # revitBuilds
        try:
            self.revitBuilds_tb.Text = user_config.CustomToolsSettings.revitBuilds
        except:
            user_config.CustomToolsSettings.revitBuilds = def_revitBuilds
        # massMessagePath
        try:
            self.massMessagePath_tb.Text = user_config.CustomToolsSettings.massMessagePath
        except:
            user_config.CustomToolsSettings.massMessagePath = def_massMessagePath
        # syncLogPath
        try:
            self.syncLogPath_tb.Text = user_config.CustomToolsSettings.syncLogPath
        except:
            user_config.CustomToolsSettings.syncLogPath = def_syncLogPath
        # openingLogPath
        try:
            self.openingLogPath_tb.Text = user_config.CustomToolsSettings.openingLogPath
        except:
            user_config.CustomToolsSettings.openingLogPath = def_openingLogPath
        # dashboardsPath
        try:
            self.dashboardsPath_tb.Text = user_config.CustomToolsSettings.dashboardsPath
        except:
            user_config.CustomToolsSettings.dashboardsPath = def_dashboardsPath
        # language
        try:
            self.language_cb.SelectedItem = user_config.CustomToolsSettings.language
        except:
            user_config.CustomToolsSettings.language = str(def_language)

        user_config.save_changes()

        self.hookLogs_tb.Text = user_config.CustomToolsSettings.hookLogs
        self.revitBuildLogs_tb.Text = user_config.CustomToolsSettings.revitBuildLogs
        self.revitBuilds_tb.Text = user_config.CustomToolsSettings.revitBuilds
        self.massMessagePath_tb.Text = user_config.CustomToolsSettings.massMessagePath 
        self.syncLogPath_tb.Text = user_config.CustomToolsSettings.syncLogPath
        self.openingLogPath_tb.Text = user_config.CustomToolsSettings.openingLogPath
        self.dashboardsPath_tb.Text = user_config.CustomToolsSettings.dashboardsPath

    # saves values to config file
    def process_text(self, sender, args):
        self.Close()
        user_config.CustomToolsSettings.hookLogs = str(self.hookLogs_tb.Text)
        user_config.CustomToolsSettings.revitBuildLogs = str(self.revitBuildLogs_tb.Text)
        user_config.CustomToolsSettings.revitBuilds = str(self.revitBuilds_tb.Text)
        user_config.CustomToolsSettings.massMessagePath = str(self.massMessagePath_tb.Text)
        user_config.CustomToolsSettings.syncLogPath = str(self.syncLogPath_tb.Text)
        user_config.CustomToolsSettings.openingLogPath = str(self.openingLogPath_tb.Text)
        user_config.CustomToolsSettings.dashboardsPath = str(self.dashboardsPath_tb.Text)
        user_config.CustomToolsSettings.language = str(self.language_cb.SelectedItem)

        # print(user_config.CustomToolsSettings.hookLogs)
        # print(user_config.CustomToolsSettings.revitBuildLogs)
        # print(user_config.CustomToolsSettings.revitBuilds)
        # print(user_config.CustomToolsSettings.massMessagePath)
        # print(user_config.CustomToolsSettings.syncLogPath)
        # print(user_config.CustomToolsSettings.openingLogPath)

    # resets to default values
    def reset(self, sender, args):
        self.hookLogs_tb.Text = def_hookLogs
        self.revitBuildLogs_tb.Text = def_revitBuildLogs
        self.revitBuilds_tb.Text = def_revitBuilds
        self.massMessagePath_tb.Text = def_massMessagePath
        self.syncLogPath_tb.Text = def_syncLogPath
        self.openingLogPath_tb.Text = def_openingLogPath
        self.dashboardsPath_tb.Text = def_dashboardsPath
        self.language_cb.SelectedItem = def_language

    # functions for set buttons
    def hookLogs(self, sender, args):
        self.hookLogs_tb.Text = forms.pick_folder(title='Select folder')

    def revitBuildLogs(self, sender, args):
        self.revitBuildLogs_tb.Text = forms.save_file(file_ext='log', default_name='versions.log')
        # correct of_dlf in pyrevit forms and add title
        # self.revitBuildLogs_tb.Text = forms.save_file(file_ext='log', default_name='versions.log', title='Select log report')

    def mass_message(self, sender, args):
        self.massMessagePath_tb.Text = forms.pick_file(file_ext='html', title='Select HTML file')

    def syncLogPath(self, sender, args):
        self.syncLogPath_tb.Text = forms.pick_folder(title='Select folder')

    def openingLogPath(self, sender, args):
        self.openingLogPath_tb.Text = forms.pick_folder(title='Select folder')

    def dashboardsPath(self, sender, args):
        self.dashboardsPath_tb.Text = forms.pick_folder(title='Select folder')

ctSettingsWindow('ctSettingsWindow.xaml').ShowDialog()