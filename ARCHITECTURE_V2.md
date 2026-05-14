# MIRROR Architecture v2.0

## Research-Driven Design

Based on analysis of 50+ GitHub projects (LangGraph, video generation, multi-platform apps) and user feedback from hackathon winners and production tools.

## Core Architecture Improvements

### 1. Three-Tier Caching Strategy

```
L1: In-memory Map (hot data, <1ms)
L2: Redis (warm data, <10ms)
L3: S3 (cold data, <100ms)
```

**Cache Keys:**
- Voice clones: `voice:{user_id}:{audio_hash}`
- Avatars: `avatar:{user_id}:{video_hash}`
- Scripts: `script:{transcript_hash}:{format}:{emotion}`
- Videos: `video:{script_hash}:{avatar_id}:{voice_id}`

**Impact**: Re-renders skip redundant AI calls, saving $3-4 per generation.

### 2. BullMQ Priority Queues

```typescript
// Three queues with different priorities
mirror:fast    // Pro users, <2 min SLA
mirror:slow    // Free users, <10 min SLA
mirror:batch   // Bulk API, <1 hour SLA
```

**Job Structure:**
```typescript
{
  id: "job_abc123",
  userId: "user_xyz",
  priority: 10,
  data: {
    audioPath: "s3://...",
    imagePath: "s3://...",
    formats: ["linkedin", "tiktok"],
    languages: ["en", "es"]
  },
  progress: {
    stage: "format",
    percent: 40,
    eta: 45
  }
}
```

### 3. Durable State with PostgreSQL Checkpointer

```python
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver.from_conn_string("postgresql://...")
graph = create_graph().compile(checkpointer=checkpointer)

# Failed jobs resume from last successful node
result = graph.invoke(state, config={"thread_id": job_id})
```

**Impact**: Network failures don't restart entire pipeline.

### 4. Real-Time Progress Streaming

```typescript
// Server-Sent Events endpoint
GET /api/jobs/:id/stream

// Client hook
const { progress, stage, eta } = useJobStream(jobId);

// Progress events
{
  stage: "intake",
  status: "running",
  percent: 10,
  eta: 80,
  message: "Transcribing audio..."
}
```

## Multi-Platform UI Architecture

### Unified Component Library

```
@mirror/ui (shared)
├── Button, Input, Card (primitives)
├── JobProgress, VideoPreview (domain)
└── theme.ts (design tokens)

@mirror/web (Next.js 14)
├── app/
│   ├── (auth)/
│   ├── (dashboard)/
│   └── api/
└── components/

@mirror/mobile (React Native)
├── screens/
├── navigation/
└── native-modules/

@mirror/desktop (Tauri)
├── src-tauri/ (Rust)
└── src/ (React)

@mirror/cli (enhanced)
├── commands/
└── interactive/
```

### State Management

```typescript
// Zustand store (shared across platforms)
interface MirrorStore {
  jobs: Job[];
  user: User;
  credits: number;
  addJob: (job: Job) => void;
  updateJobProgress: (id: string, progress: Progress) => void;
}

// React Query for server state
const { data: jobs } = useJobs();
const { mutate: createJob } = useCreateJob();
```

### API-First Design

```typescript
// OpenAPI 3.1 spec
POST   /api/v1/jobs
GET    /api/v1/jobs/:id
GET    /api/v1/jobs/:id/stream
DELETE /api/v1/jobs/:id
POST   /api/v1/batch
GET    /api/v1/user/credits
POST   /api/v1/voice-clones
GET    /api/v1/templates
```

## Plugin Architecture

```python
# Plugin interface
class MirrorPlugin(ABC):
    @abstractmethod
    def name(self) -> str:
        pass
    
    @abstractmethod
    def run(self, state: MirrorState) -> MirrorState:
        pass
    
    def ui_slot(self) -> Optional[str]:
        """Return React component path for UI injection."""
        return None

# Plugin registry
class PluginRegistry:
    def register(self, plugin: MirrorPlugin):
        self._plugins[plugin.name()] = plugin
    
    def run_all(self, state: MirrorState) -> MirrorState:
        for plugin in self._plugins.values():
            state = plugin.run(state)
        return state

# Example plugin
class BrandKitPlugin(MirrorPlugin):
    def name(self) -> str:
        return "brand_kit"
    
    def run(self, state: MirrorState) -> MirrorState:
        # Inject brand colors, logo, fonts into Hyperframes
        brand = get_user_brand(state["user_id"])
        state["brand_config"] = brand
        return state
    
    def ui_slot(self) -> str:
        return "@mirror/plugins/brand-kit/ui/Settings.tsx"
```

## User Workflows

### 1. Quick Capture (Mobile-First)

```
1. Open PWA on phone
2. Tap mic button
3. Record 60s voice memo
4. Tap "Generate"
5. Get push notification when ready
6. Review + share
```

**Implementation:**
- PWA with Web Audio API
- Background upload to S3
- Push notification via FCM
- Deep link to result

### 2. Scene Editor (Desktop)

```
1. Upload audio + optional image
2. Pipeline generates 5 formats
3. Click any format to open Scene Editor
4. Edit script inline
5. Override prompt per scene
6. Re-render individual scenes
7. Reorder scenes
8. Export final video
```

**Implementation:**
- React DnD for reordering
- Monaco editor for script editing
- Partial re-render API endpoint
- Real-time preview

### 3. Approval Workflow (Agency)

```
1. Creator generates draft
2. Share approval link with client
3. Client adds timestamped comments
4. Creator makes revisions
5. Client approves
6. Export watermark-free video
```

**Implementation:**
- Shareable UUID links
- Comment threads with timestamps
- Version history
- Approval state machine

### 4. Batch API (Enterprise)

```bash
# Submit 50 briefs via API
curl -X POST https://api.mirror.ai/v1/batch \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "jobs": [
      {"audio_url": "s3://...", "formats": ["linkedin"]},
      ...
    ],
    "webhook_url": "https://client.com/webhook"
  }'

# Receive webhook per job
POST https://client.com/webhook
{
  "job_id": "job_abc123",
  "status": "complete",
  "outputs": {
    "linkedin": "https://cdn.mirror.ai/..."
  }
}
```

## Character Consistency Engine

```python
class ConsistencyEngine:
    def __init__(self):
        self.embeddings = {}  # {user_id: {character_id: embedding}}
    
    def register_character(self, user_id: str, image_path: str) -> str:
        """Extract and store character embedding."""
        embedding = self._extract_embedding(image_path)
        char_id = str(uuid.uuid4())
        self.embeddings.setdefault(user_id, {})[char_id] = embedding
        return char_id
    
    def check_drift(self, user_id: str, char_id: str, generated_frame: str) -> float:
        """Measure drift between reference and generated frame."""
        ref_embedding = self.embeddings[user_id][char_id]
        gen_embedding = self._extract_embedding(generated_frame)
        return cosine_similarity(ref_embedding, gen_embedding)
    
    def _extract_embedding(self, image_path: str) -> np.ndarray:
        # Use CLIP or DINOv2 for robust embeddings
        pass
```

**Workflow:**
1. User uploads reference image
2. System extracts character embedding
3. During generation, check each frame
4. If drift > threshold, trigger approval gate
5. User approves or requests re-render

## Deployment Architecture

```
┌─────────────────────────────────────────────┐
│  Cloudflare (CDN + DDoS protection)         │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│  Load Balancer (AWS ALB)                    │
└─────────────────┬───────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
┌───────▼────────┐  ┌──────▼──────────┐
│  Web Tier      │  │  API Tier       │
│  (Next.js)     │  │  (FastAPI)      │
│  ECS Fargate   │  │  ECS Fargate    │
└────────────────┘  └─────────┬───────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
            ┌───────▼────────┐  ┌──────▼──────────┐
            │  Worker Tier   │  │  PostgreSQL     │
            │  (BullMQ)      │  │  (RDS)          │
            │  ECS Fargate   │  └─────────────────┘
            └────────┬───────┘
                     │
            ┌────────▼────────┐
            │  Redis          │
            │  (ElastiCache)  │
            └─────────────────┘
```

## Monitoring Stack

```yaml
# Observability
Metrics: Prometheus + Grafana
Logs: CloudWatch Logs
Traces: OpenTelemetry + Jaeger
Errors: Sentry
Analytics: PostHog

# Key Metrics
- Job success rate (target: >95%)
- P50/P95/P99 latency per stage
- API error rate (target: <1%)
- Credit burn rate per user
- Queue depth (alert if >100)
```

## Security

```yaml
Authentication: Clerk or Auth0
Authorization: RBAC with Casbin
API Keys: Hashed with bcrypt, rate-limited
File Upload: Signed S3 URLs, virus scanning
Secrets: AWS Secrets Manager
Encryption: TLS 1.3, data at rest with KMS
```

## Cost Optimization

```python
# Intelligent routing
def route_job(job: Job) -> str:
    if job.user.tier == "enterprise":
        return "mirror:fast"
    elif job.estimated_cost < 2.0:
        return "mirror:fast"  # Cheap jobs go fast
    else:
        return "mirror:slow"  # Expensive jobs batched

# Spot instances for batch queue
# Reserved instances for fast queue
# Auto-scaling based on queue depth
```

## Developer Experience

```bash
# Local development
make dev          # Start all services
make test         # Run tests
make lint         # Check code quality
make db-migrate   # Run migrations

# CLI enhancements
mirror init       # Interactive setup
mirror dev        # Watch mode with hot reload
mirror deploy     # One-command deploy
mirror logs       # Tail production logs
mirror rollback   # Instant rollback
```

## Next Steps

1. Implement L1/L2 caching (Redis + in-memory)
2. Add BullMQ job queue
3. Build SSE progress streaming
4. Create React component library
5. Design mobile PWA
6. Implement plugin architecture
7. Add character consistency engine
8. Build approval workflow
9. Create batch API
10. Deploy monitoring stack
