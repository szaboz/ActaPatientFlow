from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from SpiffWorkflow.camunda.parser.CamundaParser import CamundaParser
from SpiffWorkflow.camunda.specs.UserTask import EnumFormField, UserTask

import threading, os, random, time, simulation, playbook, csv, json

def show_form(task):
    form = task.task_spec.form
    if task.data is None:
        task.data = {}
    for field in form.fields:
        prompt = field.label
        if isinstance(field, EnumFormField):
            prompt += "? (Options: " + ', '.join([str(option.id) for option in field.options]) + ")"
        prompt += "? "
        answer = input(prompt)
        if field.type == "long":
            answer = int(answer)
        task.update_data_var(field.id, answer)

parser = CamundaParser()
parser.add_bpmn_file('EDAsIs.bpmn')
parser.add_bpmn_file('Visit.bpmn')
spec = parser.get_spec('EDAsIs')

threads = []
max_patients = 90
timecount = 0
sim_timecount = 0

def start_new_workflow():
    print('Starting')
    workflow = BpmnWorkflow(spec)

    workflow.do_engine_steps()
    ready_tasks = workflow.get_ready_user_tasks()
    while len(ready_tasks) > 0:
        for task in ready_tasks:
            if isinstance(task.task_spec, UserTask):
                show_form(task)
                print(task.data)
            else:
                print("Complete Task ", task.task_spec.name)
            workflow.complete_task_from_id(task.id)
        workflow.do_engine_steps()
        ready_tasks = workflow.get_ready_user_tasks()

class StarterThread(threading.Thread):
    def run(self):
        global threads, max_patients, timecount
        while len(threads) < max_patients:
            timecount += 1
            a = random.uniform(0, 1)
            if a <= 0.2:
                t = threading.Thread(target = start_new_workflow, args=[])
                t.start()
                threads.append(t)
            time.sleep(1)
        print('all patients are in the simulation now')

class SimulationThread(threading.Thread):
    def run(self):
        global threads, max_patients, timecount, sim_timecount
        while True:
            sim_timecount += 1
            stoppable = True
            if len(threads) == max_patients:
                for i in range(len(threads)):
                    if threads[i].is_alive():
                        stoppable = False
            else:
                stoppable = False
            if stoppable:
                print('finished')
                times = time.time()
                keys = ['name', 'age', 'arrival', 'triage', 'result', 'registration_waiting',
                'register_patient_time', 'registration_full', 'evaluate_urgency_waiting', 'evaluate_urgency_time',
                'evaluate_urgency_full', 'urgency', 'abandons', 'provide_pre_visit_waiting', 'provide_pre_visit_time',
                'provide_pre_visit_full', 'assign_esi_waiting', 'iclinic_transfer_waiting',
                'outcomes', 'collect_history_waiting', 'collect_history_time', 'collect_history_full',
                'hyp_diag_waiting', 'hyp_diag_time', 'hyp_diag_full', 'exams', 'images',
                'take_blood_waiting', 'take_blood_time', 'take_blood_full', 
                'lab_waiting', 'lab_time', 'lab_full', 'transfer_to_rad_waiting',
                'transfer_to_rad_time', 'transfer_to_rad_full', 'radiology_waiting',
                'radiology_time', 'radiology_full', 'et_diag_waiting', 'et_diag_time',
                'et_diag_full', 'diagnosis', 'def_therapy_waiting', 'def_therapy_time', 'def_therapy_full',
                'manage_outcome_waiting', 'manage_outcome_time', 'manage_outcome_full',
                'search_efacility_waiting', 'search_efacility_time',
                'wa_hosp_waiting', 'wa_hosp_time', 'wa_hosp_full',
                'transfer_to_ef_waiting', 'transfer_to_ef_time', 'transfer_to_ef_full',
                'morgue_transfer_waiting', 'morgue_transfer_time', 'morgue_transfer_full']
                with open('results_' + str(times) + '.csv', 'w', newline='') as output_file:
                    dict_writer = csv.DictWriter(output_file, keys, delimiter=';', extrasaction='ignore')
                    dict_writer.writeheader()
                    dict_writer.writerows(playbook.logbook)
                logs = [{'register_max_patients': simulation.register_max_patients, 
                'register_longest_time': simulation.register_longest_time,
                'register_longest_full': simulation.register_longest_full,
                'evaluate_max_patients': simulation.evaluate_max_patients, 
                'evaluate_longest_time': simulation.evaluate_longest_time, 
                'evaluate_longest_full': simulation.evaluate_longest_full,
                'previsit_max_patients': simulation.previsit_max_patients, 
                'previsit_longest_time': simulation.previsit_longest_time, 
                'previsit_longest_full': simulation.previsit_longest_full,
                'chistory_max_patients': simulation.chistory_max_patients, 
                'chistory_longest_time': simulation.chistory_longest_time, 
                'chistory_longest_full': simulation.chistory_longest_full,
                'hypthosize_max_patients': simulation.hypthosize_max_patients, 
                'hypthosize_longest_time': simulation.hypthosize_longest_time, 
                'hypthosize_longest_full': simulation.hypthosize_longest_full,
                'bloodsample_max_patients': simulation.bloodsample_max_patients, 
                'bloodsample_longest_time': simulation.bloodsample_longest_time, 
                'bloodsample_longest_full': simulation.bloodsample_longest_full,
                'laboratory_max_patient': simulation.laboratory_max_patients, 
                'laboratory_longest_time': simulation.laboratory_longest_time, 
                'laboratory_longest_full': simulation.laboratory_longest_full,
                'rtransfer_max_patients': simulation.rtransfer_max_patients, 
                'rtransfer_longest_time': simulation.rtransfer_longest_time, 
                'rtransfer_longest_full': simulation.rtransfer_longest_full,
                'radiology_max_patients': simulation.radiology_max_patients, 
                'radiology_longest_time': simulation.radiology_longest_time, 
                'radiology_longest_full': simulation.radiology_longest_full,
                'estabd_max_patients': simulation.estabd_max_patients, 
                'estabd_longest_time': simulation.estabd_longest_time, 
                'estabd_longest_full': simulation.estabd_longest_full,
                'dtherap_max_patients': simulation.dtherap_max_patients, 
                'dtherap_longest_time': simulation.dtherap_longest_time, 
                'dtherap_longest_full': simulation.dtherap_longest_full,
                'moutcome_max_patients': simulation.moutcome_max_patients, 
                'moutcome_longest_time': simulation.moutcome_longest_time, 
                'moutcome_longest_full': simulation.moutcome_longest_full}]
                skeys = logs[0].keys()
                with open('results_states_' + str(times) + '.csv', 'w', newline='') as output_file:
                    dict_writer = csv.DictWriter(output_file, skeys, delimiter=';', extrasaction='ignore')
                    dict_writer.writeheader()
                    dict_writer.writerows(logs)
                print('Full time needed for all patients to arrive: ' + str(timecount))
                print('Full time for simulation to end: ' + str(sim_timecount))
                
                trange = list(range(0, len(simulation.register_trend)))
                time_dataframe = {
                    'time': trange,
                    'register_patients': simulation.register_trend, 
                    'evaluate_patients': simulation.evaluate_trend,
                    'previsit_patients': simulation.previsit_trend,
                    'chistory_patients': simulation.chistory_trend,
                    'hypthosize_patients': simulation.hypthosize_trend,
                    'bloodsample_patients': simulation.bloodsample_trend,
                    'laboratory_patients': simulation.laboratory_trend,
                    'rtransfer_patients': simulation.rtransfer_trend,
                    'radiology_patients': simulation.radiology_trend,
                    'estabd_patients': simulation.estabd_trend,
                    'dtherap_patients': simulation.dtherap_trend,
                    'moutcome_patients': simulation.moutcome_trend}
                with open('time_dataframe_' + str(times) + '.json', mode='w', encoding="utf-8") as convert_file:
                    convert_file.write(json.dumps(time_dataframe, ensure_ascii=False))
                tdf = open('trends_' + str(times) + '.csv', 'w')
                writer = csv.writer(tdf, delimiter=";")
                key_list = list(time_dataframe.keys())
                limit = len(key_list)
                writer.writerow(time_dataframe.keys())
                for i in list(range(0, len(simulation.register_trend)-1)):
                    #print(i)
                    writer.writerow([time_dataframe[x][i] for x in key_list])
                os._exit(0)

print('Simulation starting, current doctors: ' + str(simulation.DOCTORS))
time.sleep(1)

starter = StarterThread()
starter.start()

watcher = SimulationThread()
watcher.start()
watcher.join()
