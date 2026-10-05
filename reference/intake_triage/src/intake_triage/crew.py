"""Reference: extract and classify a batch of inbox documents, route them, then review escalations."""
from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from intake_triage.common import connector, llm


@CrewBase
class IntakeTriageCrew:
    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def intake_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["intake_analyst"],  # type: ignore[index]
            llm=llm(),
            mcps=[connector()],
            allow_delegation=False,
            max_iter=12,
            verbose=True,
        )


    @agent
    def router(self) -> Agent:
        return Agent(
            config=self.agents_config["router"],  # type: ignore[index]
            llm=llm(),
            mcps=[connector()],
            allow_delegation=False,
            max_iter=12,
            verbose=True,
        )


    @agent
    def triage_supervisor(self) -> Agent:
        return Agent(
            config=self.agents_config["triage_supervisor"],  # type: ignore[index]
            llm=llm(),
            mcps=[connector()],
            allow_delegation=False,
            max_iter=12,
            verbose=True,
        )

    @task
    def extract_documents(self) -> Task:
        return Task(config=self.tasks_config["extract_documents"])  # type: ignore[index]


    @task
    def route_documents(self) -> Task:
        return Task(config=self.tasks_config["route_documents"])  # type: ignore[index]


    @task
    def review_batch(self) -> Task:
        return Task(config=self.tasks_config["review_batch"])  # type: ignore[index]

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)
