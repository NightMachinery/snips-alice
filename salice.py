#!/usr/bin/env python3
from hermes_python.hermes import Hermes, MqttOptions
from plumbum import local
from plumbum.cmd import echo, socat

# local.env.path.insert(0, local.env.home + '/scripts/zsh/wrappers')
# lq = local['lq.zsh']

def mmHandler(hermes, intent_message):
    v = intent_message.slots.arbit.first().value
    hermes.publish_end_session(intent_message.session_id, "")


def lqHandler(hermes, intent_message):
    (echo['Starting over (triggered via snips);'] | socat['-u', '-', 'unix-connect:' + local.env.home + '/tmp/.luna'])()
    hermes.publish_end_session(intent_message.session_id, "Luna restarted successfully.")

with Hermes(mqtt_options=MqttOptions()) as h:
    h\
        .subscribe_intent("NightMachinary:MagicMirror", mmHandler)\
        .subscribe_intent("NightMachinary:LunaQuit", lqHandler)\
        .start()
