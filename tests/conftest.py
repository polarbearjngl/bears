import pytest
from hamcrest import assert_that, equal_to

from api.bears_api import BearsApi
from tests.constants import ApiConsts, ResultMsgs


@pytest.fixture(scope='session')
def test_api():
    """Bears api."""
    alaska_api = BearsApi(host=ApiConsts.HOST, is_logger_enabled=False)
    yield alaska_api


@pytest.fixture(scope='function')
def create_bear(test_api):
    """Create new bear."""
    created = []

    def create(**kwargs):
        """Create new bear.

        Kwargs:
            bear_type: Type.
            bear_name: Name.
            bear_age: Age.

        Returns: New bear.

        """
        new_bear = test_api.create_bear(**kwargs)
        created.append(new_bear)
        return new_bear

    yield create

    for bear in created:
        delete_bear = test_api.delete_bear(bear_id=bear.bear_id)
        assert_that(delete_bear, equal_to(ResultMsgs.OK), 'Delete was not successful')
