"""Bring-your-own crew. The agents and tasks are described in config/agents.yaml and config/tasks.yaml."""
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
            # EDIT HERE: with no names the agent gets every connector tool. Fewer tools means fewer wrong turns,
            # so name the ones it needs, for example connector("search_policies", "get_policy").
            mcps=[connector()],
            max_iter=12,
            verbose=True,
        )

    @task
    def do_the_work(self) -> Task:
        return Task(config=self.tasks_config["do_the_work"])  # type: ignore[index]

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)
