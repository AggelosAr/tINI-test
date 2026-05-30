import io
from typing import Optional

from src.enums import Config, TestStatus
from src.consts import SEPERATOR_LENGTH, SEPERATOR_SYMBOL


# TODO maybe move seperator at NO_OP? is this possible?
# TODO something smells fishy with the NO_OPs -> investigate
class OperationState:

    def __init__(self, 
                 status: TestStatus,
                 entry_status: Optional[TestStatus] = None,
                 redirected_output: Optional[io.StringIO] = None,
                 detail: Optional[str] = None,
                 exception_trace: Optional[str] = None):
        
        if not entry_status:
            entry_status = TestStatus.NO_OP
        
        if not redirected_output:
            redirected_output = io.StringIO('')

        if not detail:
            detail = ''

        if not exception_trace:
            exception_trace = ''

        self.entry_status = entry_status

        self.redirected_output = redirected_output

        self.exception_trace = exception_trace

        self.status = status
        self.detail = detail

        self._entry_msg = self.get_and_format_detail(status=self.entry_status)
        self._exit_msg = self.get_and_format_detail(status=self.status, detail=self.detail)

    def __str__(self) -> str:
        return '\n'.join(self.get_boxed_information())
                            
    def __repr__(self) -> str:
        raise NotImplementedError

    @classmethod
    def get_seperator(cls) -> list[str]:
        return ['%s%s%s%s' % (Config.NEGATIVE.value, Config.CYAN.value, SEPERATOR_LENGTH*SEPERATOR_SYMBOL, Config.RESET.value, )]
    
    @property
    def entry_msg(self) -> list[str]:
        return self._entry_msg

    @entry_msg.setter
    def entry_msg(self, new_msg: list[str]) -> None:
        self._entry_msg = new_msg

    @property
    def exit_msg(self) -> list[str]:
        return self._exit_msg

    @exit_msg.setter
    def exit_msg(self, new_msg: list[str]) -> None:
        self._exit_msg = new_msg
    
    # TODO use map here 
    def get_boxed_information(self) -> list[list[str]]:
        box = ['\n'.join(filter(lambda l: l != [''], self.entry_msg)),
               '\n'.join(filter(lambda l: l != [''], [self.redirected_output.getvalue()])), 
               '\n'.join(filter(lambda l: l != [''], [self.exception_trace])),
               '\n'.join(filter(lambda l: l != [''], self.exit_msg))]
        return box

    # TODO move the messages @ state_messages.py
    def get_and_format_detail(self,
                              status: TestStatus,
                              detail: Optional[str] = None) -> list[str]:

        if not detail:
            detail = ''

        match status:

            case TestStatus.SUCCESS:
                s_msg = '%s--------- [PASS] ---------%s' % (Config.GREEN.value, Config.RESET.value, )

                return [s_msg]
            
            case TestStatus.FAIL:

                match len(detail):
                    case 0:
                        s_msg = '%s*** EXCEPTION DURING TEST ***%s' % (Config.RED.value, Config.RESET.value, )
                    case _:
                        s_msg = '%s*** EXCEPTION DURING TEST <%s> ***%s' % (Config.RED.value, detail, Config.RESET.value, )
                        
                e_msg = '%s------ [FAIL] ------%s' % (Config.RED.value, Config.RESET.value, )
                
                return [s_msg, e_msg]


            case TestStatus.SET_UP_ENTRY:
                return ['%s[*] Set up started%s' % (Config.BLUE.value, Config.RESET.value, )]
            
            case TestStatus.SET_UP_SUCCESS:
                return ['%s[*] Set up succeeded%s' % (Config.BLUE.value, Config.RESET.value, )]
            
            case TestStatus.SET_UP_FAIL:

                s_msg = '%s[*] Skipping test since set up failed.Reason: %s%s' % (Config.YELLOW.value, detail, Config.RESET.value, )
            
                e_msg = '%s------ [SET UP FAILED] ------%s' % (Config.YELLOW.value, Config.RESET.value, )
                
                return [s_msg, e_msg]
        

            case TestStatus.BREAK_DOWN_ENTRY:
                return ['%s[*] Break down started%s' % (Config.BLUE.value, Config.RESET.value, )]
            
            case TestStatus.BREAK_DOWN_SUCCESS:
                return ['%s[*] Break down succeeded%s' % (Config.BLUE.value, Config.RESET.value, )]
            
            case TestStatus.BREAK_DOWN_FAIL:
                s_msg = '%s[*] Cleaning up failed.Reason: %s%s' % (Config.YELLOW.value, detail, Config.RESET.value, )
                
                e_msg = '%s------ [BREAK DOWN FAILED] ------%s' % (Config.YELLOW.value, Config.RESET.value, )
                
                return [s_msg, e_msg]


            case TestStatus.ATTEMPT_BREAK_DOWN_ENTRY_FROM_SETUP_FAIL:
                return ['%s[*] Break down started after failed setup%s' % (Config.MAGENTA.value, Config.RESET.value, )]
            
            case TestStatus.ATTEMPT_BREAK_DOWN_ENTRY_FROM_FAIL:
                return ['%s[*] Break down started after failed test%s' % (Config.MAGENTA.value, Config.RESET.value, )]
            
            case TestStatus.ATTEMPT_BREAK_DOWN_SUCCESS:
                return ['%s[*] Break down succeeded after failed test%s' % (Config.MAGENTA.value, Config.RESET.value, )]
            
            case TestStatus.ATTEMPT_BREAK_DOWN_FAIL:
                s_msg = '%s[*] Test failed and attempting Cleaning up failed.Reason: %s%s' % (Config.MAGENTA.value, detail, Config.RESET.value, )

                e_msg = '%s------ [ATTEMPT BREAK DOWN FAILED] ------%s' % (Config.YELLOW.value, Config.RESET.value, )
                
                return [s_msg, e_msg]

            case TestStatus.NO_OP:
                return ['']
