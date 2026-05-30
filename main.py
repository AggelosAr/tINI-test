
import os
from pathlib import Path

from src.enums import Mode
from src.module_collector import ModuleCollector
from src.utils import ModuleTests



def main():

    test_collector = ModuleCollector()
    test_collector.walk_collect_test_files(root=Path(os.getcwd()))
    test_collector.normalize_test_modules()

    print(test_collector.test_modules)

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
    main()
