import os
import asyncio
from dotenv import load_dotenv
from browser_use.agent.service import Agent
from langchain_openai import ChatOpenAI
from browser_use import Browser

async def login_to_system(context, system_page, login, password):
    print(f"Logging into system: {system_page}")
    await context.navigate_to(system_page)

    # Fill in the login form

    current_page = await context.get_current_page()
    await current_page.fill("input[name='login']", login)
    await current_page.fill("input[type='password']", password)
    await current_page.click("input[type='submit']")

    # async with current_page.expect_navigation(wait_until='networkidle'):
    #     await current_page.click("input[type='submit']")

    print("Logged in...")

    # Print the page title
    title = await current_page.title()
    print(f"Page title: {title}")

    return context

async def create_agent(context):
    llm = ChatOpenAI(model='gpt-4o', temperature=0.0)

    print("Creating agent...")

    agent = Agent(
        task='Get available slots for today in current tab',
        llm=llm,
        browser_context=context,
    )

    print("Agent created...")
    return agent

async def main():
    load_dotenv()  # Load environment variables from .env file

    login = os.getenv("system_login")
    password = os.getenv("system_password")
    page = os.getenv("system_url")

    print(f"system Login: {login}")
    print(f"system Password: {password}")
    print(f"system URL: {page}")

    llm = ChatOpenAI(model='gpt-4o', temperature=0.0)

    browser = Browser()

    context = await browser.new_context()

    print("Login into system...")
    system_ctx = await login_to_system(context, page, login, password)

    agent = await create_agent(system_ctx)

    result = await agent.run()
    print(result)

if __name__ == '__main__':
    asyncio.run(main())