from src.enums import Mode
from src.misc.exceptions import (CantFindRelativePathToRoot,
                                 TooManyArgumentsDirAndFile)
from src.module_collector import ModuleCollector
from src.utils import ModuleTests


# TODO implement specific function calling on test

def main():
    

    test_collector = ModuleCollector(search_dir='fake_real_tests/test_module_collector/tests')
   
    test_collector.walk_and_collect_test_files(root=test_collector.root)
    test_collector.normalize_test_modules()


    for module, test_files in test_collector.test_modules.items():

        for test_file in test_files:
            
            # test_fails test_broken_test
            #
            # if 'test_cleanup_works_on_fail' != test_file:
            #     continue


            full_module_name = '%s.%s' % (module, test_file)

            test_module = ModuleTests(module=full_module_name,
                                      mode=Mode.NORMAL)

            test_module.gather_tests()
            test_module.run_tests()


if __name__=='__main__':

    try:
        main()
    except TooManyArgumentsDirAndFile:
        raise
    except CantFindRelativePathToRoot:
        raise

