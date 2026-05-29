import io
from typing import Optional

from src.enums import Config, TestStatus


# TODO optimize ...
class OperationState:

    def __init__(self, 
                 status: TestStatus,
                 entry_status: Optional[TestStatus] = TestStatus.NO_OP,
                 redirected_output: Optional[io.StringIO] = io.StringIO(''),
                 detail: Optional[str] = '',
                 exception_trace: Optional[str] = ''):
        
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
                              indent: Optional[int] = 2,
                              detail: Optional[str] = '') -> str:

        pad = (lambda lvl: '\t'*lvl)(indent) # type: ignore[operator]

        match status:

            case TestStatus.SUCCESS:
                s_msg = '\n%s%s--------- [PASS] ---------%s' % (pad, Config.GREEN.value, Config.RESET.value)

                return '\n'.join([s_msg, self.seperator])
            
            case TestStatus.FAIL:
                
                match len(detail):
                    case 0:
                        s_msg = ('%s%s*** EXCEPTION DURING TEST ***%s' 
                                % ( pad, Config.RED.value, Config.RESET.value, ))
                    case _:
                        s_msg = ('%s%s*** EXCEPTION DURING TEST <%s> ***%s' 
                                % ( pad, Config.RED.value, detail, Config.RESET.value, ))
                        
                e_msg = ('\n%s%s------ [FAIL] ------%s' 
                        % (pad, Config.RED.value, Config.RESET.value))
                
                return '\n'.join([s_msg, e_msg, self.seperator])
        

            case TestStatus.SET_UP_ENTRY:
                return '%s%s[*] Set up started%s\n' % (pad, Config.BLUE.value, Config.RESET.value)
            
            case TestStatus.SET_UP_SUCCESS:
                return '%s%s[*] Set up succeeded%s\n' % (pad, Config.BLUE.value, Config.RESET.value)
            
            case TestStatus.SET_UP_FAIL:

                s_msg = ('%s%s[*] Skipping test since set up failed.\n\t%sReason: %s%s' 
                        % (pad, Config.YELLOW.value, pad, detail, Config.RESET.value, ))
            
                e_msg = '\n%s%s------ [SET UP FAILED] ------%s\n' % (pad, Config.YELLOW.value, Config.RESET.value)
                
                return '\n'.join([s_msg, e_msg])
        

            case TestStatus.BREAK_DOWN_ENTRY:
                return '%s%s[*] Break down started%s\n' % (pad, Config.BLUE.value, Config.RESET.value)
            
            case TestStatus.BREAK_DOWN_SUCCESS:
                return '%s%s[*] Break down succeeded%s' % (pad, Config.BLUE.value, Config.RESET.value)
            
            case TestStatus.BREAK_DOWN_FAIL:
                s_msg = ('%s%s[*] Cleaning up failed.\n\t%sReason: %s%s' % 
                        (pad, Config.YELLOW.value, pad, detail, Config.RESET.value, ))
                
                e_msg = '\n%s%s------ [BREAK DOWN FAILED] ------%s\n' % (pad, Config.YELLOW.value, Config.RESET.value)
                
                return '\n'.join([s_msg, e_msg])

            case TestStatus.NO_OP:
                # TODO 
                # return 'XXXXXXX NO_OP XXXXXXX'
                return ''
