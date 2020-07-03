from copy import copy

import allure
import pytest
from hamcrest import assert_that, has_properties, equal_to, contains_string

from tests.constants import BearType, ResultMsgs


class TestUpdateInfo(object):

    @pytest.mark.parametrize('start_bear_values',
                             [pytest.param({'bear_name': 'Tedd', 'bear_type': BearType.BLACK.value, 'bear_age': 1})])
    @pytest.mark.parametrize(
        'new_bear_value',
        [
            pytest.param({'bear_name': 'Tedd'}),
            pytest.param({'bear_name': 'TEDD'}),
            pytest.param({'bear_name': '123'}),
            pytest.param({'bear_name': ''}),
            pytest.param({'bear_name': ' '}),
            pytest.param({'bear_name': '\r\n'}),
            pytest.param({'bear_type': BearType.BROWN.value}),
            pytest.param({'bear_type': BearType.POLAR.value}),
            pytest.param({'bear_type': BearType.GUMMY.value}),
            pytest.param({'bear_type': 'TEST'}),
            pytest.param({'bear_age': 11}),
            pytest.param({'bear_age': '11'}),
            pytest.param({'bear_age': 111}),
            pytest.param({'bear_age': -1}),
        ])
    def test_update_value(self, test_api, create_bear, start_bear_values, new_bear_value):
        """test update bear value"""
        with allure.step("Create new bear"):
            new_bear = create_bear(**start_bear_values)

        with allure.step("Get exist bear by id"):
            exist_bear = test_api.get_bear(bear_id=new_bear.bear_id)

        with allure.step("Check that exist bear equal to expected"):
            assert_that(exist_bear,
                        has_properties(bear_id=new_bear.bear_id,
                                       bear_type=new_bear.bear_type,
                                       bear_name=new_bear.name,
                                       bear_age=new_bear.age),
                        'Exist bear not equal to expected')

        with allure.step("Update created bear"):
            new_bear_values = copy(start_bear_values)
            new_bear_values.update(new_bear_value)
            update_bear = test_api.update_bear(bear_id=new_bear.bear_id,
                                               **new_bear_values)

            assert_that(update_bear, equal_to(ResultMsgs.OK), 'update was not successful')

        with allure.step("Get exist bear by id"):
            exist_bear_after_update = test_api.get_bear(bear_id=new_bear.bear_id)

        with allure.step("Check that exist bear equal to expected"):
            assert_that(exist_bear_after_update,
                        has_properties(bear_id=new_bear.bear_id,
                                       **new_bear_values),
                        'Exist bear not equal to expected')

    @pytest.mark.parametrize('start_bear_values',
                             [pytest.param({'bear_name': 'Tedd', 'bear_type': BearType.BLACK.value, 'bear_age': 1})])
    @pytest.mark.parametrize(
        'new_bear_value',
        [
            pytest.param({'bear_name': None}),
            pytest.param({'bear_type': None}),
            pytest.param({'bear_age': None}),
        ])
    def test_update_null_values(self, test_api, create_bear, start_bear_values, new_bear_value):
        """test update bear by request without required pararms"""
        with allure.step("Create new bear"):
            new_bear = create_bear(**start_bear_values)

        with allure.step("Get exist bear by id"):
            exist_bear = test_api.get_bear(bear_id=new_bear.bear_id)

        with allure.step("Check that exist bear equal to expected"):
            assert_that(exist_bear,
                        has_properties(bear_id=new_bear.bear_id,
                                       bear_type=new_bear.bear_type,
                                       bear_name=new_bear.name,
                                       bear_age=new_bear.age),
                        'Exist bear not equal to expected')

        with allure.step("Update created bear"):
            new_bear_values = copy(start_bear_values)
            new_bear_values.update(new_bear_value)
            try:
                test_api.update_bear(bear_id=new_bear.bear_id,
                                     **new_bear_values)
                raise AssertionError('Api update bear by request without required pararms')
            except AssertionError as error:
                assert_that(str(error), contains_string(ResultMsgs.INTERNAL_SERVER_ERROR))