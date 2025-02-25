import pytest

from app.users.dao import UsersDAO
from app.users.sms_codes.dao import SmsCodesDAO


async def test_add_and_get_users():
    new_user = await UsersDAO.add_data(
        first_name="Денис", last_name="Денисов", phone="9270000001", email="denis@mail.ru"
    )

    new_user = await UsersDAO.find_one_or_none(id=new_user["id"])

    assert new_user is not None


@pytest.mark.parametrize("user_id, expected_sms_code_exists", [(1, True), (9, False)])
async def test_last_sms_code(user_id, expected_sms_code_exists):
    sms_code = await SmsCodesDAO.last_sms_code(user_id=user_id)
    if expected_sms_code_exists:
        assert sms_code is not None
    else:
        assert sms_code is None
