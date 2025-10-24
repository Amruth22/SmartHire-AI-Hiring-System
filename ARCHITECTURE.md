# SmartHire Architecture Documentation

## Overview

SmartHire follows the **Client Format Pattern** with strict separation of concerns across five distinct layers. This architecture ensures maintainability, scalability, and testability.

---

## Architecture Layers

### Layer 1: Tool Layer (analyzers/)

**Purpose**: Pure analysis tools with NO state management or orchestration logic

**Components**:
- `AIAnalyzer` - Gemini AI wrapper (PRIMARY - all predictions)
- `SemanticAnalyzer` - SBERT wrapper (SUPPORTING - similarity only)

**Responsibilities**:
- ✅ Perform AI/ML/Semantic operations
- ✅ Return pure data structures
- ❌ NO state management
- ❌ NO orchestration logic
- ❌ NO side effects (except logging)

**Example**:
```python
class AIAnalyzer:
    def parse_resume(self, resume_text: str) -> Dict[str, Any]:
        # Pure function: text in, dict out
        return extracted_features
```

---

### Layer 2: Agent Layer (agents/)

**Purpose**: Coordinators that use analyzers as tools

**Components**:
- `ResumeParserAgent`
- `ExperiencePredictorAgent`
- `ResumeScorerAgent`
- `JobFitAnalyzerAgent`
- `QuestionGeneratorAgent`
- `AnswerEvaluatorAgent`

**Responsibilities**:
- ✅ Coordinate analysis using tools
- ✅ Implement business logic
- ✅ Handle errors and fallbacks
- ❌ NO direct AI/ML calls
- ❌ NO state updates
- ❌ NO orchestration

**Example**:
```python
class ResumeParserAgent(BaseAgent):
    def __init__(self):
        self.ai_analyzer = AIAnalyzer()  # Use tool
    
    def analyze(self, resume_text: str) -> Dict[str, Any]:
        # Coordinate using analyzer
        return self.ai_analyzer.parse_resume(resume_text)
```

---

### Layer 3: Node Layer (nodes/)

**Purpose**: Thin wrappers that call agents and update state

**Components**:
- `resume_parser_node`
- `experience_predictor_node`
- `resume_scorer_node`
- `job_fit_analyzer_node`
- `question_generator_node`
- `answer_evaluator_node`

**Responsibilities**:
- ✅ Call agent's analyze() method
- ✅ Update CandidateState
- ✅ Return updated state
- ❌ NO business logic
- ❌ NO tool usage
- ❌ NO orchestration

**Example**:
```python
def resume_parser_node(state: CandidateState) -> CandidateState:
    result = agent.analyze(state.resume_text)
    state.resume_features = result
    return state
```

---

### Layer 4: Workflow Layer (workflows/)

**Purpose**: Define stage sequences and build graphs

**Components**:
- `build_hiring_workflow()`
- `build_evaluation_workflow()`

**Responsibilities**:
- ✅ Define stage sequences
- ✅ Build HiringGraph instances
- ✅ Configure parallelism
- ❌ NO execution logic
- ❌ NO business logic
- ❌ NO state management

**Example**:
```python
def build_hiring_workflow() -> HiringGraph:
    stages = [
        [resume_parser_node],
        [experience_predictor_node],
        [resume_scorer_node],
        [job_fit_analyzer_node],
        [question_generator_node]
    ]
    return HiringGraph(stages=stages)
```

---

### Layer 5: Orchestration Layer (graph.py)

**Purpose**: Execute workflows and manage state flow

**Components**:
- `HiringGraph` class

**Responsibilities**:
- ✅ Execute stages sequentially
- ✅ Handle parallel execution (if needed)
- ✅ Merge state from parallel nodes
- ✅ Error handling and logging
- ❌ NO business logic
- ❌ NO tool usage

**Example**:
```python
class HiringGraph:
    def run(self, initial_state: CandidateState) -> CandidateState:
        for stage in self.stages:
            for node in stage:
                result = node(main_state)
                main_state = result
        return main_state
```

---

## Data Flow

### Main Workflow

```
User Input (Resume + Job)
    ↓
CandidateState (initial)
    ↓
HiringGraph.run()
    ↓
Stage 1: resume_parser_node
    → ResumeParserAgent
    → AIAnalyzer.parse_resume()
    → Update state.resume_features
    ↓
Stage 2: experience_predictor_node
    → ExperiencePredictorAgent
    → MLAnalyzer.predict_experience_level()
    → Update state.experience_level
    ↓
Stage 3: resume_scorer_node
    → ResumeScorerAgent
    → MLAnalyzer.score_resume()
    → Update state.resume_score
    ↓
Stage 4: job_fit_analyzer_node
    → JobFitAnalyzerAgent
    → AIAnalyzer.analyze_job_fit()
    → Update state.job_fit
    ↓
Stage 5: question_generator_node
    → QuestionGeneratorAgent
    → AIAnalyzer.generate_questions()
    → Update state.questions
    ↓
CandidateState (with questions)
    ↓
[USER ANSWERS QUESTIONS]
    ↓
Stage 6: answer_evaluator_node
    → AnswerEvaluatorAgent
    → SemanticAnalyzer + AIAnalyzer
    → Update state.answers, state.final_score
    ↓
CandidateState (final)
```

---

## State Management

### CandidateState Design

```python
@dataclass
class CandidateState:
    # Input data (immutable after creation)
    resume_text: str
    job_description: str
    job_title: str
    
    # Analysis results (populated by agents)
    resume_features: Dict
    experience_level: str
    resume_score: float
    job_fit: Dict
    
    # Interview data
    questions: List[Dict]
    answers: List[Dict]
    
    # Results
    final_score: float
    
    # Metadata
    current_step: str
    errors: List[str]
    workflow_complete: bool
```

### State Methods

**clone()** - Deep copy for parallel execution
```python
state_copy = state.clone()
```

**merge_from()** - Smart merge from parallel results
```python
main_state.merge_from(parallel_result)
```

**to_dict()** - Convert to dictionary
```python
state_dict = state.to_dict()
```

---

## Separation of Concerns

### What Goes Where?

| Layer | Responsibility | Can Do | Cannot Do |
|-------|---------------|--------|-----------|
| **Analyzers** | Pure tools | AI/ML operations, return data | State management, orchestration |
| **Agents** | Coordinators | Use analyzers, business logic | Direct AI/ML, state updates |
| **Nodes** | Wrappers | Call agents, update state | Business logic, tool usage |
| **Workflows** | Builders | Define stages, build graphs | Execute, business logic |
| **Graph** | Orchestrator | Execute stages, manage flow | Business logic, tool usage |

---

## Key Design Principles

### 1. Single Responsibility

Each component has ONE clear responsibility:
- Analyzers: Analyze
- Agents: Coordinate
- Nodes: Wrap
- Workflows: Build
- Graph: Orchestrate

### 2. Dependency Inversion

Higher layers depend on abstractions, not implementations:
- Agents depend on analyzer interfaces
- Nodes depend on agent interfaces
- Workflows depend on node functions

### 3. Open/Closed Principle

Open for extension, closed for modification:
- Add new analyzers without changing agents
- Add new agents without changing nodes
- Add new nodes without changing workflows

### 4. Interface Segregation

Each layer exposes minimal interface:
- Analyzers: analyze() methods
- Agents: analyze() method
- Nodes: node(state) -> state
- Workflows: build_*_workflow()
- Graph: run(state) -> state

---

## Error Handling Strategy

### Layer-by-Layer

**Analyzers**:
- Try AI/ML operation
- Catch exceptions
- Return fallback result
- Log error

**Agents**:
- Try analyzer call
- Catch exceptions
- Try fallback analyzer
- Log error

**Nodes**:
- Try agent call
- Catch exceptions
- Add error to state.errors
- Return state (don't crash)

**Graph**:
- Try node execution
- Catch exceptions
- Log error
- Continue to next stage (unless raise_on_error=True)

---

## Configuration Management

### ConfigManager Pattern

Singleton pattern for centralized configuration:

```python
config = get_config()
api_key = config.get("GEMINI_API_KEY_1")
```

### Configuration Sources (Priority Order)

1. Environment variables
2. .env file
3. Default values

---

## Logging Strategy

### Hierarchical Logging

```
root
├── graph (orchestration logs)
├── agent.* (agent-specific logs)
│   ├── agent.resume_parser
│   ├── agent.experience_predictor
│   └── ...
├── analyzer.* (analyzer-specific logs)
│   ├── analyzer.ai
│   ├── analyzer.ml
│   └── analyzer.semantic
└── node.* (node-specific logs)
```

### Log Levels

- **DEBUG**: Detailed execution flow
- **INFO**: Major milestones
- **WARNING**: Fallbacks used
- **ERROR**: Failures (with fallback)

---

## Testing Strategy

### Unit Tests

**Analyzers**: Test pure functions
```python
def test_ai_analyzer_parse_resume():
    analyzer = AIAnalyzer()
    result = analyzer.parse_resume(sample_text)
    assert "full_name" in result
```

**Agents**: Test coordination logic
```python
def test_resume_parser_agent():
    agent = ResumeParserAgent()
    result = agent.analyze(sample_text)
    assert result is not None
```

**Nodes**: Test state updates
```python
def test_resume_parser_node():
    state = CandidateState(resume_text="...")
    result = resume_parser_node(state)
    assert result.resume_features is not None
```

### Integration Tests

**Workflows**: Test end-to-end
```python
def test_hiring_workflow():
    workflow = build_hiring_workflow()
    state = CandidateState(...)
    result = workflow.run(state)
    assert result.workflow_complete
```

---

## Performance Considerations

### Optimization Points

1. **Parallel Execution**: Multiple nodes in same stage run concurrently
2. **Caching**: Cache ML model loading
3. **Lazy Loading**: Load analyzers only when needed
4. **Batch Processing**: Process multiple candidates in parallel

### Bottlenecks

1. **AI API Calls**: 5-10 seconds per call
2. **PDF Extraction**: 1-2 seconds per file
3. **ML Inference**: <1 second per prediction

---

## Scalability

### Horizontal Scaling

- Run multiple Streamlit instances
- Load balance with nginx
- Share state via Redis/database

### Vertical Scaling

- Increase max_workers for parallel execution
- Use GPU for ML inference
- Cache frequently used data

---

## Security Considerations

1. **API Keys**: Store in .env, never commit
2. **Input Validation**: Validate all user inputs
3. **PDF Safety**: Validate PDF files before processing
4. **Rate Limiting**: Implement API rate limiting
5. **Data Privacy**: Don't log sensitive candidate data

---

## Future Enhancements

### Potential Improvements

1. **Parallel Stage Execution**: Run independent stages in parallel
2. **Conditional Routing**: Skip stages based on conditions
3. **Retry Logic**: Automatic retry for failed operations
4. **Caching Layer**: Cache analysis results
5. **Database Integration**: Persist candidate data
6. **Real-time Updates**: WebSocket for live progress
7. **Batch Processing**: Process multiple candidates
8. **Custom Workflows**: User-defined workflow stages

---

## Conclusion

SmartHire's architecture provides:
- ✅ Clear separation of concerns
- ✅ Easy to test and maintain
- ✅ Scalable and extensible
- ✅ Production-ready error handling
- ✅ Follows industry best practices

The client format pattern ensures that each layer has a single, well-defined responsibility, making the system robust and maintainable.
