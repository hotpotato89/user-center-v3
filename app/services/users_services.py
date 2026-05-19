import asyncpg

from app.schemas.common import ReturnForm

from app.schemas.users_schemas import UserDataForm, PasswordForm, DeleteUserForm

from app.core.config import settings

async def get_users_service(pool: asyncpg.Pool, limit: int, skip: int):
    async with pool.acquire() as conn:
        data = await conn.fetch('select * from users order by reg_time desc offset $1 limit $2', skip, limit)
        total = await conn.fetchval('select count(*) from users')
    current_page = (skip // limit) + 1 if limit>0 else 1
    total_pages = (total + limit - 1) // limit if limit > 0 else 1
    if not data:
        return ReturnForm(success=False, message='База данных пуста', error_code='empty')
    return ReturnForm(success=True, message=f'Найдено {len(data)} пользователей.', data=[dict(row) for row in data], total=total, page=current_page, total_pages=total_pages, limit=limit)

async def add_user_service(pool, user_data: UserDataForm):
    async with pool.acquire() as session:
        try:
            user_id = await session.fetchval('insert into users (name, age, email) values ($1, $2, $3) returning id', user_data.name, user_data.age, user_data.email)
            return ReturnForm(success=True, message=f'Пользователь успешно добавлен', id=user_id)
        except asyncpg.UniqueViolationError:
            return ReturnForm(success=False, message=f'Пользователь с email \'{user_data.email}\' уже существует', error_code='conflict')
        except Exception as e:
            return ReturnForm(success=False, message='Ошибка на стороне сервера')
        
async def clear_all_service(pool, password: PasswordForm):
    if password.password != settings.admin_password:
        return ReturnForm(success=False, message='Неверный админ-пароль', error_code='unauthorized')
    async with pool.acquire() as session:
        deleted = await session.fetchval('select count(*) from users')
        await session.execute('truncate users restart identity')
    return ReturnForm(success=True, message=f'Удалено {deleted} записей.')

async def delete_user_service(pool, user_data: DeleteUserForm):
    if user_data.password != settings.admin_password:
        return ReturnForm(success=False, message='Неверный админ-пароль', error_code='unauthorized')
    async with pool.acquire() as session:
        try:
            deleted_data = await session.fetch('delete from users where id=$1 returning *', user_data.id)
            if not deleted_data:
                return ReturnForm(success=False, message='Нет такого пользователя', error_code='unknown_user')
        except Exception as e:
            return ReturnForm(success=False, message='Ошибка внутри сервера', error_code='server_error')
    return ReturnForm(success=True, message=f'Удален пользователь под айди {user_data.id}', data=[dict(row) for row in deleted_data])

