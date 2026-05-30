import io
from typing import Optional

from src.enums import Config, TestStatus
from src.consts import SEPERATOR_LENGTH, SEPERATOR_SYMBOL

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

    def __str__(self) -> str:
        return '\n'.join(filter(lambda l: l != str(), self.get_boxed_information))
                            
    def __repr__(self) -> str:
        raise NotImplementedError
    
    # def entry_msg(self):
    #     return self.get_and_format_detail(status=self.entry_status)

    # def exit_msg(self):
    #     return self.get_and_format_detail(status=self.status, detail=self.detail)

    @property
    def get_boxed_information(self) -> list[str]:
        return [self.get_and_format_detail(status=self.entry_status),
                self.redirected_output.getvalue(), 
                self.exception_trace,
                self.get_and_format_detail(status=self.status, detail=self.detail)]
    
    @property
    def seperator(self) -> str:
        return '%s%s%s%s' % (Config.NEGATIVE.value, Config.CYAN.value, SEPERATOR_LENGTH*SEPERATOR_SYMBOL, Config.RESET.value, )
    
    def get_and_format_detail(self,
                              status: TestStatus,
                              detail: Optional[str] = None,
                              indent: Optional[int] = None,) -> str:

        if not indent:
            indent = 2
        
        if not detail:
            detail = ''


        match status:

            case TestStatus.SUCCESS:
                s_msg = '%s--------- [PASS] ---------%s' % (Config.GREEN.value, Config.RESET.value, )

                return '\n'.join([s_msg, self.seperator])
            
            case TestStatus.FAIL:

                match len(detail):
                    case 0:
                        s_msg = '%s*** EXCEPTION DURING TEST ***%s' % (Config.RED.value, Config.RESET.value, )
                    case _:
                        s_msg = '%s*** EXCEPTION DURING TEST <%s> ***%s' % (Config.RED.value, detail, Config.RESET.value, )
                        
                e_msg = ('%s------ [FAIL] ------%s' 
                        % (Config.RED.value, Config.RESET.value))
                
                return '\n'.join([s_msg, e_msg, self.seperator])


            case TestStatus.SET_UP_ENTRY:
                return '%s[*] Set up started%s' % (Config.BLUE.value, Config.RESET.value, )
            
            case TestStatus.SET_UP_SUCCESS:
                return '%s[*] Set up succeeded%s' % (Config.BLUE.value, Config.RESET.value, )
            
            case TestStatus.SET_UP_FAIL:

                s_msg = '%s[*] Skipping test since set up failed.Reason: %s%s' % (Config.YELLOW.value, detail, Config.RESET.value, )
            
                e_msg = '%s------ [SET UP FAILED] ------%s' % (Config.YELLOW.value, Config.RESET.value, )
                
                return '\n'.join([s_msg, e_msg])
        

            case TestStatus.BREAK_DOWN_ENTRY:
                return '%s[*] Break down started%s' % (Config.BLUE.value, Config.RESET.value, )
            
            case TestStatus.BREAK_DOWN_SUCCESS:
                return '%s[*] Break down succeeded%s' % (Config.BLUE.value, Config.RESET.value, )
            
            case TestStatus.BREAK_DOWN_FAIL:
                s_msg = '%s[*] Cleaning up failed.Reason: %s%s' % (Config.YELLOW.value, detail, Config.RESET.value, )
                
                e_msg = '%s------ [BREAK DOWN FAILED] ------%s' % (Config.YELLOW.value, Config.RESET.value, )
                
                return '\n'.join([s_msg, e_msg])


            case TestStatus.ATTEMPT_BREAK_DOWN_ENTRY_FROM_SETUP_FAIL:
                return '%s[*] Break down started after failed setup%s' % (Config.MAGENTA.value, Config.RESET.value, )
            
            case TestStatus.ATTEMPT_BREAK_DOWN_ENTRY_FROM_FAIL:
                return '%s[*] Break down started after failed test%s' % (Config.MAGENTA.value, Config.RESET.value, )
            
            case TestStatus.ATTEMPT_BREAK_DOWN_SUCCESS:
                return '%s[*] Break down succeeded after failed test%s' % (Config.MAGENTA.value, Config.RESET.value, )
            
            case TestStatus.ATTEMPT_BREAK_DOWN_FAIL:
                s_msg = '%s[*] Test failed and attempting Cleaning up failed.Reason: %s%s' % (Config.MAGENTA.value, detail, Config.RESET.value, )

                e_msg = '%s------ [ATTEMPT BREAK DOWN FAILED] ------%s' % (Config.YELLOW.value, Config.RESET.value, )
                
                return '\n'.join([s_msg, e_msg])

            case TestStatus.NO_OP:
                return ''
