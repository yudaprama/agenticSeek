from sources.agents.agent import Agent
from sources.utility import pretty_print
from sources.logger import Logger

class AgentRouter:
    """
    AgentRouter is a class that selects the appropriate agent based on the user query using simple keyword matching.
    """
    def __init__(self, agents: list):
        self.agents = agents
        self.logger = Logger("router.log")
        self.asked_clarify = False
        
        # Simple keyword patterns for agent selection
        self.patterns = {
            'code': ['code', 'program', 'script', 'debug', 'compile', 'python', 'java', 'javascript', 'c++', 'bash', 'terminal', 'execute', 'run', 'coding', 'programming', 'develop'],
            'file': ['file', 'folder', 'directory', 'save', 'create', 'delete', 'move', 'copy', 'find', 'search file', 'organize', 'locate', 'exists'],
            'web': ['search', 'browse', 'website', 'google', 'internet', 'web', 'online', 'url', 'link', 'find information', 'lookup', 'news'],
            'planner': ['plan', 'organize', 'schedule', 'task', 'project', 'multiple', 'steps', 'complex', 'workflow', 'then', 'and then', 'after that']
        }
    
    def find_first_sentence(self, text: str) -> str:
        """Extract the first sentence from text."""
        first_sentence = None
        for line in text.split("\n"):
            first_sentence = line.strip()
            break
        if first_sentence is None:
            first_sentence = text
        return first_sentence
    
    def estimate_complexity(self, text: str) -> str:
        """
        Estimate complexity based on simple heuristics.
        Returns 'HIGH' for complex tasks, 'LOW' for simple ones.
        """
        text_lower = text.lower()
        
        # High complexity indicators
        high_complexity_words = [
            'then', 'and then', 'after that', 'multiple', 'several', 'both', 
            'first', 'second', 'next', 'finally', 'also', 'additionally',
            'build', 'create app', 'web app', 'application', 'api', 'database'
        ]
        
        # Count complexity indicators
        complexity_score = 0
        for word in high_complexity_words:
            if word in text_lower:
                complexity_score += 1
        
        # Check for multiple actions (commas, "and", etc.)
        if ',' in text or ' and ' in text_lower:
            complexity_score += 1
            
        # Long queries are often more complex
        if len(text.split()) > 15:
            complexity_score += 1
            
        return "HIGH" if complexity_score >= 2 else "LOW"
    
    def find_planner_agent(self) -> Agent:
        """Find the planner agent."""
        for agent in self.agents:
            if agent.type == "planner_agent":
                return agent
        pretty_print(f"Error finding planner agent. Please add a planner agent to the list of agents.", color="failure")
        self.logger.error("Planner agent not found.")
        return None
    
    def classify_intent(self, text: str) -> str:
        """
        Classify user intent based on keyword matching.
        Returns the most likely agent role.
        """
        text_lower = text.lower()
        scores = {}
        
        # Score each category based on keyword matches
        for category, keywords in self.patterns.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            scores[category] = score
        
        # Find the category with the highest score
        if not scores or max(scores.values()) == 0:
            return "talk"  # Default to casual conversation
            
        best_category = max(scores, key=scores.get)
        
        # Map categories to agent roles
        role_mapping = {
            'code': 'code',
            'file': 'file',
            'web': 'web',
            'planner': 'planification'
        }
        
        return role_mapping.get(best_category, 'talk')
    
    def select_agent(self, text: str) -> Agent:
        """
        Select the appropriate agent based on the text using simple keyword matching.
        """
        assert len(self.agents) > 0, "No agents available."
        if len(self.agents) == 1:
            return self.agents[0]
        
        # Get first sentence for analysis
        text = self.find_first_sentence(text)
        
        # Check complexity first
        complexity = self.estimate_complexity(text)
        if complexity == "HIGH":
            pretty_print(f"Complex task detected, routing to planner agent.", color="info")
            planner = self.find_planner_agent()
            if planner:
                return planner
        
        # Classify intent
        best_role = self.classify_intent(text)
        
        # Find agent with matching role
        for agent in self.agents:
            if best_role == agent.role:
                pretty_print(f"Selected agent: {agent.agent_name} (role: {agent.role})", color="warning")
                self.logger.info(f"Selected agent {agent.agent_name} for text: {text}")
                return agent
        
        # Fallback to first agent (usually casual)
        pretty_print(f"No specific agent found, using default: {self.agents[0].agent_name}", color="warning")
        self.logger.warning(f"No agent selected for text: {text}, using default")
        return self.agents[0]
