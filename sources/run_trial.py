from psychopy import event, visual
import time
import random
from sources.check_exit import check_exit
from sources.show_info import read_text_from_file
from os.path import join


def run_trial(trial, config, response_clock, clock_image, mouse, win, fixation,
              instruction=None, training=False, training_trial_idx=None):
    win.callOnFlip(response_clock.reset)
    win.flip()
    while response_clock.getTime() < config["FIXATION_TIME"]:
        fixation.draw(win)
        win.flip()

    acc = -1
    chosen_answer = {"word": None, "length": None, "category": None}
    rt = None
    trial.set_auto_draw(True)
    if instruction is not None:
        instruction.setAutoDraw(True)
    clock_is_shown = False
    win.callOnFlip(response_clock.reset)
    win.flip()
    event.clearEvents()

    while response_clock.getTime() < config["STIM_TIME"] and acc == -1:
        for idx, frame in enumerate(trial.frames):
            if mouse.isPressedIn(frame):
                chosen_answer = trial.info["answers"][idx]
                acc = chosen_answer == trial.info["target"]
                rt = response_clock.getTime()
                break

        if not clock_is_shown and config["STIM_TIME"] - response_clock.getTime() < config["SHOW_CLOCK"]:
            clock_image.setAutoDraw(True)
            clock_is_shown = True
            win.flip()

        check_exit()
        win.flip()
    clock_image.setAutoDraw(False)
    if training:
        feedback_file_name = "feedback_positive.txt" if acc == 1 else "feedback_negative.txt"
        text = read_text_from_file(join('.', 'messages', feedback_file_name)) + \
                   read_text_from_file(join('.', 'messages', "feedback_info_0{}.txt".format(training_trial_idx+1)))

        feedback = visual.TextStim(win=win, height=config['FEEDBACK_SIZE'], alignHoriz='center', alignVert='center',
                                   font=u'Arial', pos=config["FEEDBACK_POS"], text=text, wrapWidth=win.size[0],
                                   color=config["FEEDBACK_COLOR"])
        feedback.setAutoDraw(True)
        win.flip()
        event.waitKeys(keyList=['space'])
        feedback.setAutoDraw(False)

    trial.set_auto_draw(False)
    if instruction is not None:
        instruction.setAutoDraw(False)
    win.flip()
    time.sleep(config["WAIT_TIME"] + random.uniform(config["WAIT_JITTER"][0], config["WAIT_JITTER"][1]))

    return chosen_answer, acc, rt
