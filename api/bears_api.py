from collections import OrderedDict

import allure

from api.base_api import BaseApi
from models.bear import Bear
from tests.constants import ApiConsts


class BearsApi(BaseApi):

    def __init__(self, host, is_logger_enabled):
        """Base api class for bears.

        Args:
            host: host for sending requests.
            is_logger_enabled: Flag for enable logger.
        """
        super().__init__(host, is_logger_enabled)

    def get_bears(self):
        """GET /bear - read all bears.

        Returns: List of all bears.

        """
        with allure.step("Get all bears"):
            content = self._request(method='GET',
                                    url=self.host + ApiConsts.GET_ALL_BEARS)
            bears = [Bear(**bear) for bear in content]
            return bears

    def get_bear(self, bear_id):
        """Get Bear by id.

        Args:
            bear_id: ID of bear to get.

        Returns: Bear by id or empty Bear object.

        """
        with allure.step("Get bear with id {}".format(str(bear_id))):
            content = self._request(method='GET',
                                    url=self.host + ApiConsts.GET_BEAR.format(id=bear_id))
            return Bear(**content) if content is not None else Bear()

    def create_bear(self, **kwargs):
        """POST /bear - create.

        Kwargs:
            bear_type: Type.
            bear_name: Name.
            bear_age: Age.

        Returns: Created bear.

        """
        with allure.step("Create new bear"):
            json = OrderedDict([
                ('bear_type', kwargs.get('bear_type')),
                ('bear_name', kwargs.get('bear_name')),
                ('bear_age', kwargs.get('bear_age'))
            ])
            new_bear_id = self._request(method='POST',
                                        url=self.host + ApiConsts.CREATE_NEW_BEAR,
                                        json=json)
            new_bear = Bear(bear_id=new_bear_id, **kwargs)
            return new_bear

    def delete_bear(self, bear_id):
        """DELETE /bear/:id - delete specific bear.

        Args:
            bear_id: ID of bear that will be deleted.

        Returns: result msg.

        """
        with allure.step("Delete bear with id {}".format(str(bear_id))):
            content = self._request(method='DELETE',
                                    url=self.host + ApiConsts.DELETE_BEAR.format(id=bear_id),
                                    is_decode_to_json=False)
            return content.text

    def delete_all_bears(self):
        """DELETE /bear - delete all bears DELETE."""
        with allure.step("Delete all bears"):
            content = self._request(method='DELETE',
                                    url=self.host + ApiConsts.DELETE_ALL_BEARS,
                                    is_decode_to_json=False)
            return content.text

    def update_bear(self, bear_id, **kwargs):
        """PUT /bear/:id - update specific bear.

        Kwargs:
            bear_type: Type.
            bear_name: Name.
            bear_age: Age.

        Returns:

        """
        with allure.step("Update bear"):
            json = OrderedDict([
                ('bear_type', kwargs.get('bear_type')),
                ('bear_name', kwargs.get('bear_name')),
                ('bear_age', kwargs.get('bear_age'))
            ])
            content = self._request(method='PUT',
                                    url=self.host + ApiConsts.UPDATE_BEAR.format(id=bear_id),
                                    json=json,
                                    is_decode_to_json=False)
            return content.text
