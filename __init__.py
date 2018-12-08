from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

import os

class TestSkill(MycroftSkill):

    def __init__(self):
        super(TestSkill, self).__init__(name="TestSkill")
        self.dialog = []
        self.program_list = ['konsole',  'firefox', 'spotify']

    @intent_handler(IntentBuilder("").require("Testing"))
    def handle_hello_world_intent(self, message):
        utterance = message.data.get('utterance')
        self.dialog.append(utterance)

        for d in self.dialog:
            self.speak_dialog(d)

    @intent_handler(IntentBuilder("").require("Open"))
    def handle_hello_world_intent(self, message):
        program = message.data.get('utterance').lower()

        for p in program.split():
            if p == 'console':
                p = 'konsole' 
            if p in self.program_list:
                self.speak_dialog('Opening ' + p)
                os.system(p + ' &')

    def stop(self):
       return False


def create_skill():
    return TestSkill()
