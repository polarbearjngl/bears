import allure
import pytest
from hamcrest import has_properties, assert_that, contains_string

from tests.constants import BearType, ResultMsgs


class TestCreateInfo(object):

    @pytest.mark.parametrize(
        'bear_name, bear_type, bear_age',
        [
            pytest.param('Tedd', BearType.BLACK.value, 0),
            pytest.param('tedd', BearType.BLACK.value, 0),
            pytest.param('ИмяМедведя', BearType.BLACK.value, 0),
            pytest.param('медведь123', BearType.BLACK.value, 0),
            pytest.param('Tedd', BearType.BROWN.value, 0),
            pytest.param('Tedd', BearType.POLAR.value, 0),
            pytest.param('Tedd', BearType.GUMMY.value, 0),
            pytest.param('Tedd', BearType.BLACK.value, 1),
            pytest.param('Tedd', BearType.BLACK.value, 49.5),
            pytest.param('Tedd', BearType.BLACK.value, 100),
            pytest.param('Tedd', BearType.BLACK.value, '0.1'),
            pytest.param('Tedd', BearType.BLACK.value, '1.7'),
            pytest.param('Tedd', BearType.BLACK.value, '99.999')
        ])
    def test_create_bear(self, test_api, create_bear, bear_name, bear_type, bear_age):
        """test create bear."""
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

    @pytest.mark.parametrize(
        'bear_name, bear_type, bear_age, expected_age',
        [
            pytest.param('Tedd', BearType.BLACK.value, -1, 0),
            pytest.param('Tedd', BearType.BLACK.value, 101, 0),
            pytest.param('Tedd', BearType.BLACK.value, 99999.99999, 0),
        ])
    def test_create_bear_unsuccessfully_by_age(
            self, test_api, create_bear, bear_name, bear_type, bear_age, expected_age):
        """test create bear with fault age."""
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
                                       bear_age=expected_age),
                        'Exist bear not equal to expected')

    @pytest.mark.parametrize(
        'bear_name, bear_type, bear_age',
        [
            pytest.param('Tedd', 'NotExistedType', 10),
            pytest.param('Tedd', None, 10),
            pytest.param('Tedd', BearType.BLACK.value, None),
            pytest.param(None, BearType.BLACK.value, 10),
        ])
    def test_create_bear_unsuccessfully_internal_error(self, create_bear, bear_name, bear_type, bear_age):
        """test create bear and get internal server error."""
        with allure.step("Create new bear"):
            try:
                create_bear(bear_name=bear_name,
                            bear_type=bear_type,
                            bear_age=bear_age)
                raise AssertionError('Api creates bear with illegal type')
            except AssertionError as error:
                assert_that(str(error), contains_string(ResultMsgs.INTERNAL_SERVER_ERROR))
