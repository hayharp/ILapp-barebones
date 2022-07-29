'''Script to pick random initial stimuli'''

import json

def midi_to_rhythm_array(tjs_conversion):
    '''Converts a json-formatted midi file to a midi-play-/midi-variable-slider- friendly format'''
    with open(tjs_conversion, 'r') as f:
        tjs_conversion = json.load(f)
    rhythms = []
    for x in range(len(tjs_conversion['tracks'][0]['notes'])):
        try:
            rhythms.append([round(tjs_conversion['tracks'][0]['notes'][x]['time'], 3), tjs_conversion['tracks'][0]['notes'][x]['name']])
        except IndexError:
            print(x)
    try:
        return rhythms, tjs_conversion['header']['tempos'][0]['bpm']
    except KeyError:
        return rhythms, tjs_conversion['header']['tempo'][0]['bpm']