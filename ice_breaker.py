from langchain.prompts import PromptTemplate
# from langchain.chat_models import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

from third_parties.linkedin import scrape_linkedin_profile

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_parties.twitter import scrap_user_tweets
from output_parser import person_intel_parser


def ice_break(name: str) -> str:
    linkedin_profile_url = linkedin_lookup_agent(
        # name="John Friesen the Software Developer from London Ontario"
        name=name
    )
    # linkedin_profile_url = linkedin_lookup_agent(name="Eden Marco")

    summary_template = """
        given the LinkedIn information {information} about a person i want you to create:
        1. a short summary about them
        2. two interesting facts about them
        3. A topic that may interest them
        4. 2 createive Ice Breakers to open a conversation with them
                \n{format_instructions}
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], 
        template=summary_template,
        partial_variables={"format_instructions": person_intel_parser.get_format_instructions()},
    )

    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_profile_url,
    )

    result = chain.run(information=linkedin_data)
    # result = chain.invoke(input=linkedin_data)
    print(result)
    return result


if __name__ == "__main__":
    print("Hello LangChain!")
    ice_break(name="John Friesen the Software Developer from London Ontario")

    # print(scrap_user_tweets(username="@elonmusk", num_tweets=5))
