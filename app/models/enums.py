from enum import Enum as PyEnum

class PositionEnum(PyEnum):
    MANAGER = 'manager'
    SUPEROPERATOR = 'superoperator'
    SENIOR = 'senior'
    OPERATOR = 'operator'

class Status(PyEnum):
    EMPLOYED = 'employed'
    FIRED = 'fired'

class Parameter(PyEnum):
    TIME_TO_FIRST_ANSWER = 'time_to_first_answer'
    TIME_TO_NEXT_ANSWER = 'time_to_next_answer'
    COMPETENCE = 'competence'
    POLITENESS = 'politeness'
    ERRORS = 'errors'

class CoefficientType(PyEnum):
    POSITIVE = 'positive'
    NEGATIVE = 'negative'


