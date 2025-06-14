#!/usr/bin/env python3

import sys
import os
import asyncio
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Add the parent directory to sys.path to import from sources
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sources.router import AgentRouter
from sources.agents.casual_agent import CasualAgent
from sources.agents.code_agent import CoderAgent
from sources.agents.planner_agent import FileAgent
from sources.agents.browser_agent import BrowserAgent
from sources.llm_provider import Provider
from sources.utility import pretty_print
from sources.logger import Logger

# Pydantic models for API
class AgentSelectionRequest(BaseModel):
    text: str
    supported_languages: Optional[List[str]] = ["en", "fr", "zh"]

class AgentSelectionResponse(BaseModel):
    selected_agent: str
    agent_name: str
    agent_role: str
    complexity: str
    confidence: float
    language_detected: str
    translated_text: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    agents_loaded: int

class ComplexityEstimationRequest(BaseModel):
    text: str

class ComplexityEstimationResponse(BaseModel):
    complexity: str
    confidence: float

# Initialize FastAPI app
app = FastAPI(
    title="AgentRouter API",
    description="API for selecting appropriate agents based on user queries",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables
router = None
logger = Logger("router-api.log")

def initialize_router():
    """Initialize the AgentRouter with default agents"""
    global router
    try:
        logger.info("Initializing AgentRouter...")
        
        # Create a dummy provider for demonstration
        # In production, you would configure this properly
        provider = Provider(
            provider_name="ollama",
            model="llama3.2",
            server_address="http://localhost:11434",
            is_local=True
        )
        
        # Initialize agents
        agents = [
            CasualAgent("casual", "../prompts/base/casual_agent.txt", provider),
            CoderAgent("coder", "../prompts/base/coder_agent.txt", provider),
            FileAgent("file", "../prompts/base/file_agent.txt", provider),
            BrowserAgent("browser", "../prompts/base/browser_agent.txt", provider)
        ]
        
        router = AgentRouter(agents, supported_language=["en", "fr", "zh"])
        logger.info("AgentRouter initialized successfully")
        pretty_print("AgentRouter API initialized", color="success")
        
    except Exception as e:
        logger.error(f"Failed to initialize AgentRouter: {str(e)}")
        pretty_print(f"Failed to initialize AgentRouter: {str(e)}", color="failure")
        raise e

@app.on_event("startup")
async def startup_event():
    """Initialize router on startup"""
    initialize_router()

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    logger.info("Health check endpoint called")
    
    if router is None:
        raise HTTPException(status_code=503, detail="Router not initialized")
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        agents_loaded=len(router.agents)
    )

@app.post("/select-agent", response_model=AgentSelectionResponse)
async def select_agent(request: AgentSelectionRequest):
    """Select the appropriate agent based on the input text"""
    logger.info(f"Agent selection requested for text: {request.text}")
    
    if router is None:
        raise HTTPException(status_code=503, detail="Router not initialized")
    
    try:
        # Detect language and translate if needed
        lang = router.lang_analysis.detect_language(request.text)
        first_sentence = router.find_first_sentence(request.text)
        translated_text = router.lang_analysis.translate(first_sentence, lang)
        
        # Estimate complexity
        complexity = router.estimate_complexity(translated_text)
        
        # Select agent
        selected_agent = router.select_agent(request.text)
        
        if selected_agent is None:
            raise HTTPException(status_code=500, detail="Failed to select agent")
        
        # Get confidence score (this is a simplified approach)
        labels = [agent.role for agent in router.agents]
        try:
            result = router.router_vote(translated_text, labels, log_confidence=False)
            confidence = 0.8  # Placeholder confidence score
        except Exception:
            confidence = 0.5
        
        response = AgentSelectionResponse(
            selected_agent=selected_agent.type,
            agent_name=selected_agent.agent_name,
            agent_role=selected_agent.role,
            complexity=complexity,
            confidence=confidence,
            language_detected=lang,
            translated_text=translated_text if lang != "en" else None
        )
        
        logger.info(f"Selected agent: {selected_agent.agent_name} for text: {request.text}")
        return response
        
    except Exception as e:
        logger.error(f"Error in agent selection: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Agent selection failed: {str(e)}")

@app.post("/estimate-complexity", response_model=ComplexityEstimationResponse)
async def estimate_complexity(request: ComplexityEstimationRequest):
    """Estimate the complexity of a given text"""
    logger.info(f"Complexity estimation requested for text: {request.text}")
    
    if router is None:
        raise HTTPException(status_code=503, detail="Router not initialized")
    
    try:
        complexity = router.estimate_complexity(request.text)
        
        # Get confidence from the classifier
        try:
            predictions = router.complexity_classifier.predict(request.text)
            predictions = sorted(predictions, key=lambda x: x[1], reverse=True)
            confidence = predictions[0][1] if predictions else 0.5
        except Exception:
            confidence = 0.5
        
        response = ComplexityEstimationResponse(
            complexity=complexity,
            confidence=confidence
        )
        
        logger.info(f"Complexity estimation: {complexity} (confidence: {confidence}) for text: {request.text}")
        return response
        
    except Exception as e:
        logger.error(f"Error in complexity estimation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Complexity estimation failed: {str(e)}")

@app.get("/agents")
async def list_agents():
    """List all available agents"""
    logger.info("Agents list requested")
    
    if router is None:
        raise HTTPException(status_code=503, detail="Router not initialized")
    
    agents_info = []
    for agent in router.agents:
        agents_info.append({
            "name": agent.agent_name,
            "type": agent.type,
            "role": agent.role,
            "description": getattr(agent, 'description', 'No description available')
        })
    
    return {"agents": agents_info}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AgentRouter API",
        "version": "1.0.0",
        "endpoints": [
            "/health",
            "/select-agent",
            "/estimate-complexity",
            "/agents",
            "/docs"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    ) 