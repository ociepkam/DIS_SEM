from sources.trial import Trial


def create_experiment_trials(config, win, word_bank, trials_info):
    trials = []
    for trial in trials_info:
        t = Trial()
        t.prepare_info(word_bank=word_bank, n_answers=trial["N_ANSWERS"], task_length=trial["TASK_LENGTH"],
                       trial_with_distractor=trial["DISTRACTOR"], distractor_length=trial["DISTRACTOR_LENGTH"],
                       task_category=trial["TASK_CATEGORY"], target_category=trial["TARGET_CATEGORY"])
        print(t.info)
        t.prepare_visualisation(config, win)
        trials.append(t)
    return trials


def create_training_trials(config, win, trials_description):
    trials = []
    for _, trial in trials_description.items():
        t = Trial()
        t.info = trial
        t.prepare_visualisation(config, win)
        trials.append(t)
    return trials
