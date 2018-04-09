import ParameterClasses as P
import MarkovModelClasses as MarkovCls
import SupportMarkovModel as SupportMarkov
import scr.SamplePathClasses as PathCls
import scr.FigureSupport as Figs


#Q1
print('Part A: No anticoagulation')

# create a cohort
cohort = MarkovCls.Cohort(
    id=0,
    therapy=P.Therapies.OBSERVE)

# simulate the cohort
simOutputs = cohort.simulate()

#print('list of survival times', simOutputs._survivalTimes)
#print('list of number of strokes', simOutputs._list_of_number_of_strokes)

#print('mean life years:', simOutputs.get_sumStat_survival_times().get_mean())
#print('mean number of strokes:', simOutputs.get_sumStat_number_of_Strokes().get_mean())


# graph survival curve
PathCls.graph_sample_path(
    sample_path=simOutputs.get_survival_curve(),
    title='Survival curve (no anticoag)',
    x_label='Simulation time step',
    y_label='Number of alive patients'
    )

# graph histogram of survival times
Figs.graph_histogram(
    data=simOutputs.get_survival_times(),
    title='Survival times of patients (no anticoag)',
    x_label='Survival time (years)',
    y_label='Counts',
    bin_width=1
)

# graph histogram of number of strokes
Figs.graph_histogram(
    data=simOutputs.get_number_of_strokes(),
    title='Number of strokes (no anticoag)',
    x_label='Number of strokes',
    y_label='Counts',
    bin_width=1
)

# print the outcomes of this simulated cohort
SupportMarkov.print_outcomes(simOutputs, 'Observation therapy:')

#Q2
print('Part B: Anticoagulation')

# create a cohort
cohort = MarkovCls.Cohort(
    id=0,
    therapy=P.Therapies.ANTICOAG)

# simulate the cohort
simOutputs = cohort.simulate()

#print('list of survival times', simOutputs._survivalTimes)
#print('list of number of strokes', simOutputs._list_of_number_of_strokes)

#print('mean life years:', simOutputs.get_sumStat_survival_times().get_mean())
#print('mean number of strokes:', simOutputs.get_sumStat_number_of_Strokes().get_mean())


# graph survival curve
PathCls.graph_sample_path(
    sample_path=simOutputs.get_survival_curve(),
    title='Survival curve (with anticoag)',
    x_label='Simulation time step',
    y_label='Number of alive patients'
    )

# graph histogram of survival times
Figs.graph_histogram(
    data=simOutputs.get_survival_times(),
    title='Survival times of patients (with anticoag)',
    x_label='Survival time (years)',
    y_label='Counts',
    bin_width=1
)

# graph histogram of number of strokes
Figs.graph_histogram(
    data=simOutputs.get_number_of_strokes(),
    title='Number of strokes (with anticoag)',
    x_label='Number of strokes',
    y_label='Counts',
    bin_width=1
)

# print the outcomes of this simulated cohort
SupportMarkov.print_outcomes(simOutputs, 'Anticoagulation therapy:')
