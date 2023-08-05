from http import HTTPStatus
from typing import Callable
from scintillant.apimodels.types import SkillRequest, SkillResponse


class ContextUpdater:
    states = {}  # state_name: state_func
    exit_phrases = ['exit', 'quit', 'end']

    def __init__(self, data: SkillRequest):
        # Default parameters for find state and complete it
        self.data = data
        self.context = data.context
        self.response = SkillResponse(status=HTTPStatus.OK)

    @property
    def next_state(self):
        return self.context['state']

    @next_state.setter
    def next_state(self, func: Callable):
        if func:
            self.context['state'] = func.__name__
        else:
            self.context.pop('state')

    def execute_state(self):
        # Termination of the skill if the user has asked for it
        if self.data.message.text in self.exit_phrases:
            self.response.status = 'exit'
        # In case the user has just entered the skill,
        # we call the _initial_state_ function.
        elif 'state' not in self.context:
            self._initial_state_()
        # In case the user already has a state.
        else:
            state = self.context.get('state')
            if state not in self.states:
                raise Exception(f"State {state} not registered!")
            else:
                self.states[state](self)

    def get_response(self) -> SkillResponse:
        self.execute_state()
        self.response.context = self.context
        return self.response

    def _initial_state_(self):
        """Execute when state is None"""
        self.response.text = (
            "Welcome to Scintillant v2.0! \n"
            "This message generated from default scintillant initial state. "
            "Create your own _initial_state_ function on context controller to "
            "override it."
        )

    @classmethod
    def statefunc(cls, func):
        cls.states[func.__name__] = func

        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        wrapper.__name__ = func.__name__

        return wrapper
