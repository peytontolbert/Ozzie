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

app = FastAPI()

app.mount("/api", api_app)
app.mount("/ws", ws_app)

@app.on_event("startup")
async def startup_event():
    await data_aggregator.connect()
    await event_publisher.start()
    # Initialize AGI components
    value_alignment_verifier = ValueAlignmentVerifier()
    containment_protocol_manager = ContainmentProtocolManager()
    alignment_decision_simulator = AlignmentDecisionSimulator()
    long_term_impact_analyzer = LongTermImpactAnalyzer()
    feedback_integrator = FeedbackIntegrator()
    explanation_generator = ExplanationGenerator()
    intent_interpreter = IntentInterpreter()
    workflow_engine = WorkflowEngine()
    workflow_optimizer = WorkflowOptimizer(workflow_engine)
    augmented_intelligence_interface = AugmentedIntelligenceInterface(
        intent_interpreter=intent_interpreter,
        explanation_generator=explanation_generator,
        feedback_integrator=feedback_integrator
    )

    # Add these components to a global state or dependency injection system
    app.state.agi_components = {
        "value_alignment_verifier": value_alignment_verifier,
        "containment_protocol_manager": containment_protocol_manager,
        "alignment_decision_simulator": alignment_decision_simulator,
        "long_term_impact_analyzer": long_term_impact_analyzer,
        "feedback_integrator": feedback_integrator,
        "explanation_generator": explanation_generator,
        "augmented_intelligence_interface": augmented_intelligence_interface,
        "intent_interpreter": intent_interpreter,
        "workflow_optimizer": workflow_optimizer
    }

    # Initialize VirtualEnvironment
    ve = VirtualEnvironment()
    ve.initialize()

    # Start the autonomous loop
    autonomous_loop = AutonomousLoop(app.state.agi_components, ve)
    asyncio.create_task(autonomous_loop.run())

@app.on_event("shutdown")
async def shutdown_event():
    await data_aggregator.disconnect()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)