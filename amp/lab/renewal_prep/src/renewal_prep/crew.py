"""Renewal prep crew. The agents and tasks are described in config/agents.yaml and config/tasks.yaml."""
from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from renewal_prep.common import connector, llm


@CrewBase
class RenewalPrepCrew:
    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def renewal_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["renewal_specialist"],  # type: ignore[index]
            llm=llm(),
            mcps=[connector("list_expiring_agreements", "get_client_account")],
            max_iter=12,
            verbose=True,
        )

    @task
    def draft_renewal_outreach(self) -> Task:
        return Task(config=self.tasks_config["draft_renewal_outreach"])  # type: ignore[index]

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)
