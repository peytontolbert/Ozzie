# Ozzie: AI Software Developer and Autonomous Agent Builder

## Project Overview

Ozzie is an advanced AI system designed to function as a software developer and autonomous agent builder. It utilizes a complex architecture of interconnected components to reason about scenarios, make decisions, and execute actions in a virtual environment.

## Main Components

1. **FastAPI Application** (`main.py`)
   - Serves as the entry point for the application
   - Initializes and connects all major components
   - Sets up API endpoints and WebSocket connections

2. **Autonomous Loop** (`autonomous_loop/`)
   - Core decision-making cycle
   - Processes scenarios, selects actions, and updates the knowledge graph
   - Key classes: `AutonomousLoop`, `KnowledgeGraphUpdater`, `EntityExtractor`, `RelationshipExtractor`

3. **Knowledge Graph** (`knowledge_graph/`)
   - Stores and manages the system's knowledge
   - Includes `QueryEngine` for interacting with the Neo4j database

4. **Experience Engine** (`experience_engine.py`)
   - Generates scenarios and evaluates outcomes
   - Creates and manages hierarchical agent structures

5. **Virtual Environment** (`virtual_environment.py`)
   - Simulates the environment in which Ozzie operates

6. **Human-AGI Interface** (`human_agi_interface/`)
   - Components for aligning AI behavior with human values and intentions
   - Includes: `ValueAlignmentVerifier`, `ContainmentProtocolManager`, `AlignmentDecisionSimulator`, `LongTermImpactAnalyzer`, `FeedbackIntegrator`, `ExplanationGenerator`, `AugmentedIntelligenceInterface`, `IntentInterpreter`

7. **Workflows** (`workflows/`)
   - Manages and optimizes workflows for task execution
   - Key classes: `WorkflowEngine`, `WorkflowOptimizer`

8. **Web UI** (`web_ui/`)
   - Provides a user interface for interacting with the system
   - Includes API endpoints and WebSocket management

9. **Cognitive Architecture** (`cognitive_architecture/`)
   - Includes the `AbstractReasoningEngine` for high-level reasoning

## Key Interactions

1. The `AutonomousLoop` orchestrates the system's operation:
   - Generates scenarios using the `ExperienceEngine`
   - Processes scenarios using the `AbstractReasoningEngine`
   - Generates and executes workflows using the `WorkflowEngine`
   - Selects actions based on the processing results
   - Updates the `KnowledgeGraph` with new information

2. The `KnowledgeGraph` (implemented via `QueryEngine`) is used throughout the system:
   - Updated after each cycle of the autonomous loop
   - Queried during reasoning and decision-making processes

3. The `VirtualEnvironment` interacts with the `ExperienceEngine` to simulate action outcomes

4. Human-AGI interface components ensure alignment with human values and intentions

## Setup and Dependencies

- Neo4j is used as the graph database
- Environment variables for database connection are stored in a `.env` file
- The system is built on FastAPI and uses asyncio for concurrent operations

## Running the Application

1. Ensure all dependencies are installed:
   ```
   pip install -r requirements.txt
   ```

2. Set up your `.env` file with Neo4j credentials:
   ```
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_password
   ```

3. Run the main application:
   ```
   python main.py
   ```

## Next Steps for Development

1. Implement more sophisticated scenario generation in the `ExperienceEngine`
2. Enhance the `AbstractReasoningEngine` for better decision-making
3. Expand the capabilities of the `WorkflowEngine` and `WorkflowOptimizer`
4. Improve the user interface in the `web_ui` component
5. Develop more advanced value alignment and containment protocols in the `human_agi_interface`

For more detailed information on each component, please refer to their respective documentation files.