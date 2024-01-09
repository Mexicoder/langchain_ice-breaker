from langchain.prompts import PromptTemplate
# from langchain.chat_models import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor

from langchain.agents import initialize_agent, Tool, AgentType, create_react_agent

from tools.tools import get_profile_url


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    template = """given the full name {name_of_person} i want you to get me a link to their LinkedIn profile page.
                        Your answer should contain only a URL"""

    tools_for_agent = [
        Tool(
            name="Crawl Google for linkedin profile page",
            func=get_profile_url,
            description="useful for when you need to get the LinkedIn Page URL",
        )
    ]
    
    # agent = create_react_agent(
    #     tools=tools_for_agent,
    #     llm=llm,
    #     # agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    #     # verbose=True,
    # )

    agent:AgentExecutor = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    prompt_template = PromptTemplate(
        input_variables=["name_of_person"], template=template
    )

    linkedin_profile_url = agent.run(
        prompt_template.format_prompt(name_of_person=name)
        )
    return linkedin_profile_url
