/* Demo iterative learning jsPsych experiment for ILapp-barebones */

// Get stim data and metadata
var initial_data
var trial_list

// Function to shuffle arrays
function shuffle(array) {
  for (let x = array.length - 1; x > 0; x--) {
    const y = Math.floor(Math.random() * (x + 1));
    [array[x], array[y]] = [array[y], array[x]]
  }
}

// Get initial stimuli for each trial
var get_stims = {
    type: 'html-button-response',
    stimulus: '<p>Press "Begin" when you are ready for the next audio sequence.</p>',
    choices: ['Begin'],
    on_start: function() {
        trial = trial_list.pop();
        STIMULUS_INDEX = 0
        var midi = initial_data[trial]['midi'].slice()
        var target_tempo = initial_data[trial]['target_tempo']
        // run_sequence is a per-trial variable that carries the relevant trial stimulus and metadata
        run_sequence = {midi: midi, trial_num: trial, ref_tempo: initial_data[trial]['ref_tempo'], target_tempo: target_tempo, stim_type: initial_data[trial]['stim_type'], stim_name: initial_data[trial]['stim_name'], iteration_tag: initial_data[trial]['iteration_tag']}
    }
}

var stim = {
    type: 'midi-play',
    stimulus: function() {return run_sequence.midi},
    iterations: 1,
    message: 'Remember the tempo of this clip',
    ref_tempo: function() {return run_sequence.ref_tempo},
    tempo: function() {return run_sequence.target_tempo}
};

var welcome = {
    type: 'html-button-response',
    on_start: function() {
        initial_data = JSON.parse(metadata)['Stims'][`Participant ${JSON.parse(metadata)['Participant']}`]
        trial_list = []
        for (let x = Object.keys(initial_data).length; x > 0; x--) {
            trial_list.push(`trial_${x}`)
        }
        shuffle(trial_list)
    },
    stimulus: '<p>In this experiment, you will hear various rhythms at different tempos (speeds).</p>' +
              '<p>Each rhythm will repeat four times. Remember how fast or slow the rhythm goes.</p>' +
              '<p>After a brief pause, you will hear the same rhythm again, but now at a different tempo.</p>' +
              '<p>Adjust the speed of the rhythm using the slider until it matches the original tempo.</p>' +
              '<p>Once you are confident with your decision, you will proceed to the next rhythm.</p>',
    choices: ['Continue']
};

/* Task section */
var test = {
    type: 'midi-variable-slider',
    stimulus: function() {return run_sequence.midi},
    message: '<p>Adjust the tempo of the clip until it matches the original.</p>' +
             '<p>Click "Submit" when you feel confident with your selection.</p>',
    transport_variable: 'bpm',
    tv_target: function() {return run_sequence.target_tempo},
    slider_range_upper: 250,
    slider_range_lower: 40,
    ref_tempo: function() {return run_sequence.ref_tempo},
    // Allowed percentage of error
    outlier_boundary: .50,
    iteration_tag: function() {return run_sequence.iteration_tag},
    on_finish: function(data) {
        data['target_tempo'] = Math.round(data['slider_value'])
        data['stim_name'] = run_sequence.stim_name
        data['ref_tempo'] = run_sequence.ref_tempo
        data['iter_type'] = 'rhythm'
        data['presentation_tempo'] = run_sequence.target_tempo
    }
};

/* Full test loop */
var full_loop_node = {
    timeline: [get_stims, stim, test],
    loop_function: function(data) {
        if (typeof trial_list[0] !== 'undefined') {
            return true;
        } else {
            return false;
        }
    }
}

/* Finish message */
var finish_message = {
    type: 'html-button-response',
    on_start: function() {
        var parsed_metadata = JSON.parse(metadata)
        parsed_metadata = JSON.stringify(parsed_metadata)
        saveData(jsPsych.data.get()
                 .filter([{ trial_type: 'midi-variable-slider'}]).filter([{ iter_type: 'rhythm'}])
                 .ignore('trial').ignore('trial_index').ignore('trial_type').ignore('internal_node_id').ignore('iter_type').ignore('slider_value')
                 .json(), parsed_metadata, false)
    },
    stimulus: function() {
        return '<p>The task is now complete!</p>' +
               '<p>Please press "Finish" when ready.</p>'
    },
    choices: ['Finish']
}

var demo_il = {
    timeline: [welcome, full_loop_node, finish_message]
}