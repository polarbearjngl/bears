import allure
import pytest
from hamcrest import assert_that, has_properties, equal_to, contains_string

from tests.constants import BearType, ResultMsgs
from utils.Utils import Utils


class TestDeleteInfo(object):

    @pytest.mark.parametrize(
        'bear_name, bear_type, bear_age, bear_id_to_delete',
        [
            pytest.param('Tedd', BearType.BLACK.value, 0, None),
            pytest.param('Tedd', BearType.BLACK.value, 0, -1),
        ])
    def test_delete(self, test_api, create_bear, bear_name, bear_type, bear_age, bear_id_to_delete):
        """test delete one bear."""
        with allure.step("Get all bears before delete"):
            all_bears_before = test_api.get_bears()

        with allure.step("Create new bear"):
            new_bear = create_bear(bear_name=bear_name,
                                   bear_type=bear_type,
                                   bear_age=bear_age)

        with allure.step("Get exist bear by id"):
            exist_bear = test_api.get_bear(bear_id=new_bear.bear_id)

        with allure.step("Check that exist bear equal to expected"):
            assert_that(exist_bear,
                        has_properties(bear_id=new_bear.bear_id,
                                       bear_type=new_bear.bear_type,
                                       bear_name=new_bear.name,
                                       bear_age=new_bear.age),
                        'Exist bear not equal to expected')

        with allure.step("Delete bear"):
            delete_bear = test_api.delete_bear(
                bear_id=new_bear.bear_id if bear_id_to_delete is None else bear_id_to_delete)
            assert_that(delete_bear, equal_to(ResultMsgs.OK), 'Delete was not successful')

        if bear_id_to_delete is None:
            with allure.step("Get deleted bear"):
                try:
                    test_api.get_bear(bear_id=new_bear.bear_id)
                    raise AssertionError('Api returns bear with id that not exists')
                except AssertionError as error:
                    assert_that(str(error), contains_string(ResultMsgs.EMPTY))
        else:
            with allure.step("Get exist bear by id"):
                exist_bear_after_delete = test_api.get_bear(bear_id=new_bear.bear_id)

            with allure.step("Check that exist bear equal to expected"):
                assert_that(exist_bear_after_delete,
                            has_properties(bear_id=new_bear.bear_id,
                                           bear_type=new_bear.bear_type,
                                           bear_name=new_bear.name,
                                           bear_age=new_bear.age),
                            'Exist bear not equal to expected')

        with allure.step("Get all bears after delete"):
            all_bears_after = test_api.get_bears()

        with allure.step("Check that new bear is present in DB"):
            if bear_id_to_delete is None:
                assert_that(len(all_bears_before), equal_to(len(all_bears_after)),
                            'Number of bears not equal to expected')
            else:
                assert_that(len(all_bears_before) + 1, equal_to(len(all_bears_after)),
                            'Number of bears not equal to expected')

    @pytest.mark.parametrize(
        'bear_name, bear_type, bears_count',
        [
            pytest.param('Tedd', BearType.BLACK.value, 10),
        ])
    def test_delete_all(self, test_api, create_bear, bear_name, bear_type, bears_count):
        """test delete all bears."""
        for _ in range(bears_count):
            with allure.step("Create new bear"):
                create_bear(bear_name=bear_name,
                            bear_type=bear_type,
                            bear_age=Utils.get_random_int())

        with allure.step("Get all bears before delete"):
            all_bears_before = test_api.get_bears()

        with allure.step("Delete bears"):
            delete_bears = test_api.delete_all_bears()
            assert_that(delete_bears, equal_to(ResultMsgs.OK), 'Delete was not successful')

        with allure.step("Get all bears after delete"):
            all_bears_after = test_api.get_bears()

        with allure.step("Check that new bear is present in DB"):
            assert_that(len(all_bears_before) - bears_count, equal_to(len(all_bears_after)),
                        'Number of bears not equal to expected')
