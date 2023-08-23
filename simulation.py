import threading, time
import random
import generator

class Patient:
  name = 'something'
  attr = {}
  waiting = False
  triage_level = 0
  arrival = None
  def __init__(self):
      self.name = generator.get_a_name()
      self.age = random.randint(16, 60)
      self.attr = {}
      self.waiting = False
      #self.triage_level =  random.randint(1,4)
      self.triage_level = random.choices([1,2,3,4,5],[0.00673,0.01241,0.23359,0.40175,0.34549], k=1)[0]
      self.attr['triage'] = self.triage_level
      self.arrival = time.time()
      
      
  def __str__(self):
      return self.name + ' , ' + str(self.age) + ' , ' + str(self.triage_level) + ': ' + str(self.attr)
  
  def stop_waiting(self):
      print(self.name + ' stopped waiting')
      self.waiting = False
      
  def wait_for_somebody(self):
      while(self.waiting):
          pass

register_patients = 0 #
register_max_patients = 0 #
register_longest_time = 0 #
register_longest_full = 0 #
register_trend = []

evaluate_patients = 0 #
evaluate_max_patients = 0 #
evaluate_longest_time = 0 #
evaluate_longest_full = 0 # 
evaluate_trend = []

previsit_patients = 0 #
previsit_max_patients = 0 #
previsit_longest_time = 0 #
previsit_longest_full = 0 #
previsit_trend = []

chistory_patients = 0 #
chistory_max_patients = 0 #
chistory_longest_time = 0 #
chistory_longest_full = 0 #
chistory_trend = []

hypthosize_patients = 0 #
hypthosize_max_patients = 0 #
hypthosize_longest_time = 0 #
hypthosize_longest_full = 0 #
hypthosize_trend = []

bloodsample_patients = 0 #
bloodsample_max_patients = 0 #
bloodsample_longest_time = 0 #
bloodsample_longest_full = 0 #
bloodsample_trend = []

laboratory_patients = 0 #
laboratory_max_patients = 0 #
laboratory_longest_time = 0 #
laboratory_longest_full = 0 #
laboratory_trend = []

rtransfer_patients = 0 #
rtransfer_max_patients = 0 #
rtransfer_longest_time = 0 #
rtransfer_longest_full = 0 #
rtransfer_trend = []

radiology_patients = 0 #
radiology_max_patients = 0 #
radiology_longest_time = 0 #
radiology_longest_full = 0 #
radiology_trend = []

estabd_patients = 0 #
estabd_max_patients = 0 #
estabd_longest_time = 0 #
estabd_longest_full = 0 #
estabd_trend = []

dtherap_patients = 0 #
dtherap_max_patients = 0 #
dtherap_longest_time = 0 #
dtherap_longest_full = 0 #
dtherap_trend = []

moutcome_patients = 0 #
moutcome_max_patients = 0 #
moutcome_longest_time = 0 #
moutcome_longest_full = 0 #
moutcome_trend = []

DOCTORS = 3
GENERIC_NURSES = 2
SPECIALIZED_NURSES = 3
EMPLOYEE = 2
GENERIC_OPERATORS = 4

DOCTORS_QUEUE = [[],[],[],[],[]]
GENERIC_NURSES_QUEUE = [[],[],[],[],[]]
SPECIALIZED_NURSES_QUEUE = [[],[],[],[],[]]
EMPLOYEE_QUEUE = [[],[],[],[],[]]
GENERIC_OPERATORS_QUEUE = [[],[],[],[],[]]

doctors_sem = threading.Semaphore()
employee_sem = threading.Semaphore()
snr_sem = threading.Semaphore()
gnr_sem = threading.Semaphore()
operator_sem = threading.Semaphore()

class TrendFollowerThread(threading.Thread):
    def run(self):
        global register_patients, register_trend
        global evaluate_patients, evaluate_trend
        global previsit_patients, previsit_trend
        global chistory_patients, chistory_trend
        global hypthosize_patients, hypthosize_trend
        global bloodsample_patients, bloodsample_trend
        global laboratory_patients, laboratory_trend
        global rtransfer_patients, rtransfer_trend
        global radiology_patients, radiology_trend
        global estabd_patient, estabd_trend
        global dtherap_patients, dtherap_trend
        global moutcome_patients, moutcome_trend
        while True:
            register_trend.append(register_patients)
            evaluate_trend.append(evaluate_patients)
            previsit_trend.append(previsit_patients)
            chistory_trend.append(chistory_patients)
            hypthosize_trend.append(hypthosize_patients)
            bloodsample_trend.append(bloodsample_patients)
            laboratory_trend.append(laboratory_patients)
            rtransfer_trend.append(rtransfer_patients)
            radiology_trend.append(radiology_patients)
            estabd_trend.append(estabd_patients)
            dtherap_trend.append(dtherap_patients)
            moutcome_trend.append(moutcome_patients)
            time.sleep(1)
tft = TrendFollowerThread()
tft.start()

class DoctorSchedulerThread(threading.Thread):
    def run(self):
        global DOCTORS, DOCTORS_QUEUE
        while True:
            current_doctors = DOCTORS
            for i in range(len(DOCTORS_QUEUE)):
                if len(DOCTORS_QUEUE[i]) > 0:
                    for l in range(len(DOCTORS_QUEUE[i])-1,-1,-1):
                        # insert with: DOCTORS_QUEUE[0].insert(0, something)
                        if current_doctors > 0:
                            current_doctors -= 1
                            doctors_sem.acquire()
                            DOCTORS -= 1 #ezzel elvileg van arra lehetőség, hogy már valójában van doki, de scheduler még nem észleli
                            DOCTORS_QUEUE[i][l]()
                            del DOCTORS_QUEUE[i][l]
                            doctors_sem.release()


dr = DoctorSchedulerThread()
dr.start()

class GNurseSchedulerThread(threading.Thread):
    def run(self):
        global GENERIC_NURSES, GENERIC_NURSES_QUEUE
        while True:
            current_gnurse = GENERIC_NURSES
            for i in range(len(GENERIC_NURSES_QUEUE)):
                if len(GENERIC_NURSES_QUEUE[i]) > 0:
                    for l in range(len(GENERIC_NURSES_QUEUE[i])-1,-1,-1):
                        if current_gnurse > 0:
                            current_gnurse -= 1
                            gnr_sem.acquire()
                            GENERIC_NURSES -= 1
                            GENERIC_NURSES_QUEUE[i][l]()
                            del GENERIC_NURSES_QUEUE[i][l]
                            gnr_sem.release()

gnr = GNurseSchedulerThread()
gnr.start()

class SNurseSchedulerThread(threading.Thread):
    def run(self):
        global SPECIALIZED_NURSES, SPECIALIZED_NURSES_QUEUE
        while True:
            current_snurse = SPECIALIZED_NURSES
            for i in range(len(SPECIALIZED_NURSES_QUEUE)):
                if len(SPECIALIZED_NURSES_QUEUE[i]) > 0:
                    for l in range(len(SPECIALIZED_NURSES_QUEUE[i])-1,-1,-1):
                        if current_snurse > 0:
                            current_snurse -= 1
                            snr_sem.acquire()
                            SPECIALIZED_NURSES -= 1
                            SPECIALIZED_NURSES_QUEUE[i][l]()
                            del SPECIALIZED_NURSES_QUEUE[i][l]
                            snr_sem.release()

snr = SNurseSchedulerThread()
snr.start()

class EmployeeSchedulerThread(threading.Thread):
    def run(self):
        global EMPLOYEE, EMPLOYEE_QUEUE, employee_sem
        while True:
            current_employee = EMPLOYEE
            for i in range(len(EMPLOYEE_QUEUE)):
                if len(EMPLOYEE_QUEUE[i]) > 0:
                    for l in range(len(EMPLOYEE_QUEUE[i])-1,-1,-1):
                        if current_employee > 0:
                            current_employee -= 1
                            employee_sem.acquire()
                            EMPLOYEE -= 1
                            EMPLOYEE_QUEUE[i][l]()
                            del EMPLOYEE_QUEUE[i][l]
                            employee_sem.release()

er = EmployeeSchedulerThread()
er.start()

class OperatorSchedulerThread(threading.Thread):
    def run(self):
        global GENERIC_OPERATORS, GENERIC_OPERATORS_QUEUE
        while True:
            current_operators = GENERIC_OPERATORS
            for i in range(len(GENERIC_OPERATORS_QUEUE)):
                if len(GENERIC_OPERATORS_QUEUE[i]) > 0:
                    for l in range(len(GENERIC_OPERATORS_QUEUE[i])-1,-1,-1):
                        if current_operators > 0:
                            current_operators -= 1
                            operator_sem.acquire()
                            GENERIC_OPERATORS -= 1
                            GENERIC_OPERATORS_QUEUE[i][l]()
                            del GENERIC_OPERATORS_QUEUE[i][l]
                            operator_sem.release()

opr = OperatorSchedulerThread()
opr.start()