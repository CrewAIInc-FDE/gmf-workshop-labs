"""Bring-your-own crew with the workshop finance tools on the one agent."""
from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from bring_your_own.common import connector, llm
from bring_your_own.northwind_finance_tools import (
    CreditTierLookupTool,
    LoanPaymentCalculatorTool,
    PayoffQuoteTool,
)


@CrewBase
class BringYourOwnCrew:
    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def assistant(self) -> Agent:
        return Agent(
            config=self.agents_config["assistant"],  # type: ignore[index]
            llm=llm(),
            # EDIT HERE: name only the connector tools this agent needs (none named = all of them),
            # for example connector("get_client_account", "search_policies", "get_policy").
            mcps=[connector("get_client_account")],
            # EDIT HERE: keep only the finance tools this agent needs. Fewer tools means fewer wrong turns.
            tools=[LoanPaymentCalculatorTool(), PayoffQuoteTool(), CreditTierLookupTool()],
            max_iter=12,
            verbose=True,
        )

    @task
    def do_the_work(self) -> Task:
        return Task(config=self.tasks_config["do_the_work"])  # type: ignore[index]

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)
