import io
from typing import Optional

from src.enums import Config, TestStatus


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
    
    @property
    def get_boxed_information(self) -> list[str]:
        return [self.get_and_format_detail(status=self.entry_status),
                self.redirected_output.getvalue(), 
                self.exception_trace,
                self.get_and_format_detail(status=self.status, detail=self.detail)]
    
    @property
    def seperator(self) -> str:
        return '\n%s%s%s%s\n' % (Config.NEGATIVE.value, Config.CYAN.value, 120*'=', Config.RESET.value, )
    
    def get_and_format_detail(self,
                              status: TestStatus,
                              detail: Optional[str] = None,
                              indent: Optional[int] = None,) -> str:

        if not indent:
            indent = 2
        
        if not detail:
            detail = ''

        pad = (lambda lvl: '\t'*lvl)(indent)

        match status:

            case TestStatus.SUCCESS:
                s_msg = '\n%s%s--------- [PASS] ---------%s' % (pad, Config.GREEN.value, Config.RESET.value)

                return '\n'.join([s_msg, self.seperator])
            
            case TestStatus.FAIL:

                match len(detail):
                    case 0:
                        s_msg = '\n%s%s*** EXCEPTION DURING TEST ***%s' % ( pad, Config.RED.value, Config.RESET.value, )
                    case _:
                        s_msg = '\n%s%s*** EXCEPTION DURING TEST <%s> ***%s' % ( pad, Config.RED.value, detail, Config.RESET.value, )
                        
                e_msg = ('\n%s%s------ [FAIL] ------%s' 
                        % (pad, Config.RED.value, Config.RESET.value))
                
                return '\n'.join([s_msg, e_msg, self.seperator])


            case TestStatus.SET_UP_ENTRY:
                return '%s%s[*] Set up started%s\n' % (pad, Config.BLUE.value, Config.RESET.value)
            
            case TestStatus.SET_UP_SUCCESS:
                return '%s%s[*] Set up succeeded%s\n' % (pad, Config.BLUE.value, Config.RESET.value)
            
            case TestStatus.SET_UP_FAIL:

                s_msg = '%s%s[*] Skipping test since set up failed.\n\t%sReason: %s%s' % (pad, Config.YELLOW.value, pad, detail, Config.RESET.value, )
            
                e_msg = '\n%s%s------ [SET UP FAILED] ------%s\n' % (pad, Config.YELLOW.value, Config.RESET.value)
                
                return '\n'.join([s_msg, e_msg])
        

            case TestStatus.BREAK_DOWN_ENTRY:
                return '%s%s[*] Break down started%s\n' % (pad, Config.BLUE.value, Config.RESET.value)
            
            case TestStatus.BREAK_DOWN_SUCCESS:
                return '%s%s[*] Break down succeeded%s' % (pad, Config.BLUE.value, Config.RESET.value)
            
            case TestStatus.BREAK_DOWN_FAIL:
                s_msg = '%s%s[*] Cleaning up failed.\n\t%sReason: %s%s' % (pad, Config.YELLOW.value, pad, detail, Config.RESET.value, )
                
                e_msg = '\n%s%s------ [BREAK DOWN FAILED] ------%s\n' % (pad, Config.YELLOW.value, Config.RESET.value)
                
                return '\n'.join([s_msg, e_msg])


            case TestStatus.ATTEMPT_BREAK_DOWN_ENTRY_FROM_SETUP_FAIL:
                return '%s%s[*] Break down started after failed setup%s\n' % (pad, Config.MAGENTA.value, Config.RESET.value)
            
            case TestStatus.ATTEMPT_BREAK_DOWN_ENTRY_FROM_FAIL:
                return '%s%s[*] Break down started after failed test%s\n' % (pad, Config.MAGENTA.value, Config.RESET.value)
            
            case TestStatus.ATTEMPT_BREAK_DOWN_SUCCESS:
                return '%s%s[*] Break down succeeded after failed test%s' % (pad, Config.MAGENTA.value, Config.RESET.value)
            
            case TestStatus.ATTEMPT_BREAK_DOWN_FAIL:
                s_msg = '%s%s[*] Test failed and attempting Cleaning up failed.\n\t%sReason: %s%s' % (pad, Config.MAGENTA.value, pad, detail, Config.RESET.value, )

                e_msg = '\n%s%s------ [ATTEMPT BREAK DOWN FAILED] ------%s\n' % (pad, Config.YELLOW.value, Config.RESET.value)
                
                return '\n'.join([s_msg, e_msg])

            case TestStatus.NO_OP:
                return ''
