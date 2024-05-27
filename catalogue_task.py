from SeoKeywordResearch import SeoKeywordResearch
from crewai import Task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, tool
from textwrap import dedent
import os


os.environ["SERPER_API_KEY"]


search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()


@tool("SEO_Key")
def seo_keyword(self, question) -> str:
    ''' This the tools to help in doing seo research input the topic and get keywords '''
    keyword_research = SeoKeywordResearch(
        query=f"{question}",
        api_key=os.environ['SERP_API_KEY'],
        lang='en',
        country='in',
        domain='google.com'
    )

    auto_complete_results = keyword_research.get_auto_complete()
    related_searches_results = keyword_research.get_related_searches()
    related_questions_results = keyword_research.get_related_questions()

    data = {
        'auto_complete': auto_complete_results,
        'related_searches': related_searches_results,
        'related_questions': related_questions_results
    }

    data = keyword_research.print_data(data)
    return data







class Cataloguetask():


  def researcher(self, product, agent):
    return Task(
      description= (f'''
        'Browse the internet for informations related this product.'
        'Product name = {product}'
        'Gathering all the data available about that product available on the internet'
        'After  gathering all the product related details. compile them into a detailed report of the product and pass as output'
        'Please be precise with numbers'
    '''),
      expected_output=f'''Correct details about the of the product you are provided with.
      'Scrape and pass as much detail as possible'
      ''',
      agent=agent,
      tools=[search_tool,scrape_tool],
      async_execution=True,

    )
  


  def research_seo(self,agent, product, cont):
    return Task(
      description = f"""
      'product name = {product}'
      'please search for top ranking SEO keywords to rank this product first on the browser'
      'please don't choose more than 4 keywords but make sure they are excellent'
      """,
      expected_output = """
      please search best and top ranking keywords of done pass only actual keywords
      """,
      agent = agent ,
      tools = [seo_keyword],
      context = [cont],
    )




  def writing(self, agent, cont, cont2 ,product):
    return Task(
        description =dedent(f'''
                            'product = {product}'
                            'Use the product information, You have to create digital catalogue of this product.'
                            'use easy to read words and write like a skilled human copywriter'
                            'Craft compelling and persuasive product content for driving sales, improving customer engagement, enhance brand identity, and boost search engine optimization (SEO) rankings.'
                            'Please mix SEO ranking keywords inside PRODUCT details.'
    '''),
        expected_output='''
        'Use eye-catching techniques to make it more appealing and engaging to consumers.'
        'Write product copy gives customers a clear and direct message about the benefits and value of a product.'
        'Highlight how this product can address customers’ needs and solve their problems, then they are compelled to purchase.' 
        'Consumers appreciate transparency and concise product information when they read it.'
        'Use persuasive language Skillfully and mix call-to-action in other details. That can evoke emotions or create a sense of urgency, encouraging consumers to make a purchase.'
        ''',
        agent = agent,
        context = [cont, cont2]
    )
  

