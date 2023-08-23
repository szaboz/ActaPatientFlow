import simulation
import time, random

logbook = []

#Common
def log_patient_object(patient):
    print(str(patient))
    patient.attr['name'] = patient.name
    patient.attr['age'] = patient.age
    patient.attr['arrival'] = patient.arrival
    logbook.append(patient.attr)

#Registration
def register_patient() -> simulation.Patient:
    patient  = simulation.Patient()
    
    patient.waiting = True
    simulation.employee_sem.acquire()
    simulation.register_patients += 1
    if simulation.register_patients > simulation.register_max_patients:
        simulation.register_max_patients = simulation.register_patients
    simulation.EMPLOYEE_QUEUE[patient.triage_level-1].insert(0, patient.stop_waiting)
    simulation.employee_sem.release()
    ts1 = time.time()
    patient.wait_for_somebody()
    tsdb = time.time()
    patient.attr['registration_waiting'] = tsdb-ts1
    registration_waiting = 0
    if patient.triage_level >= 3:
        registration_waiting = random.choices([2,3,4,5,6], [3,4,3,2,1], k=1)[0]
    else:
        registration_waiting = random.randint(0,2)
    patient.attr['register_patient_time'] = registration_waiting
    time.sleep(registration_waiting)
    ts2 = time.time()
    patient.attr['registration_full'] = ts2-ts1
    print(patient.name + ' Register patient')
    simulation.employee_sem.acquire()
    simulation.EMPLOYEE += 1
    simulation.register_patients -= 1
    if patient.attr['register_patient_time'] > simulation.register_longest_time:
        simulation.register_longest_time = patient.attr['register_patient_time']
    if patient.attr['registration_full'] > simulation.register_longest_full:
        simulation.register_longest_full = patient.attr['registration_full']
    simulation.employee_sem.release()
    return patient

#Triage Area
def evaluate_urgency(patient):
    simulation.gnr_sem.acquire()
    simulation.evaluate_patients += 1
    if simulation.evaluate_patients > simulation.evaluate_max_patients:
        simulation.evaluate_max_patients = simulation.evaluate_patients
    simulation.GENERIC_NURSES_QUEUE[patient.triage_level-1].insert(0, patient.stop_waiting)
    simulation.gnr_sem.release()
    ts1 = time.time()
    patient.wait_for_somebody()
    tsdb = time.time()
    patient.attr['evaluate_urgency_waiting'] = tsdb-ts1

    evaluate_urgency_time = 0
    if patient.triage_level >= 3:
        patient.attr['urgency'] = 0
        evaluate_urgency_time = random.choices([1,2,3,4], [2,3,2,1], k=1)[0]
    else:
        patient.attr['urgency'] = 1
        evaluate_urgency_time = 0
    patient.attr['evaluate_urgency_time'] = evaluate_urgency_time
    time.sleep(evaluate_urgency_time)
    if patient.attr['urgency'] == 0:
        patient.attr['abandons'] = 1 if random.uniform(0,1) <= 0.027 else 0
    else:
        patient.attr['abandons'] = None

    ts2 = time.time()
    patient.attr['evaluate_urgency_full'] = ts2-ts1
    print(patient.name + ' Evaluate urgency')
    simulation.gnr_sem.acquire()
    simulation.GENERIC_NURSES += 1
    simulation.evaluate_patients -= 1
    if patient.attr['evaluate_urgency_time'] > simulation.evaluate_longest_time:
        simulation.evaluate_longest_time = patient.attr['evaluate_urgency_time']
    if patient.attr['evaluate_urgency_full'] > simulation.evaluate_longest_full:
        simulation.evaluate_longest_full = patient.attr['evaluate_urgency_full']
    simulation.gnr_sem.release()

def provide_pre_visit(patient):
    simulation.gnr_sem.acquire()
    simulation.previsit_patients += 1
    if simulation.previsit_patients > simulation.previsit_max_patients:
        simulation.previsit_max_patients = simulation.previsit_patients
    simulation.GENERIC_NURSES_QUEUE[patient.triage_level-1].insert(0, patient.stop_waiting)
    simulation.gnr_sem.release()
    ts1 = time.time()
    patient.wait_for_somebody()
    tsdb = time.time()
    patient.attr['provide_pre_visit_waiting'] = tsdb-ts1

    provide_pre_visit_time = 0
    if patient.triage_level >= 3:
        provide_pre_visit_time = random.randint(3,10)
    else:
        provide_pre_visit_time = random.randint(1,3)

    patient.attr['provide_pre_visit_time'] = provide_pre_visit_time
    time.sleep(provide_pre_visit_time)

    ts2 = time.time()
    patient.attr['provide_pre_visit_full'] = ts2-ts1
    print(patient.name + ' Provide pre-visit')
    simulation.gnr_sem.acquire()
    simulation.GENERIC_NURSES += 1
    simulation.previsit_patients -= 1
    if  patient.attr['provide_pre_visit_time'] > simulation.previsit_longest_time:
        simulation.previsit_longest_time =  patient.attr['provide_pre_visit_time']
    if patient.attr['provide_pre_visit_full'] > simulation.previsit_longest_full:
        simulation.previsit_longest_full = patient.attr['provide_pre_visit_full']
    simulation.gnr_sem.release()

def assign_esi(patient):
    simulation.gnr_sem.acquire()
    simulation.GENERIC_NURSES_QUEUE[patient.triage_level-1].insert(0, patient.stop_waiting)
    simulation.gnr_sem.release()
    ts1 = time.time()
    patient.wait_for_somebody()
    tsdb = time.time()
    patient.attr['assign_esi_waiting'] = tsdb-ts1
    print(patient.name + ' Assign ESI')
    simulation.gnr_sem.acquire()
    simulation.GENERIC_NURSES += 1
    simulation.gnr_sem.release()
    patient.attr['immediate_ic'] = 1 if random.uniform(0,1) <= 0.015 else 0

#Visit Area
def manage_outcome(patient):
    simulation.snr_sem.acquire()
    simulation.moutcome_patients += 1
    if simulation.moutcome_patients > simulation.moutcome_max_patients:
        simulation.moutcome_max_patients = simulation.moutcome_patients
    simulation.SPECIALIZED_NURSES_QUEUE[patient.triage_level-1].insert(0, patient.stop_waiting)
    simulation.snr_sem.release()
    ts1 = time.time()
    patient.wait_for_somebody()
    tsdb = time.time()
    patient.attr['manage_outcome_waiting'] = tsdb-ts1

    manage_outcome_time = 0
    if patient.triage_level >= 3:
        manage_outcome_time = random.randint(7,15)
    else:
        manage_outcome_time = random.randint(2,4)

    patient.attr['manage_outcome_time'] = manage_outcome_time
    time.sleep(manage_outcome_time)

    ts2 = time.time()
    patient.attr['manage_outcome_full'] = ts2-ts1
    print(patient.name + ' Manage outcome')

    outcomes = ['ic', 'dis', 'ef', 'dea', 'hos']
    patient.attr['outcomes'] = random.choices(outcomes, [0.048,0.735,0.004,0.004,0.209], k=1)[0]
    simulation.snr_sem.acquire()
    simulation.SPECIALIZED_NURSES += 1
    simulation.moutcome_patients -= 1
    if patient.attr['manage_outcome_time'] > simulation.moutcome_longest_time:
        simulation.moutcome_longest_time =  patient.attr['manage_outcome_time']
    if patient.attr['manage_outcome_full'] > simulation.moutcome_longest_full:
        simulation.moutcome_longest_full = patient.attr['manage_outcome_full']
    simulation.snr_sem.release()
    if patient.attr['outcomes'] == 'dis': #embedded pre-end state
        patient.attr['result'] = "The Patient was dismissed"
        print(patient.name + ' dismissed')
        log_patient_object(patient)

def search_external_facility(patient):
    simulation.snr_sem.acquire()
    simulation.SPECIALIZED_NURSES_QUEUE[patient.triage_level-1].insert(0, patient.stop_waiting)
    simulation.snr_sem.release()
    ts1 = time.time()
    patient.wait_for_somebody()
    tsdb = time.time()
    patient.attr['search_efacility_waiting'] = tsdb-ts1

    search_efacility_time = random.randint(60,480)
    eft = search_efacility_time/10

    print(patient.name + ' eft time: ' + str(eft))

    patient.attr['search_efacility_time'] = search_efacility_time
    time.sleep(eft)
    simulation.snr_sem.acquire()
    simulation.SPECIALIZED_NURSES += 1
    simulation.snr_sem.release()
    print(patient.name + ' Search external facility')

#Visit SubProcess
def collect_history(patient):
    simulation.snr_sem.acquire()
    simulation.chistory_patients += 1
    if simulation.chistory_patients > simulation.chistory_max_patients:
        simulation.chistory_max_patients = simulation.chistory_patients
    simulation.SPECIALIZED_NURSES_QUEUE[patient.triage_level-1].insert(0, patient.stop_waiting)
    simulation.snr_sem.release()
    ts1 = time.time()
    patient.wait_for_somebody()
    tsdb = time.time()
    patient.attr['collect_history_waiting'] = tsdb-ts1

    collect_history_time = 0
    if patient.triage_level >= 3:
        collect_history_time = random.randint(1,4)
    else:
        collect_history_time = random.randint(1,2)
    patient.attr['collect_history_time'] = collect_history_time
    time.sleep(collect_history_time)

    ts2 = time.time()
    patient.attr['collect_history_full'] = ts2-ts1
    print(patient.name + ' Collect history')
    simulation.snr_sem.acquire()
    simulation.SPECIALIZED_NURSES += 1
    simulation.chistory_patients -= 1
    if patient.attr['collect_history_time'] > simulation.chistory_longest_time:
        simulation.chistory_longest_time =  patient.attr['collect_history_time']
    if patient.attr['collect_history_full'] > simulation.chistory_longest_full:
        simulation.chistory_longest_full = patient.attr['collect_history_full']
    simulation.snr_sem.release()

def hypothisize_diagnosis(patient):
    simulation.doctors_sem.acquire()
    simulation.hypthosize_patients += 1
    if simulation.hypthosize_patients > simulation.hypthosize_max_patients:
        simulation.hypthosize_max_patients = simulation.hypthosize_patients
    simulation.DOCTORS_QUEUE[patient.triage_level-1].insert(0, patient.stop_waiting)
    simulation.doctors_sem.release()
    ts1 = time.time()
    patient.wait_for_somebody()
    tsdb = time.time()
    patient.attr['hyp_diag_waiting'] = tsdb-ts1

    hyp_diag_time = 0
    if patient.triage_level >= 3:
        hyp_diag_time = random.choices([1,2,3,4,5], [3,4,3,2,1], k=1)[0]
    else:
        hyp_diag_time = random.randint(1,2)
    patient.attr['hyp_diag_time'] = hyp_diag_time
    time.sleep(hyp_diag_time)

    ts2 = time.time()
    patient.attr['hyp_diag_full'] = ts2-ts1
    print(patient.name + ' Hypthosize diagnosis')
    simulation.doctors_sem.acquire()
    simulation.DOCTORS += 1
    simulation.hypthosize_patients -= 1
    if patient.attr['hyp_diag_time'] > simulation.hypthosize_longest_time:
        simulation.hypthosize_longest_time =  patient.attr['hyp_diag_time']
    if patient.attr['hyp_diag_full'] > simulation.hypthosize_longest_full:
        simulation.hypthosize_longest_full = patient.attr['hyp_diag_full']
    simulation.doctors_sem.release()
    
    patient.attr['exams'] = random.choice([True, False])
    patient.attr['images'] = random.choice([True, False])

def establish_diagnosis(patient):
    simulation.doctors_sem.acquire()
    simulation.estabd_patients += 1
    if simulation.estabd_patients > simulation.estabd_max_patients:
        simulation.estabd_max_patients = simulation.estabd_patients
    simulation.DOCTORS_QUEUE[patient.triage_level-1].insert(0, patient.stop_waiting)
    simulation.doctors_sem.release()
    ts1 = time.time()
    patient.wait_for_somebody()
    tsdb = time.time()
    patient.attr['et_diag_waiting'] = tsdb-ts1

    et_diag_time = 0
    patient.attr['diagnosis'] = random.choice(['med', 'ort', 'sur'])
    if patient.attr['diagnosis'] == 'med':
        if patient.triage_level >= 3:
            et_diag_time = random.randint(5,25)
        else:
            et_diag_time = random.randint(3,5)
    elif patient.attr['diagnosis'] == 'sur':
        if patient.triage_level >= 3:
            et_diag_time = random.randint(3,12)
        else:
            et_diag_time = random.randint(3,5)
    else:
        if patient.triage_level >= 3:
            et_diag_time = random.randint(3,7)
        else:
            et_diag_time = random.randint(3,5)
    patient.attr['et_diag_time'] = et_diag_time
    time.sleep(et_diag_time)

    ts2 = time.time()
    patient.attr['et_diag_full'] = ts2-ts1
    print(patient.name + ' Establish diagnosis')
    simulation.doctors_sem.acquire()
    simulation.DOCTORS += 1
    simulation.estabd_patients -= 1
    if patient.attr['et_diag_time'] > simulation.estabd_longest_time:
        simulation.estabd_longest_time = patient.attr['et_diag_time']
    if patient.attr['et_diag_full'] > simulation.estabd_longest_full:
        simulation.estabd_longest_full = patient.attr['et_diag_full']
    simulation.doctors_sem.release()

def define_therapy(patient):
    simulation.doctors_sem.acquire()
    simulation.dtherap_patients += 1
    if simulation.dtherap_patients > simulation.dtherap_max_patients:
        simulation.dtherap_max_patients = simulation.dtherap_patients
    simulation.DOCTORS_QUEUE[patient.triage_level-1].insert(0, patient.stop_waiting)
    simulation.doctors_sem.release()
    ts1 = time.time()
    patient.wait_for_somebody()
    tsdb = time.time()
    patient.attr['def_therapy_waiting'] = tsdb-ts1

    def_therapy_time = 0
    if patient.triage_level >= 3:
        def_therapy_time = random.randint(2,5)
    else:
        def_therapy_time = random.randint(5,10)
    patient.attr['def_therapy_time'] = def_therapy_time
    time.sleep(def_therapy_time)

    ts2 = time.time()
    patient.attr['def_therapy_full'] = ts2-ts1
    print(patient.name + ' Define therapy')
    simulation.doctors_sem.acquire()
    simulation.DOCTORS += 1
    simulation.dtherap_patients -= 1
    if patient.attr['def_therapy_time'] > simulation.dtherap_longest_time:
        simulation.dtherap_longest_time = patient.attr['def_therapy_time']
    if patient.attr['def_therapy_full'] > simulation.dtherap_longest_full:
        simulation.dtherap_longest_full = patient.attr['def_therapy_full']
    simulation.doctors_sem.release()

def take_blood_sample(patient):
    simulation.snr_sem.acquire()
    simulation.bloodsample_patients += 1
    if simulation.bloodsample_patients > simulation.bloodsample_max_patients:
        simulation.bloodsample_max_patients = simulation.bloodsample_patients
    simulation.SPECIALIZED_NURSES_QUEUE[patient.triage_level-1].insert(0, patient.stop_waiting)
    simulation.snr_sem.release()
    ts1 = time.time()
    patient.wait_for_somebody()
    tsdb = time.time()
    patient.attr['take_blood_waiting'] = tsdb-ts1

    take_blood_time = 0
    if patient.triage_level >= 3:
        take_blood_time = random.randint(3,8)
    else:
        take_blood_time = random.randint(1,2)
    patient.attr['take_blood_time'] = take_blood_time
    time.sleep(take_blood_time)

    ts2 = time.time()
    patient.attr['take_blood_full'] = ts2-ts1
    print(patient.name + ' Take blood sample')
    simulation.snr_sem.acquire()
    simulation.SPECIALIZED_NURSES += 1
    simulation.bloodsample_patients -= 1
    if patient.attr['take_blood_time'] > simulation.bloodsample_longest_time:
        simulation.bloodsample_longest_time = patient.attr['take_blood_time']
    if patient.attr['take_blood_full'] > simulation.bloodsample_longest_full:
        simulation.bloodsample_longest_full = patient.attr['take_blood_full']
    simulation.snr_sem.release()

def transfer_to_radiology(patient):
    simulation.operator_sem.acquire()
    simulation.rtransfer_patients += 1
    if simulation.rtransfer_patients > simulation.rtransfer_max_patients:
        simulation.rtransfer_max_patients = simulation.rtransfer_patients
    simulation.GENERIC_OPERATORS_QUEUE[patient.triage_level-1].insert(0, patient.stop_waiting)
    simulation.operator_sem.release()
    ts1 = time.time()
    patient.wait_for_somebody()
    tsdb = time.time()
    patient.attr['transfer_to_rad_waiting'] = tsdb-ts1

    transfer_to_rad_time = 0
    if patient.triage_level >= 3:
        transfer_to_rad_time = random.choices([5,6,7,8,9,10,11,12,13,14,15], [7,8,9,10,9,8,7,6,5,4,3], k=1)[0]
    else:
        transfer_to_rad_time = random.randint(3,5)
    patient.attr['transfer_to_rad_time'] = transfer_to_rad_time
    time.sleep(transfer_to_rad_time)

    ts2 = time.time()
    patient.attr['transfer_to_rad_full'] = ts2-ts1
    print(patient.name + ' Transfer to radiology')
    simulation.operator_sem.acquire()
    simulation.GENERIC_OPERATORS += 1
    simulation.rtransfer_patients -= 1
    if patient.attr['transfer_to_rad_time'] > simulation.rtransfer_longest_time:
        simulation.rtransfer_longest_time = patient.attr['transfer_to_rad_time']
    if patient.attr['transfer_to_rad_full'] > simulation.rtransfer_longest_full:
        simulation.rtransfer_longest_full = patient.attr['transfer_to_rad_full']
    simulation.operator_sem.release()

def laboratory(patient):
    simulation.doctors_sem.acquire()
    simulation.laboratory_patients += 1
    if simulation.laboratory_patients > simulation.laboratory_max_patients:
        simulation.laboratory_max_patients = simulation.laboratory_patients
    simulation.DOCTORS_QUEUE[patient.triage_level-1].insert(0, patient.stop_waiting)
    simulation.doctors_sem.release()
    ts1 = time.time()
    patient.wait_for_somebody()
    tsdb = time.time()
    patient.attr['lab_waiting'] = tsdb-ts1

    lab_time = 0
    if patient.triage_level >= 3:
        lab_time = random.randint(5,15)
    else:
        lab_time = random.randint(3,5)
    patient.attr['lab_time'] = lab_time
    time.sleep(lab_time)

    ts2 = time.time()
    patient.attr['lab_full'] = ts2-ts1
    print(patient.name + ' Laboratory')
    simulation.doctors_sem.acquire()
    simulation.DOCTORS += 1
    simulation.laboratory_patients -= 1
    if patient.attr['lab_time'] > simulation.laboratory_longest_time:
        simulation.laboratory_longest_time = patient.attr['lab_time']
    if patient.attr['lab_full'] > simulation.laboratory_longest_full:
        simulation.laboratory_longest_full = patient.attr['lab_full']
    simulation.doctors_sem.release()

def radiology(patient):
    simulation.snr_sem.acquire()
    simulation.radiology_patients += 1
    if simulation.radiology_patients > simulation.radiology_max_patients:
        simulation.radiology_max_patients = simulation.radiology_patients
    simulation.SPECIALIZED_NURSES_QUEUE[patient.triage_level-1].insert(0, patient.stop_waiting)
    simulation.snr_sem.release()
    ts1 = time.time()
    patient.wait_for_somebody()
    tsdb = time.time()
    patient.attr['radiology_waiting'] = tsdb-ts1

    radiology_time = 0
    if patient.triage_level >= 3:
        radiology_time = random.randint(10,20)
    else:
        radiology_time = random.randint(7,12)
    patient.attr['radiology_time'] = radiology_time
    time.sleep(radiology_time)

    ts2 = time.time()
    patient.attr['radiology_full'] = ts2-ts1
    print(patient.name + ' Radiology')
    simulation.snr_sem.acquire()
    simulation.SPECIALIZED_NURSES += 1
    simulation.radiology_patients -= 1
    if patient.attr['radiology_time'] > simulation.radiology_longest_time:
        simulation.radiology_longest_time = patient.attr['radiology_time']
    if patient.attr['radiology_full'] > simulation.radiology_longest_full:
        simulation.radiology_longest_full = patient.attr['radiology_full']
    simulation.snr_sem.release()

#Pre-End States
def discharge_patient(patient):
    patient.attr['result'] = "The Patient abandoned the TA"
    print(patient.name + ' Discharge patient')
    log_patient_object(patient)

def transfer_to_internal_clinic(patient):
    patient.attr['result'] = "The Patient was transferred to Internal Clinic"
    simulation.gnr_sem.acquire()
    simulation.GENERIC_NURSES_QUEUE[patient.triage_level-1].insert(0, patient.stop_waiting)
    simulation.gnr_sem.release()
    ts1 = time.time()
    patient.wait_for_somebody()
    tsdb = time.time()
    patient.attr['iclinic_transfer_waiting'] = tsdb-ts1
    simulation.gnr_sem.acquire()
    simulation.GENERIC_NURSES += 1
    simulation.gnr_sem.release()
    print(patient.name + ' Transfer to clinics')
    log_patient_object(patient)

def transfer_to_morgue(patient):
    patient.attr['result'] = "The Patient died, was transferred to morgue"
    simulation.operator_sem.acquire()
    simulation.GENERIC_OPERATORS_QUEUE[patient.triage_level-1].insert(0, patient.stop_waiting)
    simulation.operator_sem.release()
    ts1 = time.time()
    patient.wait_for_somebody()
    tsdb = time.time()
    patient.attr['morgue_transfer_waiting'] = tsdb-ts1

    morgue_transfer_time = 7
    patient.attr['morgue_transfer_time'] = morgue_transfer_time
    time.sleep(morgue_transfer_time)

    ts2 = time.time()
    patient.attr['morgue_transfer_full'] = ts2-ts1
    print(patient.name + ' Transfer to morgue')
    simulation.operator_sem.acquire()
    simulation.GENERIC_OPERATORS += 1
    simulation.operator_sem.release()
    log_patient_object(patient)
    

def transfer_to_external_facility(patient):
    patient.attr['result'] = "The Patient was transferred to external facility"
    simulation.operator_sem.acquire()
    simulation.GENERIC_OPERATORS_QUEUE[patient.triage_level-1].insert(0, patient.stop_waiting)
    simulation.operator_sem.release()
    ts1 = time.time()
    patient.wait_for_somebody()
    tsdb = time.time()
    patient.attr['transfer_to_ef_waiting'] = tsdb-ts1

    transfer_to_ef_time = 7
    patient.attr['transfer_to_ef_time'] = transfer_to_ef_time
    time.sleep(transfer_to_ef_time)

    ts2 = time.time()
    patient.attr['transfer_to_ef_full'] = ts2-ts1
    print(patient.name + ' Transfer to external facility')
    simulation.operator_sem.acquire()
    simulation.GENERIC_OPERATORS += 1
    simulation.operator_sem.release()
    log_patient_object(patient)

def hospitalize_in_ward(patient):
    patient.attr['result'] = "The Patient was hospitalized in ward"
    simulation.snr_sem.acquire()
    simulation.SPECIALIZED_NURSES_QUEUE[patient.triage_level-1].insert(0, patient.stop_waiting)
    simulation.snr_sem.release()
    ts1 = time.time()
    patient.wait_for_somebody()
    tsdb = time.time()
    patient.attr['wa_hosp_waiting'] = tsdb-ts1

    wa_hosp_time = 15
    patient.attr['wa_hosp_time'] = wa_hosp_time
    time.sleep(wa_hosp_time)

    ts2 = time.time()
    patient.attr['wa_hosp_full'] = ts2-ts1
    print(patient.name + ' Hospitalize in ward')
    simulation.snr_sem.acquire()
    simulation.SPECIALIZED_NURSES += 1
    simulation.snr_sem.release()
    log_patient_object(patient)
