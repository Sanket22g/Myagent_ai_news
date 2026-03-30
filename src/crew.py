from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from src.tools.custom_tool import YouTubeSearchTool
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from src.models import ResearchDigestOutput
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class MyagentUdate():
    """MyagentUdate crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def news_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['news_scout'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            
        )

    @agent
    def youtube_research_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['youtube_research_scout'], # type: ignore[index]
            verbose=True,
            tools=[YouTubeSearchTool()]
        )
    @agent
    def summary_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['summary_analyst'], # type: ignore[index]
            verbose=True
        )
    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def fetch_ai_news(self) -> Task:
        return Task(
            config=self.tasks_config['fetch_ai_news'], # type: ignore[index]
        )

    @task
    def fetch_related_youtube_videos(self) -> Task:
        return Task(
            config=self.tasks_config['fetch_related_youtube_videos'], # type: ignore[index]
            depends_on=[self.fetch_ai_news] # This means this task will only run after fetch_ai_news is completed
        )
    @task
    def generate_final_summary(self) -> Task:
        return Task(
            config=self.tasks_config['generate_final_summary'], # type: ignore[index]
           output_pydantic=ResearchDigestOutput,
           #output_file="report.json"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AiAgentAppForSummary crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            max_rpm=10
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
