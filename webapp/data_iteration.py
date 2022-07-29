'''Handles data iteration for iterative learning experiments'''

import json
import math
import os
import random

UPPERCASE_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def get_dataset(gen, participant, data_path, gen_size, method='absplit', splits=None):
    '''Gets the proper dataset given generation and current participant number'''

    if method == 'absplit':
        #This method splits each generation into an a and b group, which allows a half-gen-size window for participants
        #This avoids an instance where several participants have to wait on the last participant of the previous generation
        if participant > gen_size / 2:
            with open(f'results/{data_path}/Gen {gen-1}B.json') as f:
                dataset = json.load(f)
        else:
            with open(f'results/{data_path}/Gen {gen-1}A.json') as f:
                dataset = json.load(f)

    if method == 'split':
        #Similar to absplit, this method splits each generation into an arbitrary number of buckets. Should eventually replace absplit
        letter_list = UPPERCASE_LETTERS[0:splits]
        split_letter = letter_list[math.floor((participant-1)/gen_size*splits)]
        with open(f'results/{data_path}/Gen {gen-1}{split_letter}.json') as f:
            dataset = json.load(f)

    if method == 'one-to-one':
        #This method has participants using data from their actual participant number predecessor, like in a true game of telephone
        with open(f'results/{data_path}/Gen {gen-1}, Participant {participant}.json') as f:
            dataset = json.load(f)

    return dataset

def post_save(dataset, result_folder, sensitive=False):
    '''Saves from POST request data'''
    demo = ''
    if sensitive:
        if sensitive == 'demo':
            demo = ' Demographics'
        sensitive = '/.sensitive'
    if not sensitive:
        sensitive = ''
    result_path = (f'results{sensitive}/{result_folder}')
    path_exists = os.path.exists(result_path)
    if not path_exists:
        os.makedirs(result_path)
    with open(f"{result_path}/Gen {dataset[0]['Gen']}, Participant {dataset[0]['Participant']}{demo}.json", 'x') as f:
        f.write(json.dumps(dataset))

def no_iter_post_save(dataset, result_folder, sensitive=False):
    '''Saves from POST request data for non-iterative experiments'''
    demo = ''
    if sensitive:
        if sensitive == 'demo':
            demo = ' Demographics'
        sensitive = '/.sensitive'
    if not sensitive:
        sensitive = ''
    result_path = f'results{sensitive}/{result_folder}'
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    with open(f"{result_path}/Participant {dataset[0]['ID']}{demo}.json", 'x') as f:
        f.write(json.dumps(dataset))

def feature_reoder(dataset, feature, repetitions, participants, add_range):
    '''Reorders a stimulus dataset by allowing a feature only a certain number of repetitions'''
    unordered = []
    for x in range(participants):
        unordered.append([])
    feature_vals = []
    for participant in range(participants):
        for trial in dataset[f'Participant {participant+add_range}']:
            if dataset[f'Participant {participant+add_range}'][trial][feature] not in feature_vals:
                feature_vals.append(dataset[f'Participant {participant+add_range}'][trial][feature])
    #Assemble all trials into a list
    all_trials = []
    for participant in range(participants):
        for trial in dataset[f'Participant {participant+add_range}']:
            all_trials.append(dataset[f'Participant {participant+add_range}'][trial])
    #Begin to order
    for participant in range(participants):
        for val in feature_vals:
            repeats = 0
            for trial in all_trials:
                if trial[feature] == val and repeats < repetitions:
                    unordered[participant].append(trial)
                    all_trials.remove(trial)
                    repeats += 1
    reordered = {}
    for participant in range(participants):
        reordered[f'Participant {participant+add_range}'] = {}
        for trial in unordered[participant]:
            trial_name = f'trial_{unordered[participant].index(trial)+1}'
            reordered[f'Participant {participant+add_range}'][trial_name] = trial
    return reordered

def gen_data(experiment, gen, split, splits, gen_size, features, feature_types=None, feature_reorder_params=None):
    '''Creates the stimulus dataset for general iterative experiments. Split should be an index value!'''
    log_notes = []
    #Does appropriate split things
    letter_list = UPPERCASE_LETTERS[0:splits]
    split_letter = letter_list[split]
    participant_range = range(math.floor(gen_size/splits))
    add_range = 1 + math.ceil(gen_size/splits) * split
    #Concatenate result files for given split. Uses most recent generation for any given participant
    in_dataset = {}
    for x in participant_range:
        seeking_gen = 1
        while seeking_gen:
            try:
                with open(f'results/{experiment}/Gen {gen-seeking_gen}, Participant {x+add_range}.json') as f:
                    data = json.loads(f.read())
                    for element in data:
                        if not feature_types:
                            try: #In instance of initial data
                                trial_name = [key for key in element.keys() if 'trial' in key][0]
                                if trial_name not in in_dataset:
                                    in_dataset[trial_name] = {}
                                for y in features:
                                    try:
                                        in_dataset[trial_name][y].append(element[trial_name][y])
                                    except KeyError:
                                        in_dataset[trial_name][y] = []
                                        in_dataset[trial_name][y].append(element[trial_name][y])
                            except (KeyError, IndexError): #In instance of user-generated data
                                if 'Participant' in element.keys(): #Check if this element is the metadata
                                    pass
                                else:
                                    trial_name = f'trial_{data.index(element)}'
                                    if trial_name not in in_dataset:
                                        in_dataset[trial_name] = {}
                                    for y in features:
                                        try:
                                            in_dataset[trial_name][y].append(element[y])
                                        except KeyError:
                                            in_dataset[trial_name][y] = []
                                            in_dataset[trial_name][y].append(element[y])
                if seeking_gen > 1:
                    log_notes.append(f'WARNING: Data for Participant {x+add_range}, Gen {gen-1} not found. Using Gen {gen-seeking_gen} for {gen-1}{split_letter} split.')
                seeking_gen = False
            except FileNotFoundError:
                seeking_gen += 1
                assert(gen - seeking_gen > -1),'Could not find any appropriate stimuli file. Are Gen 0 files missing?'
    dataset = {}
    for x in participant_range:
        dataset[f'Participant {x+add_range}'] = {}
        for trial in in_dataset:
            dataset[f'Participant {x+add_range}'][trial] = {}
    for trial in in_dataset:
        index_spots = [*range(0, (len(in_dataset['trial_1'][features[0]])))]
        random.shuffle(index_spots)
        for index_spot in index_spots:
            for feature in features:
                dataset[f'Participant {index_spots.index(index_spot)+add_range}'][trial][feature] = in_dataset[trial][feature][index_spot]
    if feature_reorder_params:
        dataset = feature_reoder(dataset, feature_reorder_params[0], feature_reorder_params[1], math.floor(gen_size/2), add_range)
    with open(f'results/{experiment}/Gen {gen-1}{split_letter}.json', 'w') as f:
        f.write(json.dumps(dataset))
    log_notes.append(f'INFO: Generated {gen-1}{split_letter} split.')
    return log_notes
