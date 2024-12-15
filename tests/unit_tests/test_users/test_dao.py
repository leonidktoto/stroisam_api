from app.users.dao import UsersDAO


async def test_add_and_get_users():
    new_user = await UsersDAO.add_data(
        first_name="Денис", 
        last_name="Денисов", 
        phone="9270000001", 
        email="denis@mail.ru"
    )


    new_user = await UsersDAO.find_one_or_none(id=new_user["id"])
    print(new_user)
    assert new_user is not None


