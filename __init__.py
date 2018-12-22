from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

import os
import subprocess

# TODO
# More advanced scripts
# ssh to kth: open terminal, ssh, ls

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
        self.directions = ['left', 'right', 'back', 'next']

    def check_correct_process_name(self, p):
        if p == 'console':
            p = ['konsole']
        elif p == 'discover':
            p = ['plasma-discover']
        elif p == 'folders':
            p = ['dolphin']
        elif p == 'signal':
            p = ['signal-desktop']
        elif p == 'status':
            # p = ['konsole', '-e',  'htop', 'ksysguard']
            p = [['konsole', '-e',  'htop'], ['ksysguard']]
        return p

    @intent_handler(IntentBuilder("").require("close"))
    def close_programs(self, message):
        program = message.data.get('utterance').lower()
        success = False

        for p in program.split():
            if p in self.program_list:
                p = self.check_correct_process_name(p)

                subprocess.Popen(['pkill', p])  
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
                p_list = self.check_correct_process_name(p)
                
                for p in p_list:
                    subprocess.Popen(p)  # If mycroft dies this dies.
                self.speak_dialog('Done!')
                success = True

                # Only works one time?
                # with daemon.DaemonContext():  
                    # This process now survives mycroft termination
                    # subprocess.Popen(p)  

        if not success:
            self.speak_dialog(f'Whats {program.split()[-1]}?')

    @intent_handler(IntentBuilder("").require("Go"))
    def move_desktop(self, message):
        def command(p):
            if p in ['left', 'back', 'previous']:
                cmd = ['qdbus',  'org.kde.KWin',
                        '/KWin', 'org.kde.KWin.previousDesktop']
            elif p in ['right', 'next']:
                cmd = ['qdbus',  'org.kde.KWin', '/KWin', 'org.kde.KWin.nextDesktop']
            return cmd

        program = message.data.get('utterance').lower()
        success = False
        for p in program.split():
            if p in self.directions:
                cmd = command(p)
                subprocess.Popen(cmd)  

    @intent_handler(IntentBuilder("").require("Lock"))
    def lock_desktop(self):
        cmd = ['qdbus', 'org.kde.screensaver', '/ScreenSaver', 'Lock']
        subprocess.Popen(cmd)  

    def stop(self):
       return False


def create_skill():
    return TestSkill()
