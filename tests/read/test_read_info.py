import allure
from hamcrest import assert_that, less_than, is_not, has_items, has_properties, contains_string

from tests.constants import ResultMsgs
from utils.Utils import Utils


class TestReadInfo(object):

    def test_get_all_bears(self, test_api, create_bear):
        """Test for checking GET all bears."""
        with allure.step("Get all bears before create new"):
            all_bears_before = test_api.get_bears()

        with allure.step("Create new random bear"):
            new_bear = create_bear(bear_name=Utils.get_random_string(),
                                   bear_type=Utils.get_random_bear_type(),
                                   bear_age=Utils.get_random_int())

        with allure.step("Check that new bear is unique"):
            assert_that(all_bears_before,
                        is_not(has_items(has_properties(bear_id=new_bear.bear_id,
                                                        bear_type=new_bear.bear_type,
                                                        bear_name=new_bear.name,
                                                        bear_age=new_bear.age))),
                        'DB already has info about created bear')

        with allure.step("Get all bears after create new"):
            all_bears_after = test_api.get_bears()

        with allure.step("Check that new bear is present in DB"):
            assert_that(len(all_bears_before), less_than(len(all_bears_after)),
                        'Number of bears not equal to expected')

            assert_that(all_bears_after,
                        has_items(has_properties(bear_id=new_bear.bear_id,
                                                 bear_type=new_bear.bear_type,
                                                 bear_name=new_bear.name,
                                                 bear_age=new_bear.age)),
                        'No info about created bear in DB')

    def test_get_exist_bear(self, test_api, create_bear):
        """test get existed bear by id."""
        with allure.step("Create new bear"):
            new_bear = create_bear(bear_name=Utils.get_random_string(),
                                   bear_type=Utils.get_random_bear_type(),
                                   bear_age=Utils.get_random_int())

        with allure.step("Get exist bear by id"):
            exist_bear = test_api.get_bear(bear_id=new_bear.bear_id)

        with allure.step("Check that exist bear equal to expected"):
            assert_that(exist_bear,
                        has_properties(bear_id=new_bear.bear_id,
                                       bear_type=new_bear.bear_type,
                                       bear_name=new_bear.name,
                                       bear_age=new_bear.age),
                        'Exist bear not equal to expected')

    def test_get_not_existed_bear(self, test_api):
        """Get bear with not existed id."""
        with allure.step("Get all bears"):
            all_bears = test_api.get_bears()

        with allure.step("Get not existed bear by id"):
            if len(all_bears) > 0:
                not_exist_id = max([bear.bear_id for bear in all_bears]) + 1
            else:
                not_exist_id = 1

            try:
                test_api.get_bear(bear_id=not_exist_id)
                raise AssertionError('Api returns bear with id that not exists')
            except AssertionError as error:
                assert_that(str(error), contains_string(ResultMsgs.EMPTY))
