from io import StringIO
from typing import Iterator, Optional

from src._internals.consts import (_RESET, SEPERATOR_CYAN, SEPERATOR_LENGTH,
                                   SEPERATOR_NEGATIVE, SEPERATOR_SYMBOL)
from src.enums import CONFIG, TestStatus


class OperationState:

    def __init__(self, 
                 status: TestStatus,
                 entry_status: Optional[TestStatus] = None,
                 redirected_output: Optional[StringIO] = None,
                 detail: Optional[str] = None,
                 exception_trace: Optional[str] = None):
        
        if not entry_status:
            entry_status = TestStatus.NO_OP
        
        if not redirected_output:
            redirected_output = StringIO('')

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
    def get_end_seperator(cls) -> list[str]:
        return ['%s%s%s%s' % 
                (SEPERATOR_NEGATIVE, 
                 SEPERATOR_CYAN, 
                 SEPERATOR_LENGTH*SEPERATOR_SYMBOL, 
                 _RESET, )]
    
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
    
    def align_message(self, el: str) -> str:
        return '%s%s' % ((SEPERATOR_LENGTH // 2 - (len(el) // 2)) * str(' '), el, )

    # TODO maybe align messages relative to each other also 
    def get_boxed_information(self) -> Iterator[str]:
        return map(lambda l: '\n'.join(l), [map(self.align_message, self.entry_msg),
                                            [self.redirected_output.getvalue()], 
                                            [self.exception_trace],
                                            map(self.align_message, self.exit_msg)])

    def get_and_format_detail(self,
                              status: TestStatus,
                              detail: Optional[str] = None) -> list[str]:

        if not detail:
            detail = ''

        match status:

            case TestStatus.SUCCESS:
                s_msg = '%s--------- [PASS] ---------%s' % (CONFIG.get(status), _RESET, )

                return [s_msg]
            
            case TestStatus.FAIL:

                match len(detail):
                    case 0:
                        s_msg = '%s*** EXCEPTION DURING TEST ***%s' % (CONFIG.get(status), _RESET, )
                        n_msg = ''
                    case _:
                        # TODO (refactor) since detail is not used in any state 
                        # we will take advatage of that to put the MUST_EQUALS messages there.
                        s_msg = '%s*** EXCEPTION DURING TEST ***%s' % (CONFIG.get(status), _RESET, )
                        n_msg = '%s %s %s' % (CONFIG.get(status), detail, _RESET, )
                        
                e_msg = '%s------ [FAIL] ------%s' % (CONFIG.get(status), _RESET, )
                
                return [s_msg, n_msg, e_msg]


            case TestStatus.SET_UP_ENTRY:
                return ['%s[*] Set up started%s' % (CONFIG.get(status), _RESET, )]
            
            case TestStatus.SET_UP_SUCCESS:
                return ['%s[*] Set up succeeded%s' % (CONFIG.get(status), _RESET, )]
            
            case TestStatus.SET_UP_FAIL:

                s_msg = '%s[*] Skipping test since set up failed.Reason: %s%s' % (CONFIG.get(status), detail, _RESET, )
            
                e_msg = '%s------ [SET UP FAILED] ------%s' % (CONFIG.get(status), _RESET, )
                
                return [s_msg, e_msg]
        

            case TestStatus.BREAK_DOWN_ENTRY:
                return ['%s[*] Break down started%s' % (CONFIG.get(status), _RESET, )]
            
            case TestStatus.BREAK_DOWN_SUCCESS:
                return ['%s[*] Break down succeeded%s' % (CONFIG.get(status), _RESET, )]
            
            case TestStatus.BREAK_DOWN_FAIL:
                s_msg = '%s[*] Cleaning up failed.Reason: %s%s' % (CONFIG.get(status), detail, _RESET, )
                
                e_msg = '%s------ [BREAK DOWN FAILED] ------%s' % (CONFIG.get(status), _RESET, )
                
                return [s_msg, e_msg]


            case TestStatus.ATTEMPT_BREAK_DOWN_ENTRY_FROM_SETUP_FAIL:
                return ['%s[*] Break down started after failed setup%s' % (CONFIG.get(status), _RESET, )]
            
            case TestStatus.ATTEMPT_BREAK_DOWN_ENTRY_FROM_FAIL:
                return ['%s[*] Break down started after failed test%s' % (CONFIG.get(status), _RESET, )]
            
            case TestStatus.ATTEMPT_BREAK_DOWN_SUCCESS:
                return ['%s[*] Break down succeeded after failed test%s' % (CONFIG.get(status), _RESET, )]
            
            case TestStatus.ATTEMPT_BREAK_DOWN_FAIL:
                s_msg = '%s[*] Test failed and attempting cleaning up failed.Reason: %s%s' % (CONFIG.get(status), detail, _RESET, )

                e_msg = '%s------ [ATTEMPT BREAK DOWN FAILED] ------%s' % (CONFIG.get(status), _RESET, )
                
                return [s_msg, e_msg]

            case TestStatus.NO_OP:
                return ['XXX']
