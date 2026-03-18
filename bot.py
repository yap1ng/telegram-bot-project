import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()

tasks = []
completed_tasks = []

@dp.message(Command("start"))
async def main_start(message: Message):
    await message.answer(
        f"Добро пожаловать, {message.from_user.first_name}!\nЯ бот-менеджер задач.\nВыбери команду:\n/add - добавить новую задачу\n/tasks - просмотр задач\n/done - отметить задачу выполненной\n/delete - удалить задач\n/stats - статистика"
    )


#добавление
class AddTask(StatesGroup):
    waiting_for_task = State()

@dp.message(Command("add"))
async def add_task(message: Message, state: FSMContext):

    await message.answer("✏️ Напиши задачу:")
    await state.set_state(AddTask.waiting_for_task)

@dp.message(AddTask.waiting_for_task)
async def save_task(message: Message, state: FSMContext):

    task = message.text

    tasks.append(task)

    await message.answer("✅ Задача добавлена!")

    await state.clear()



#задачи
@dp.message(Command("tasks"))
async def show_tasks(message: Message):

    if not tasks:
        await message.answer("📭 Список задач пуст")
        return

    text = "📋 Ваши задачи:\n\n"

    for i, task in enumerate(tasks, start=1):
        text += f"{i}. {task}\n"

    await message.answer(text)



#отметить
@dp.message(Command("done"))
async def done_task(message: Message):

    try:
        index = int(message.text.split()[1]) - 1

        task = tasks.pop(index)
        completed_tasks.append(task)

        await message.answer(f"✅ Задача '{task}' выполнена")

    except:
        await message.answer("Напиши номер задачи \nПример: /done 2")


#удалить
@dp.message(Command("delete"))
async def delete_task(message: Message):

    try:
        index = int(message.text.split()[1]) - 1

        task = tasks.pop(index)

        await message.answer(f"🗑 Задача '{task}' удалена")

    except:
        await message.answer("Напиши номер задачи \nПример: /delete 1")


#статистика
@dp.message(Command("stats"))
async def stats(message: Message):

    total = len(tasks) + len(completed_tasks)
    await message.answer(f"📊 Статистика \nВсего задач: {total} \nВыполнено: {len(completed_tasks)} \nОсталось: {len(tasks)}")



async def main():
    #session = AiohttpSession(proxy="http://ОНККТ5:HOET6W@161.115.231.116:9019")
    bot = Bot(token=BOT_TOKEN) #,session=session
    print("Бот запущен")
    await dp.start_polling(bot)

asyncio.run(main())
