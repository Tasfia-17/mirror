# MIRROR UI/UX Design

## Design Principles

1. **Instant Feedback**: Show progress at every stage
2. **Mobile-First**: One-tap capture on phone
3. **Progressive Disclosure**: Simple by default, powerful when needed
4. **Offline-First**: Cache everything, sync when online
5. **Accessible**: WCAG 2.1 AA compliant

## Platform Experiences

### Web (Next.js 14)

**Landing Page**
```
Hero: "60 seconds of voice. 50 pieces of content."
Demo video (30s loop)
CTA: "Try it free" → Sign up
Social proof: "Used by 10,000+ creators"
```

**Dashboard**
```
┌─────────────────────────────────────────┐
│ MIRROR                    Credits: 120  │
├─────────────────────────────────────────┤
│                                         │
│  ┌───────────────────────────────────┐ │
│  │  Drop audio or click to upload    │ │
│  │  [📁 Browse] [🎤 Record]          │ │
│  └───────────────────────────────────┘ │
│                                         │
│  Recent Jobs                            │
│  ┌─────────────────────────────────┐   │
│  │ ⏳ "Product launch..."  40%     │   │
│  │ ✅ "Weekly update"     Complete │   │
│  │ ❌ "Team intro"        Failed   │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**Job Progress**
```
┌─────────────────────────────────────────┐
│ Generating "Product launch..."          │
├─────────────────────────────────────────┤
│                                         │
│  [████████████░░░░░░░░░░] 60%          │
│                                         │
│  ✅ Intake      (3.2s)                  │
│  ✅ Identity    (4.5s)                  │
│  ✅ Format      (2.1s)                  │
│  ⏳ Cinematic   (estimating...)         │
│  ⏸️  Hyperframes                        │
│  ⏸️  Translate                          │
│                                         │
│  ETA: 45 seconds                        │
└─────────────────────────────────────────┘
```

**Scene Editor**
```
┌─────────────────────────────────────────┐
│ LinkedIn Video                          │
├─────────────────────────────────────────┤
│                                         │
│  [Video Preview]                        │
│                                         │
│  Scene 1 (0:00-0:15)                    │
│  ┌─────────────────────────────────┐   │
│  │ "Did you know that 80% of..."  │   │
│  │ [Edit Script] [Re-render]       │   │
│  └─────────────────────────────────┘   │
│                                         │
│  Scene 2 (0:15-0:30)                    │
│  ┌─────────────────────────────────┐   │
│  │ "Here's why this matters..."    │   │
│  │ [Edit Script] [Re-render]       │   │
│  └─────────────────────────────────┘   │
│                                         │
│  [+ Add Scene] [Export]                 │
└─────────────────────────────────────────┘
```

### Mobile (React Native PWA)

**Home Screen**
```
┌─────────────────┐
│ MIRROR          │
├─────────────────┤
│                 │
│   [  🎤  ]      │
│                 │
│  Tap to record  │
│                 │
│                 │
│  Recent         │
│  ┌───────────┐  │
│  │ Product   │  │
│  │ launch    │  │
│  │ ⏳ 40%    │  │
│  └───────────┘  │
│                 │
│  ┌───────────┐  │
│  │ Weekly    │  │
│  │ update    │  │
│  │ ✅ Done   │  │
│  └───────────┘  │
└─────────────────┘
```

**Recording Flow**
```
1. Tap mic button
2. Record 60s (waveform animation)
3. Tap "Generate"
4. Background upload
5. Push notification when ready
6. Tap notification → View results
```

**Result View**
```
┌─────────────────┐
│ Product launch  │
├─────────────────┤
│                 │
│  [Video Player] │
│                 │
│  LinkedIn       │
│  TikTok         │
│  YouTube        │
│  Sales          │
│  Podcast        │
│                 │
│  [Share] [Edit] │
└─────────────────┘
```

### Desktop (Tauri)

**Main Window**
```
┌─────────────────────────────────────────┐
│ File  Edit  View  Help                  │
├─────────────────────────────────────────┤
│                                         │
│  Sidebar          │  Main Area          │
│  ┌──────────┐    │  ┌────────────────┐ │
│  │ Projects │    │  │ Drop files     │ │
│  │ ────────│    │  │ here           │ │
│  │ Launch   │    │  │                │ │
│  │ Update   │    │  │ [Browse]       │ │
│  │ Intro    │    │  │ [Record]       │ │
│  │          │    │  └────────────────┘ │
│  │ [+ New]  │    │                     │
│  └──────────┘    │  Recent Jobs        │
│                  │  ┌────────────────┐ │
│                  │  │ Product launch │ │
│                  │  │ ⏳ 40%         │ │
│                  │  └────────────────┘ │
└─────────────────────────────────────────┘
```

**Batch Processing**
```
┌─────────────────────────────────────────┐
│ Batch Processing                        │
├─────────────────────────────────────────┤
│                                         │
│  Files (10)                             │
│  ┌─────────────────────────────────┐   │
│  │ ✅ file1.mp3    Complete        │   │
│  │ ⏳ file2.mp3    Processing...   │   │
│  │ ⏸️  file3.mp3    Queued         │   │
│  │ ...                              │   │
│  └─────────────────────────────────┘   │
│                                         │
│  Settings                               │
│  Formats: [x] LinkedIn [x] TikTok       │
│  Languages: [x] English [x] Spanish     │
│                                         │
│  [Start Batch] [Cancel]                 │
└─────────────────────────────────────────┘
```

### CLI (Enhanced)

**Interactive Mode**
```bash
$ mirror

? Select action:
  > Generate from audio
    Batch process
    View jobs
    Settings

? Audio file: voice_memo.mp3
? Add image? (y/N): y
? Image file: product_photo.jpg
? Formats: (Use space to select)
  [x] LinkedIn
  [x] TikTok
  [ ] YouTube
  [x] Sales
  [ ] Podcast

Generating...
[████████████░░░░░░░░░░] 60% (ETA: 45s)

✓ Complete! 3 videos generated.
  linkedin: https://cdn.mirror.ai/abc123.mp4
  tiktok:   https://cdn.mirror.ai/def456.mp4
  sales:    https://cdn.mirror.ai/ghi789.mp4
```

**Watch Mode**
```bash
$ mirror watch ./audio_files

Watching ./audio_files for new files...

[12:34:56] New file: product_launch.mp3
[12:34:57] Generating...
[12:35:42] ✓ Complete! 5 videos generated.

[12:36:12] New file: team_intro.mp3
[12:36:13] Generating...
```

## Component Library

### Design Tokens

```typescript
// colors.ts
export const colors = {
  primary: {
    50: '#f0f9ff',
    500: '#0ea5e9',
    900: '#0c4a6e',
  },
  success: '#10b981',
  warning: '#f59e0b',
  error: '#ef4444',
  neutral: {
    50: '#fafafa',
    500: '#737373',
    900: '#171717',
  },
};

// typography.ts
export const typography = {
  fontFamily: {
    sans: 'Inter, system-ui, sans-serif',
    mono: 'JetBrains Mono, monospace',
  },
  fontSize: {
    xs: '0.75rem',
    sm: '0.875rem',
    base: '1rem',
    lg: '1.125rem',
    xl: '1.25rem',
    '2xl': '1.5rem',
  },
};

// spacing.ts
export const spacing = {
  1: '0.25rem',
  2: '0.5rem',
  4: '1rem',
  8: '2rem',
  16: '4rem',
};
```

### Core Components

```typescript
// Button.tsx
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'ghost';
  size: 'sm' | 'md' | 'lg';
  loading?: boolean;
  icon?: ReactNode;
  children: ReactNode;
}

// JobProgress.tsx
interface JobProgressProps {
  jobId: string;
  stages: Stage[];
  currentStage: string;
  percent: number;
  eta: number;
}

// VideoPreview.tsx
interface VideoPreviewProps {
  url: string;
  format: string;
  duration: number;
  onEdit?: () => void;
  onShare?: () => void;
}

// SceneCard.tsx
interface SceneCardProps {
  scene: Scene;
  onEditScript: (script: string) => void;
  onRerender: () => void;
  onDelete: () => void;
}
```

## User Flows

### 1. First-Time User

```
1. Land on homepage
2. Watch 30s demo video
3. Click "Try it free"
4. Sign up with Google/GitHub
5. Onboarding: "Record a 60s voice memo"
6. Record or upload
7. Wait 90s
8. See 5 videos generated
9. Click LinkedIn video
10. See Scene Editor
11. Edit script inline
12. Re-render scene
13. Export video
14. Prompt: "Share on LinkedIn?"
```

### 2. Power User (Agency)

```
1. Upload 10 client briefs (batch)
2. Set brand kit per client
3. Generate all videos
4. Review in approval queue
5. Add comments per scene
6. Share approval links with clients
7. Clients approve/request changes
8. Export watermark-free videos
9. Auto-publish to client channels
10. View analytics dashboard
```

### 3. Mobile Creator

```
1. Open PWA on phone
2. Tap mic button
3. Record 60s idea
4. Tap "Generate"
5. Lock phone, go about day
6. Get push notification (2 min later)
7. Tap notification
8. Swipe through 5 videos
9. Tap "Share to TikTok"
10. TikTok opens with video pre-loaded
```

## Accessibility

- Keyboard navigation for all actions
- Screen reader support with ARIA labels
- High contrast mode
- Reduced motion mode
- Captions on all demo videos
- Alt text on all images
- Focus indicators
- Error messages with recovery actions

## Performance

- Code splitting per route
- Image optimization with Next.js Image
- Lazy loading for video previews
- Service worker for offline support
- IndexedDB for local job cache
- Optimistic UI updates
- Skeleton screens during loading
- Debounced search and filters

## Responsive Breakpoints

```css
/* Mobile */
@media (max-width: 640px) { }

/* Tablet */
@media (min-width: 641px) and (max-width: 1024px) { }

/* Desktop */
@media (min-width: 1025px) { }

/* Large Desktop */
@media (min-width: 1440px) { }
```

## Dark Mode

All components support dark mode via CSS variables:

```css
:root {
  --bg-primary: #ffffff;
  --text-primary: #171717;
}

[data-theme="dark"] {
  --bg-primary: #0a0a0a;
  --text-primary: #fafafa;
}
```

## Animation

```typescript
// Framer Motion variants
const fadeIn = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
};

const slideIn = {
  initial: { x: -100, opacity: 0 },
  animate: { x: 0, opacity: 1 },
};

const stagger = {
  animate: {
    transition: {
      staggerChildren: 0.1,
    },
  },
};
```

## Next Steps

1. Build Figma design system
2. Implement component library in Storybook
3. Create Next.js web app
4. Build React Native mobile app
5. Create Tauri desktop app
6. Enhance CLI with interactive mode
7. User testing with 10 creators
8. Iterate based on feedback
