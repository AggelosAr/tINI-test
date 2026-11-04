

@consts  V2 const set to True
@consts set python path
for V2 coverage


python -m tini_test -v minimal --coverage --coverage-target src --coverage-store /tmp/coverages/tini_test/.coverage.run_MAIN
python -m tini_test --coverage-merge /tmp/coverages/tini_test/
python -m tini_test --coverage-generate-report --coverage-target src --coverage-store /tmp/coverages/tini_test/.coverage_merged

----


@test_mocking_as_context_manager_maintains_state_of_shared maybe implement

Maybe update how mocking class methods is handled.

Discard stdin/out for minimals?

add docstring to var

Maybe udate isolate to take a snapshot for true isolation

