
from ps7_v1 import *
import random
import matplotlib.pyplot as plt
from cProfile import label

class ResistantVirus(SimpleVirus):
    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb

    def getMaxBirthProb(self):
        return self.maxBirthProb

    def getResistances(self):
        return self.resistances

    def getMutProb(self):
        return self.mutProb

    def isResistantTo(self, drug):
        if drug in self.getResistances():
            if self.getResistances()[drug] == True: return True
            else: return False            
        else:
            raise KeyError ('Not in resistances (neither true nor false)') 

    def reproduce(self, popDensity, activeDrugs):
        isResistant = True
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                isResistant = False
                break
                
        # if resistant, may reproduce
        maxReproduceProb = self.maxBirthProb * (1 - popDensity)

        if isResistant:
            if random.random() < maxReproduceProb:
                childResistances = self.getResistances().copy()
                for drug in childResistances:
                    if self.mutProb > random.random():
                        childResistances[drug] = not (self.isResistantTo(drug))

                return ResistantVirus(self.maxBirthProb, self.clearProb, childResistances, self.mutProb)
            else: 
                raise NoChildException ('This child does not reproduce') 
        else:
            raise NoChildException ('This child does not reproduce')

        
        
class Patient(SimplePatient):
    def __init__(self, viruses, maxPop):

        SimplePatient.__init__(self, viruses, maxPop)
        self.drugList = []

    def getViruses(self):
        return self.viruses

    def addPrescription(self, newDrug):
        if newDrug not in self.drugList:
            self.drugList.append(newDrug)

    def getPrescriptions(self):
        return self.drugList

    def getResistPop(self, drugResist):      
        resistantViruses = 0
        for drug in drugResist:
            for virus in self.viruses:
                if virus.isResistantTo(drug):
                    resistantViruses += 1
        return resistantViruses

    def update(self):
        offspringViruses = []
#         for virus in self.getViruses():
#             if virus.doesClear():
#                 self.viruses.remove(virus)
#         
        
        numRemoveVirus = 0
        for virus in self.getViruses() :
            if virus.doesClear():
                numRemoveVirus += 1
                self.viruses.remove(virus)
            else:
                clear = False
                for drug in self.getPrescriptions() :
                    if not virus.isResistantTo(drug):
                        clear = True
                        break
                if clear and virus.doesClear():
                    self.viruses.remove(virus)
                    numRemoveVirus += 1
 
        # update population density
        popDens = float(self.getTotalPop()) / float(self.maxPop)
 
        # determine which viruses reproduce
        for virus in self.getViruses():
            try:
                offspringViruses.append(virus.reproduce(popDens, self.getPrescriptions()))
            except NoChildException: pass
 
        for child in offspringViruses:
            if self.getTotalPop() < self.maxPop:
                self.viruses.append(child)
 
        return self.getTotalPop()



def virusCollection(numViruses, maxBirthProb, clearProb, resistances, mutProb):

    viruses = []
    for virusNum in range(numViruses):
        viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
    return viruses 

def simulationWithDrug(Drug1=150, returnVirusAmount=False , numTrials = 100, numTimeSteps = 500):
    
    random.seed()
    # Virus Characteristics.
    maxPop = 1000
    numViruses = 100
    maxBirthProb = 0.1
    clearProb = 0.05
    mutProb = 0.005
    resistances = {'guttagonol': False}

    dataMatrix = numpy.zeros(shape = (numTrials, numTimeSteps))
    dataMatrixResistVs = numpy.zeros(shape = (numTrials, numTimeSteps))
     
    # run number of trials
    for trial in range(numTrials):
                
        # instantiate viruses and patient
        viruses = virusCollection(numViruses, maxBirthProb, clearProb, resistances, mutProb)
        randPatientX = Patient(viruses, maxPop)
        # Simulate the time-steps.
        dataMatrix[trial][0] = numViruses
#         dataMatrixResistVs[trial][0] = numViruses
        for time in range(numTimeSteps):
            if time == Drug1 :
                randPatientX.addPrescription('guttagonol')
            dataMatrix[trial][time] += randPatientX.update()
            dataMatrixResistVs[trial][time] += randPatientX.getResistPop(['guttagonol'])
            

    # Statistical Analysis.
    meanData = dataMatrix.mean(0)
    if returnVirusAmount : return meanData
    meanDataResistVs = dataMatrixResistVs.mean(0)
    
    time = numpy.arange(numTimeSteps) 
    stdData95_CI = dataMatrix.std(0) * 2
    selectedTime = numpy.arange(0, numTimeSteps, 10)
    # Ploting.
    pylab.title("With Drug")
    pylab.plot(time, meanData)
    pylab.plot(meanDataResistVs)
    pylab.xlabel('Time')
    pylab.ylabel('Virus')
    pylab.errorbar(time[selectedTime], meanData[selectedTime], stdData95_CI[selectedTime], fmt = 'o')    
    pylab.show()








def simulationTwoDrugsVirusPopulations(Drug1=150, Drug2=350,returnVirusAmount=False, numTrials = 100, numTimeSteps = 500):
    """
    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for asimulation with a 300 time step delay
     between administering the 2 drugs and a simulations for which drugs are administered simultaneously.
    """
        
    random.seed()
    # Virus Characteristics.
    maxPop = 1000
    numViruses = 100
    maxBirthProb = 0.1
    clearProb = 0.05
    mutProb = 0.005
    resistances = {'guttagonol': False, 'srinol': False}

    dataMatrix = numpy.zeros(shape = (numTrials, numTimeSteps))
    dataMatrixResistVs = numpy.zeros(shape = (numTrials, numTimeSteps))
     
    # run number of trials
    for trial in range(numTrials):
                
        # instantiate viruses and patient
        viruses = virusCollection(numViruses, maxBirthProb, clearProb, resistances, mutProb)
        randPatientX = Patient(viruses, maxPop)
        # Simulate the time-steps.
        dataMatrix[trial][0] = numViruses
#         dataMatrixResistVs[trial][0] = numViruses
        for time in range(numTimeSteps):
            if time == Drug1:
                randPatientX.addPrescription('guttagonol')
            if time == Drug2:
                randPatientX.addPrescription('srinol')
            dataMatrix[trial][time] += randPatientX.update()
            dataMatrixResistVs[trial][time] += randPatientX.getResistPop(['guttagonol'])
            

    # Statistical Analysis.
    meanData = dataMatrix.mean(0)
    if returnVirusAmount : return meanData

    meanDataResistVs = dataMatrixResistVs.mean(0)
#     if returnVirusAmount : return meanData
    
    time = numpy.arange(numTimeSteps) 
    stdData95_CI = dataMatrix.std(0) * 2
    selectedTime = numpy.arange(0, numTimeSteps, 10)
    # Ploting.
    pylab.title("With Drug")
    pylab.plot(time, meanData)
    pylab.plot(meanDataResistVs)
    pylab.xlabel('Time')
    pylab.ylabel('Virus')
    pylab.errorbar(time[selectedTime], meanData[selectedTime], stdData95_CI[selectedTime], fmt = 'o')    
    pylab.show()
    
def simulationDelayedTreatment():
    """Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed
    treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of
    300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).
    """
    
#     timesteps = [300,150,75,0]
    bins = [0,50,100,150,200,250,300,350,400,450,500,550,600,650,700]
    # TODO
    plt.figure('simulation 1 drug after 300 timestemp delayed treatment ')
    plt.hist(simulationWithDrug(300,True), bins, histtype='bar', rwidth=0.8 ,alpha=0.3 , color ='c' , label = 'given at 300 timesteps')
    plt.xlabel('virus amount')
    plt.ylabel('patient amount')
    plt.title('simulation one drug delayed treatment ')
    plt.legend()
    plt.show()
    
    
    plt.figure('simulation 1 drug after 150 timestemp delayed treatment ')
    plt.hist(simulationWithDrug(150,True), bins, histtype='bar', rwidth=0.8 ,alpha=0.3 ,color ='r', label = ' given at 150 timesteps')
    plt.xlabel('virus amount')
    plt.ylabel('patient amount')
    plt.title('simulation one drug delayed treatment ')
    plt.legend()
    plt.show()
    
    
    plt.figure('simulation 1 drug after 75 timestemp delayed treatment ')
    plt.hist(simulationWithDrug(75,True), bins, histtype='bar', rwidth=0.8 ,alpha=0.5 ,color ='y', label = ' given at 75 timesteps')
    plt.xlabel('virus amount')
    plt.ylabel('patient amount')
    plt.title('simulation one drug delayed treatment ')
    plt.legend()
    plt.show()
    
    plt.figure('simulation 1 drug after 0 timestemp delayed treatment ')
    plt.hist(simulationWithDrug(0,True), bins, histtype='bar', rwidth=0.8 , alpha=0.4 ,color ='b', label = ' given at 0 timesteps')
    plt.xlabel('virus amount')
    plt.ylabel('patient amount')
    plt.title('simulation one drug delayed treatment ')
    plt.legend()
    plt.show()
    
def simulationTwoDrugsDelayedTreatment():
    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
    Histograms of final total virus populations are displayed for lag times
    of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """
    timesteps = [150,75,0]
    bins = [0,50,100,150,200,250,300,350,400,450,500,550,600,650,700]
    # TODO
    plt.figure('simulation 2 drug delayed treatment ')
    plt.subplot(131)
#     plt.hist(simulationTwoDrugsVirusPopulations(0,300,True), bins, histtype='bar', rwidth=0.8 ,alpha=0.3 , color ='c' , label = 'given at 300 timesteps')
    plt.hist(simulationTwoDrugsVirusPopulations(0,150,True), bins, histtype='bar', rwidth=0.8 ,alpha=0.3 ,color ='r', label = ' given after 150 timesteps')
    plt.xlabel('virus amount')
    plt.ylabel('patient amount')
    plt.title('for 0 delay of first drug ')
    plt.legend()
#     plt.show()
    
    
    plt.subplot(132)
    plt.hist(simulationTwoDrugsVirusPopulations(0,75,True), bins, histtype='bar', rwidth=0.8 ,alpha=0.5 ,color ='y', label = ' given after 75 timesteps')
    plt.xlabel('virus amount')
    plt.ylabel('patient amount')
    plt.title('for 0 delay of first drug ')
    plt.legend()
#     plt.show()
    
    
    plt.subplot(133)
    plt.hist(simulationTwoDrugsVirusPopulations(0,0,True), bins, histtype='bar', rwidth=0.8 , alpha=0.4 ,color ='b', label = ' given after 0 timesteps')
    plt.xlabel('virus amount')
    plt.ylabel('patient amount')
    plt.title('for 0 delay of first drug ')
    plt.legend()
    plt.show()
    
    
    plt.figure('simulation 2 drug delayed treatment ')
    plt.subplot(131)
#     plt.hist(simulationTwoDrugsVirusPopulations(75,300,True), bins, histtype='bar', rwidth=0.8 ,alpha=0.3 , color ='c' , label = 'given at 300 timesteps')
    plt.hist(simulationTwoDrugsVirusPopulations(75,225,True), bins, histtype='bar', rwidth=0.8 ,alpha=0.3 ,color ='r', label = ' given after 150 timesteps')
    plt.xlabel('virus amount')
    plt.ylabel('patient amount')
    plt.title('for 75 delay of first drug ')
    plt.legend()    
    
    plt.subplot(132)
    plt.hist(simulationTwoDrugsVirusPopulations(75,140,True), bins, histtype='bar', rwidth=0.8 ,alpha=0.5 ,color ='y', label = ' given after 75 timesteps')
    plt.xlabel('virus amount')
    plt.ylabel('patient amount')
    plt.title('for 75 delay of first drug ')
    plt.legend()    
    
    
    plt.subplot(133)
    plt.hist(simulationTwoDrugsVirusPopulations(75,75,True), bins, histtype='bar', rwidth=0.8 , alpha=0.4 ,color ='b', label = ' given after 0 timesteps')
    plt.xlabel('virus amount')
    plt.ylabel('patient amount')
    plt.title('for 75 delay of first drug ')
    plt.legend()
    plt.show()
# 

    plt.figure('simulation 2 drug delayed treatment ')
    plt.subplot(131)
#     plt.hist(simulationTwoDrugsVirusPopulations(0,300,True), bins, histtype='bar', rwidth=0.8 ,alpha=0.3 , color ='c' , label = 'given at 300 timesteps')
    plt.hist(simulationTwoDrugsVirusPopulations(150,300,True), bins, histtype='bar', rwidth=0.8 ,alpha=0.3 ,color ='r', label = ' given after 150 timesteps')
    plt.xlabel('virus amount')
    plt.ylabel('patient amount')
    plt.title('for 150 delay of first drug ')
    plt.legend()
    
    plt.subplot(132)
    plt.hist(simulationTwoDrugsVirusPopulations(150,225,True), bins, histtype='bar', rwidth=0.8 ,alpha=0.5 ,color ='y', label = ' given after 75 timesteps')
    plt.xlabel('virus amount')
    plt.ylabel('patient amount')
    plt.title('for 150 delay of first drug ')
    plt.legend()
        
    plt.subplot(133)
    plt.hist(simulationTwoDrugsVirusPopulations(150,150,True), bins, histtype='bar', rwidth=0.8 , alpha=0.4 ,color ='b', label = ' given after 0 timesteps')
    plt.xlabel('virus amount')
    plt.ylabel('patient amount')
    plt.title('for 150 delay of first drug ')
    plt.legend()
    plt.show()
    # TODO
    
simulationWithDrug()
simulationTwoDrugsVirusPopulations()
 
simulationDelayedTreatment()
simulationTwoDrugsDelayedTreatment()