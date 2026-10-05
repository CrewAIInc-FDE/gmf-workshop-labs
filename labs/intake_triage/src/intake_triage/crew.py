"""Starter: one agent reads one inbox document and says where it should go."""
from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from intake_triage.common import connector, llm


@CrewBase
class IntakeTriageCrew:
    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def intake_clerk(self) -> Agent:
        return Agent(
            config=self.agents_config["intake_clerk"],  # type: ignore[index]
            llm=llm(),
            mcps=[connector()],
            allow_delegation=False,
            max_iter=12,
            verbose=True,
        )

    @task
    def triage_document(self) -> Task:
        return Task(config=self.tasks_config["triage_document"])  # type: ignore[index]

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)
