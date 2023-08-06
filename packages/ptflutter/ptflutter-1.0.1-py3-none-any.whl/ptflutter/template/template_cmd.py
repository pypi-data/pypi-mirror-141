# coding=utf-8

from subprocess import call

from ptflutter.config.config_cmd import ConfigCommand
from ptflutter.template.template_mobx import TemplateMobX
from .template import Template
from ..utils.utils import *
from ..core.command import Command, CommandOption


class TemplateCommand(Command):
    def __init__(self, template_name, scene_name, options):
        super(TemplateCommand, self).__init__()
        self.template_name = template_name
        self.scene_name = scene_name
        self.options = CommandOption(options)

    def get_project_package_name(self):
        try:
            name = get_current_dart_package_name()
            print("Current package name: %s" % name)
            return name.strip()
        except (IOError, OSError) as e:
            logError("Please run this command in flutter folder.")
            exit(1)

    def create_files(self):
        config = ConfigCommand.getInstance()
        architecture = config.read_config("architecture.type")
        if self.template_name == Template.TemplateType.BASE:
            if architecture == "mobx":
                template = TemplateMobX.BaseTemplate(
                    self.options,
                    self.scene_name,
                    self.get_project_package_name()
                )
            elif architecture == "rx":
                template = Template.BaseTemplate(
                    self.options,
                    self.scene_name,
                    self.get_project_package_name()
                )
            output_path = template.create_files()
            # Reload disk
            logAndCommand("ide.action.synchronize")
        else:
            logError("Invalid template type.")
            exit(1)
