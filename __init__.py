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
                'dolphin']

    @intent_handler(IntentBuilder("").require("Close"))
    def handle_hello_world_intent(self, message):
        program = message.data.get('utterance').lower()
        success = False

        for p in program.split():
            if p in self.program_list:
                if p == 'console':
                    p = 'konsole'
                elif p == 'folders':
                    p = 'dolphin'
                elif p == 'signal':
                    p = 'signal-desktop'

                subprocess.Popen(['pkill', p])  
                # Only works one time?
                # with daemon.DaemonContext():  
                    # This process now survives mycroft termination
                    # subprocess.Popen(p)  
                self.speak_dialog('Done!')
                success = True

        if not success:
            self.speak_dialog(f'Whats {program.split()[-1]}?')
        return True

    @intent_handler(IntentBuilder("").require("Open"))
    def handle_hello_world_intent(self, message):
        program = message.data.get('utterance').lower()
        success = False

        for p in program.split():
            if p in self.program_list:
                if p == 'console':
                    p = ['konsole','-e', 'tmux']
                elif p == 'folders':
                    p = 'dolphin'
                elif p == 'signal':
                    p = 'signal-desktop'

                subprocess.Popen(p)  
                # Only works one time?
                # with daemon.DaemonContext():  
                    # This process now survives mycroft termination
                    # subprocess.Popen(p)  
                self.speak_dialog('Done!')
                success = True

        if not success:
            self.speak_dialog(f'Whats {program.split()[-1]}?')
        return True

    def stop(self):
       return False


def create_skill():
    return TestSkill()
