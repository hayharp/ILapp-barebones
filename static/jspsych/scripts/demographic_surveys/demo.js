/* Collects demographic data for a demo experiment */

var get_age = {
    type: 'survey-html-form',
    preamble: 'Enter your age in years:',
    html: '<input type="number" name="Age" id="age-resp-box" required/><br>',
    autofocus: 'age-resp-box'
}

var get_gender_soph = {
    type: 'survey-multi-choice',
    questions: [
        {
            prompt: 'With which gender do you most identify?',
            options: ['Male', 'Female', 'Non-binary', 'Prefer not to answer'],
            required: true,
            name: 'Gender'
        },
        {
            prompt: 'Which title best describes you?',
            options: ['Non-musician', 'Music-loving non-musician', 'Amateur musician', 'Serious amateur musician', 'Semi-professional musician', 'Professional musician'],
            required: true,
            name: 'Sophistication'
        }
    ],
    on_finish: function() {
        saveData(jsPsych.data.get()
            .filter([{trial_type: 'survey-html-form'}, {trial_type: 'survey-multi-choice'}])
            .ignore('rt').ignore('trial_index').ignore('time_elapsed').ignore('internal_node_id').ignore('question_order').ignore('trial_type').json(),
            metadata, 'demo')
    }
}

var demographics = {
    timeline: [get_age, get_gender_soph]
}