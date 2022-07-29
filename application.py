'''App to be deployed to EB'''

import logging

from flask import Flask, request, render_template

from webapp import data_iteration

application = app = Flask(__name__)

logger = logging.getLogger('werkzeug')
handler = logging.FileHandler('flask.log')
logger.addHandler(handler)

def write_ap(experiment, gen, participant):
    '''Writes active participant directly to its respective file'''
    with open(f'results/{experiment}/active_participant', 'w') as f:
        f.write(f'{str(gen)}\n')
        f.write(str(participant))

def get_ap(experiment):
    '''Gets active participant directly from its respective file'''
    with open(f'results/{experiment}/active_participant') as f:
        gen = int(f.readline())
        participant = int(f.readline())
    return gen, participant

@app.route('/')
def mainpage():
    '''Simplest page option. When "/" receives a GET, it calls mainpage()'''
    return 'Welcome to our experiment backend!'

@app.route('/favicon.ico')
def favicon():
    '''Redirects to favicon'''
    return app.send_static_file('favicon.ico')

@app.errorhandler(404)
def page_not_found(error):
    '''Redirects to a slightly nicer 404 page'''
    logger.error(error)
    return render_template('404.html', title='Page not found'), 404

@app.route('/demo', methods=['GET', 'POST'])
def demo_experiment():
    '''Demo iterative learning experiment'''

    active_gen, active_participant = get_ap('demo')
    gen_size = 4 #Allows for at least 3 concurrent users
    splits = 2

    if request.method == 'POST':
        #Block for data collection; triggers upon experiment completion
        data_iteration.post_save(request.json, 'demo', request.json[0]['Sensitive'])

    active_participant += 1
    #Block for Split B
    if (active_participant-1)/gen_size*splits == 1:
        logger.info(data_iteration.gen_data('demo', active_gen, 1, splits, gen_size,
                                            ['target_tempo', 'midi', 'stim_name', 'ref_tempo', 'iteration_tag'], feature_reorder_params=['stim_name', 1]))
    #Block for Split A
    if active_participant > gen_size:
        active_participant = 1
        active_gen += 1
        logger.info(data_iteration.gen_data('demo', active_gen, 0, splits, gen_size,
                                            ['target_tempo', 'midi', 'stim_name', 'ref_tempo', 'iteration_tag'], feature_reorder_params=['stim_name', 1]))
    write_ap('demo', active_gen, active_participant)
    dataset = {}
    dataset['Participant'] = active_participant
    dataset['Gen'] = active_gen
    dataset['URL'] = '/demo'
    dataset['Stims'] = data_iteration.get_dataset(active_gen, active_participant, 'demo', gen_size, method='split', splits=2)
    return render_template('demo_experiment.html', data=dataset)
