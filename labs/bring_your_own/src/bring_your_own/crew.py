"""Starter: one general agent with the workshop connector, ready to be reshaped around your problem."""
from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from bring_your_own.common import connector, llm


@CrewBase
class BringYourOwnCrew:
    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def assistant(self) -> Agent:
        return Agent(
            config=self.agents_config["assistant"],  # type: ignore[index]
            llm=llm(),
            mcps=[connector()],
            allow_delegation=False,
            max_iter=12,
            verbose=True,
        )

    @task
    def solve(self) -> Task:
        return Task(config=self.tasks_config["solve"])  # type: ignore[index]

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)
