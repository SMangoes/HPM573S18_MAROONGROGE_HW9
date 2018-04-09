
# simulation settings
POP_SIZE = 2000     # cohort population size
SIM_LENGTH = 50    # length of simulation (years)
ALPHA = 0.05        # significance level for calculating confidence intervals
DISCOUNT = 0.03     # annual discount rate

ADD_BACKGROUND_MORT = False  # if background mortality should be added
DELTA_T = 1       # years

PSA_ON = False      # if probabilistic sensitivity analysis is on


#Probability matrix as given
PROB_MATRIX = [
    [0.75, 0.15, 0,   0.1],  #Starting well
    [0,       0,    1,   0],  #Starting in stroke
    [0,    0.25,  0.55, 0.2], #Post-stroke
    [0,       0,     0,   1]  #Dead
]

#Probability matrix with anti-coag
PROB_MATRIX_anti_coag = [
    [0.75, 0.15, 0,   0.1],  #Starting well
    [0,       0,    1,   0],  #Starting in stroke
    [0,    0.1625,  0.6275, 0.21], #Post-stroke
    [0,       0,     0,   1]  #Dead
]

# annual cost of each health state
ANNUAL_STATE_COST = [
    0,   #Starting well
    5000,   #Starting in stroke
    0,    #Post-stroke
    0]      #Dead

# annual health utility of each health state
ANNUAL_STATE_UTILITY = [
    0.75,   #Starting well
    0.50,   #Starting in stroke
    0.25,    #Post-stroke
    0]      #Dead

# annual drug costs
OBSERVE_COST = 0
ANTICOAG_COST = 2086.0

# treatment relative risk
TREATMENT_RR = 0.509
TREATMENT_RR_CI = 0.365, 0.71  # lower 95% CI, upper 95% CI

# annual probability of background mortality (number per year per 1,000 population)
ANNUAL_PROB_BACKGROUND_MORT = 0

