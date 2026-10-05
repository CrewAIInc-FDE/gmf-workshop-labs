"""Reference: find maturing agreements, decide eligible options from policy, draft outreach."""
from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from renewal_prep.common import connector, llm


@CrewBase
class RenewalPrepCrew:
    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def portfolio_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["portfolio_analyst"],  # type: ignore[index]
            llm=llm(),
            mcps=[connector()],
            allow_delegation=False,
            max_iter=12,
            verbose=True,
        )


    @agent
    def offer_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["offer_specialist"],  # type: ignore[index]
            llm=llm(),
            mcps=[connector()],
            allow_delegation=False,
            max_iter=12,
            verbose=True,
        )


    @agent
    def outreach_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["outreach_writer"],  # type: ignore[index]
            llm=llm(),
            allow_delegation=False,
            max_iter=12,
            verbose=True,
        )

    @task
    def find_accounts(self) -> Task:
        return Task(config=self.tasks_config["find_accounts"])  # type: ignore[index]


    @task
    def decide_options(self) -> Task:
        return Task(config=self.tasks_config["decide_options"])  # type: ignore[index]


    @task
    def write_outreach(self) -> Task:
        return Task(config=self.tasks_config["write_outreach"])  # type: ignore[index]

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)
