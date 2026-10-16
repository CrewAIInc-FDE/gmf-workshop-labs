"""Payoff quote desk crew. The agents and tasks are described in config/agents.yaml and config/tasks.yaml.

The calculator tool comes from the northwind_finance_tools folder next to this file (a copy of the
workshop tools package), so nothing needs to be installed or published."""
from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from bring_your_own.common import connector, llm
from bring_your_own.northwind_finance_tools import PayoffQuoteTool


@CrewBase
class BringYourOwnCrew:
    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def payoff_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["payoff_analyst"],  # type: ignore[index]
            llm=llm(),
            mcps=[connector("get_client_account")],
            tools=[PayoffQuoteTool()],
            max_iter=12,
            verbose=True,
        )

    @agent
    def quote_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["quote_writer"],  # type: ignore[index]
            llm=llm(),
            mcps=[connector("search_policies", "get_policy")],
            max_iter=12,
            verbose=True,
        )

    @task
    def calculate_payoff(self) -> Task:
        return Task(config=self.tasks_config["calculate_payoff"])  # type: ignore[index]

    @task
    def write_quote_note(self) -> Task:
        return Task(config=self.tasks_config["write_quote_note"])  # type: ignore[index]

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)
