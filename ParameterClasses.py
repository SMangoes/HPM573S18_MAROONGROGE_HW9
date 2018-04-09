from enum import Enum
import numpy as np
import scipy.stats as stat
import math as math
import InputData as Data
import scr.MarkovClasses as MarkovCls
import scr.RandomVariantGenerators as Random
import scr.ProbDistParEst as Est


class HealthStats(Enum):
    """ health states of patients with HIV """
    Well = 0
    Stroke = 1
    Post_Stroke = 2
    Dead = 3


class Therapies(Enum):
    """ observe vs. anticoag therapy """
    OBSERVE = 0
    ANTICOAG = 1


class _Parameters:

    def __init__(self, therapy):

        # selected therapy
        self._therapy = therapy

        # simulation time step
        self._delta_t = Data.DELTA_T

        # calculate the adjusted discount rate
        self._adjDiscountRate = Data.DISCOUNT*Data.DELTA_T

        # initial health state
        self._initialHealthState = HealthStats.Well

        # annual treatment cost
        if self._therapy == Therapies.OBSERVE:
            self._annualTreatmentCost = Data.OBSERVE_COST
        else:
            self._annualTreatmentCost = Data.OBSERVE_COST + Data.ANTICOAG_COST

        # transition probability matrix of the selected therapy
        self._prob_matrix = []
        # treatment relative risk
        self._treatmentRR = 0

        # annual state costs and utilities
        self._annualStateCosts = []
        self._annualStateUtilities = []

    def get_initial_health_state(self):
        return self._initialHealthState

    def get_delta_t(self):
        return self._delta_t

    def get_adj_discount_rate(self):
        return self._adjDiscountRate

    def get_transition_prob(self, state):
        return self._prob_matrix[state.value]

    def get_annual_state_cost(self, state):
        if state == HealthStats.Dead:
            return 0
        else:
            return self._annualStateCosts[state.value]

    def get_annual_state_utility(self, state):
        if state == HealthStats.Dead:
            return 0
        else:
            return self._annualStateUtilities[state.value]

    def get_annual_treatment_cost(self):
        return self._annualTreatmentCost


class ParametersFixed(_Parameters):
    def __init__(self, therapy):

        # initialize the base class
        _Parameters.__init__(self, therapy)

        # calculate transition probabilities between states
        self._prob_matrix = Data.PROB_MATRIX

        # update the transition probability matrix if combination therapy is being used
        if self._therapy == Therapies.ANTICOAG:
            self._prob_matrix = Data.PROB_MATRIX_anti_coag

        # annual state costs and utilities
        self._annualStateCosts = Data.ANNUAL_STATE_COST
        self._annualStateUtilities = Data.ANNUAL_STATE_UTILITY


def calculate_prob_matrix():
    """ :returns transition probability matrix for hiv states under mono therapy"""

    # create an empty matrix populated with zeroes
    prob_matrix = []
    for s in HealthStats:
        prob_matrix.append([0] * len(HealthStats))

    # for all health states
    for s in HealthStats:
        # if the current state is death
        if s is HealthStats.Dead:
            # the probability of staying in this state is 1
            prob_matrix[s.value][s.value] = 1
        else:
            # calculate the transition probabilities out of this state
            for j in range(s.value, HealthStats.Dead.value):
                prob_matrix[s.value][j] = Data.PROB_MATRIX[s.value][j]

    return prob_matrix


def add_background_mortality(prob_matrix):

    # find the transition rate matrix
    rate_matrix = MarkovCls.discrete_to_continuous(prob_matrix, 1)
    # add mortality rates
    for s in HealthStats:
        if s not in [HealthStats.Dead]:
            rate_matrix[s.value][HealthStats.Dead.value] \
                = -np.log(1 - Data.ANNUAL_PROB_BACKGROUND_MORT)

    # convert back to transition probability matrix
    prob_matrix[:], p = MarkovCls.continuous_to_discrete(rate_matrix, Data.DELTA_T)
    # print('Upper bound on the probability of two transitions within delta_t:', p)


def calculate_prob_matrix_combo(matrix_mono, combo_rr):
    """
    :param matrix_mono: (list of lists) transition probability matrix under mono therapy
    :param combo_rr: relative risk of the combination treatment
    :returns (list of lists) transition probability matrix under combination therapy """

    # create an empty list of lists
    matrix_combo = []
    for l in matrix_mono:
        matrix_combo.append([0] * len(l))

    # populate the combo matrix
    # first non-diagonal elements
    for s in HealthStats:
        for next_s in range(s.value + 1, len(HealthStats)):
            matrix_combo[s.value][next_s] = combo_rr * matrix_mono[s.value][next_s]

    # diagonal elements are calculated to make sure the sum of each row is 1
    for s in HealthStats:
        if s not in HealthStats.Dead:
            matrix_combo[s.value][s.value] = 1 - sum(matrix_combo[s.value][s.value + 1:])

    return matrix_combo
