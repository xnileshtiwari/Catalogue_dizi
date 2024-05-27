from crewai import Agent
from textwrap import dedent
import streamlit as st
import time


pools = ["Initializing...", "Giving instructions...", "Performing actions⚡..."]


def streamlit_callback(step_output):
    # This function will be called after each step of the agent's execution
    with st.status("New Agent...", expanded=True) as status:
        for pool in pools:
            st.write(pool)
            time.sleep(2)

        st.markdown("---")
        for step in step_output:
            if isinstance(step, tuple) and len(step) == 2:
                action, observation = step
                if isinstance(action, dict) and "tool" in action and "tool_input" in action and "log" in action:
                    st.markdown(f"# Action")
                    st.markdown(f"**Tool:** {action['tool']}")
                    st.markdown(f"**Tool Input** {action['tool_input']}")
                    st.markdown(f"**Log:** {action['log']}")
                    st.markdown(f"**Action:** {action['Action']}")
                    st.write("Found URL.")
                    st.markdown(
                        f"**Action Input:** ```json\n{action['tool_input']}\n```")
                elif isinstance(action, str):
                    st.markdown(f"**Action:** {action}")
                else:
                    st.markdown(f"**Action:** {str(action)}")
                time.sleep(1)

                st.markdown(f"**Observation**")
                time.sleep(2)
                if isinstance(observation, str):
                    observation_lines = observation.split('\n')
                    for line in observation_lines:
                        if line.startswith('Title: '):
                            st.markdown(f"**Title:** {line[7:]}")
                        elif line.startswith('Link: '):
                            st.markdown(f"**Link:** {line[6:]}")
                        elif line.startswith('Snippet: '):
                            st.markdown(f"**Snippet:** {line[9:]}")
                        elif line.startswith('-'):
                            st.markdown(line)
                        else:
                            st.markdown(line)
                else:
                    st.markdown(str(observation))
            else:
                st.markdown(step)
        status.update(label="Action completed!", state="complete", expanded=False)












class Catalogueagent():
    def researcher(self, langm):
        return Agent(
            role = "Product Researcher",
            goal = "Being the best at gather, interpret data and amaze your customer with it",
            backstory = '''
            You are the BEST product researcher, you're 
            skilled in sifting through different e-commerce websites, product pages, to gather all the 
            data about the product provided.
            ''',
            verbose=True,
            # tools=[],  # Optional, defaults to an empty list
            llm=langm,  # Optional
            #allow_delegation=False,  # Optional
            max_iter=4,  # Optional
            # max_rpm=None, # Optional
            step_callback=streamlit_callback,
        )


    def seo_expert(self, langm):
        return Agent(
            role = "SEO Expert",
            goal = "Search for high ranking seo keywords",
            backstory = '''
            You are SEO expert at big company. your job is to research about high ranking keywords 
            for digital product catalogue to improve it's ranking and overall sales.
            ''',
            verbose =True,
            llm = langm,
            max_iter=2,  # Optional

            step_callback=streamlit_callback
        )



    def writer(self, langm):
        return Agent(
            role = "Writter",
            goal = "Write highquality contents",
            backstory = dedent('''
            You are a creative copy-writter. For writing product catalogue on amazon.
            You are an expert at marketing and at art of using words to please reader.
            '''),
            verbose=True,
            # tools=[],  # Optional, defaults to an empty list
            llm=langm,  # Optional
            allow_delegation=False,  # Optional
            # max_iter=15,  # Optional
            # max_rpm=None, # Optional
            step_callback=streamlit_callback
        )
