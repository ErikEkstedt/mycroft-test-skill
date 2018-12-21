from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

import os
from os.path import join
from subprocess import Popen
import subprocess
import daemon


class TestSkill(MycroftSkill):
    def __init__(self):
        super(TestSkill, self).__init__(name="TestSkill")
        self.dialog = []
        self.program_list = [
                'console',
                'firefox',
                'browser',
                'spotify',
                'signal',
                'discover',
                'slack',
                'status',
                'dolphin',
                'folders']

    @intent_handler(IntentBuilder("").require("close"))
    def close_programs(self, message):
        program = message.data.get('utterance').lower()
        success = False

        for p in program.split():
            if p in self.program_list:
                p = self.check_correct_process_name(p)

                subprocess.Popen(['pkill', p])  
                # Only works one time?
                # with daemon.DaemonContext():  
                    # This process now survives mycroft termination
                    # subprocess.Popen(p)  
                self.speak_dialog('Done!')
                success = True

        if not success:
            self.speak_dialog(f'Whats {program.split()[-1]}?')

    @intent_handler(IntentBuilder("").require("Open"))
    def open_programs(self, message):
        program = message.data.get('utterance').lower()
        success = False

        for p in program.split():
            if p in self.program_list:
                p = self.check_correct_process_name(p)
                subprocess.Popen(p)  
                # Only works one time?
                # with daemon.DaemonContext():  
                    # This process now survives mycroft termination
                    # subprocess.Popen(p)  
                self.speak_dialog('Done!')
                success = True

        if not success:
            self.speak_dialog(f'Whats {program.split()[-1]}?')

    def check_correct_process_name(self, p):
        if p == 'console':
            p = 'konsole'
        elif p == 'discover':
            p = 'plasma-discover'
        elif p == 'folders':
            p = 'dolphin'
        elif p == 'signal':
            p = 'signal-desktop'
        elif p == 'status':
            p = ['konsole', '-e',  'htop']
        return p

    def stop(self):
       return False


def create_skill():
    return TestSkill()
