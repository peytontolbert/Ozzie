from fastapi import FastAPI
from web_ui.api_endpoints import app as api_app, data_aggregator
from web_ui.websocket_manager import app as ws_app
from web_ui.event_publisher import event_publisher
from human_agi_interface.value_alignment_verifier import ValueAlignmentVerifier
from human_agi_interface.containment_protocol_manager import ContainmentProtocolManager
from human_agi_interface.alignment_decision_simulator import AlignmentDecisionSimulator
from human_agi_interface.long_term_impact_analyzer import LongTermImpactAnalyzer
from human_agi_interface.feedback_integrator import FeedbackIntegrator
from human_agi_interface.explanation_generator import ExplanationGenerator
from human_agi_interface.augmented_intelligence_interface import AugmentedIntelligenceInterface
from human_agi_interface.intent_interpreter import IntentInterpreter
from workflows.workflow_optimizer import WorkflowOptimizer
from workflows.workflow_engine import WorkflowEngine
from autonomous_loop import AutonomousLoop
import asyncio
from virtual_environment import VirtualEnvironment
from web_ui import api_endpoints
from experience_engine import ExperienceEngine
from cognitive_architecture.abstract_reasoning_engine import AbstractReasoningEngine
from simulated_environment import SimulatedEnvironment
from generalized_simulated_environment import GeneralizedSimulatedEnvironment
import logging
from utils.logger import Logger
from knowledge_graph.graph_structure import GraphStructure
from knowledge_graph.query_engine import QueryEngine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()

app.mount("/api", api_app)
app.mount("/ws", ws_app)

app.include_router(api_endpoints.router)

@app.on_event("startup")
async def startup_event():
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    logger = Logger("MainApplication")
    logger.info("Application starting up")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    # Initialize app.state.agi_components
    app.state.agi_components = {}

    # Initialize GraphStructure and QueryEngine using environment variables
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    
    graph_structure = GraphStructure(uri, user, password)
    query_engine = QueryEngine(uri, user, password)

    # Add GraphStructure and QueryEngine to agi_components
    app.state.agi_components["graph_structure"] = graph_structure
    app.state.agi_components["query_engine"] = query_engine
    app.state.agi_components["knowledge_graph"] = query_engine  # Use QueryEngine as the knowledge graph

    global feedback_integrator
    feedback_integrator = FeedbackIntegrator(state_size=10, action_size=5)  # Provide values if needed
    await data_aggregator.connect()
    await event_publisher.start()

    # Initialize AGI components
    app.state.agi_components.update({
        "value_alignment_verifier": ValueAlignmentVerifier(),
        "containment_protocol_manager": ContainmentProtocolManager(),
        "alignment_decision_simulator": AlignmentDecisionSimulator(),
        "long_term_impact_analyzer": LongTermImpactAnalyzer(),
        "explanation_generator": ExplanationGenerator(),
        "intent_interpreter": IntentInterpreter(),
        "workflow_engine": WorkflowEngine(),
        "feedback_integrator": feedback_integrator,
    })

    # Initialize components that depend on other components
    app.state.agi_components.update({
        "workflow_optimizer": WorkflowOptimizer(app.state.agi_components["workflow_engine"]),
        "augmented_intelligence_interface": AugmentedIntelligenceInterface(
            intent_interpreter=app.state.agi_components["intent_interpreter"],
            explanation_generator=app.state.agi_components["explanation_generator"],
            feedback_integrator=app.state.agi_components["feedback_integrator"]
        ),
    })

    # Initialize ExperienceEngine with the query_engine
    experience_engine = ExperienceEngine(query_engine=app.state.agi_components["query_engine"])
    app.state.agi_components["experience_engine"] = experience_engine

    # Create hierarchical agent structure
    await experience_engine.create_hierarchical_agents(2, 3)

    # Initialize VirtualEnvironment with experience_engine
    ve = VirtualEnvironment(experience_engine)
    ve.initialize()

    # Initialize AbstractReasoningEngine with the knowledge_graph (query_engine)
    abstract_reasoning_engine = AbstractReasoningEngine(app.state.agi_components["knowledge_graph"])
    app.state.agi_components["abstract_reasoning_engine"] = abstract_reasoning_engine

    # Start the autonomous loop
    autonomous_loop = AutonomousLoop(app.state.agi_components, ve)
    asyncio.create_task(autonomous_loop.run())

    # Start Ozzie's agent management
    asyncio.create_task(app.state.agi_components["experience_engine"].ozzie_manage_agents())

@app.on_event("shutdown")
async def shutdown_event():
    await data_aggregator.disconnect()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)