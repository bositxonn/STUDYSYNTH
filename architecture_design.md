# AI-Powered Online Learning Platform - Architecture & Design

## 1. System Architecture

The platform follows a modern, decoupled client-server architecture:

1. **Frontend (Client)**: 
   - Built with **Next.js** (React) using Server-Side Rendering (SSR) and Static Site Generation (SSG) for SEO and performance.
   - **Tailwind CSS** for responsive, utility-first styling.
   - State management via React Context or Zustand. Data fetching via React Query.
   - Communicates with the backend via RESTful APIs.

2. **Backend (API Server)**:
   - Built with **NestJS** (Node.js) for structured, scalable, and maintainable enterprise-grade code (uses TypeScript natively).
   - Serves as a RESTful API.
   - Integrates with external services: **Stripe** (Payments), **AWS S3** (Video storage & streaming), **OpenAI API** (Quiz generation).

3. **Database Layer**:
   - **PostgreSQL**: Relational database strictly ensuring data integrity for users, courses, and payments.
   - **Prisma ORM**: Type-safe interactions with the DB.

4. **Authentication & Authorization**:
   - **JWT (JSON Web Tokens)** stored in HttpOnly cookies for session management.
   - Role-based access control (RBAC) via NestJS Guards.

5. **AI Service Layer**:
   - Dedicated backend service modules interact with OpenAI API to generate testing material from video transcripts and user profiles.

---

## 2. Database Schema (PostgreSQL)

```dbml
Table Users {
  id String [pk]
  email String [unique]
  passwordHash String
  name String
  avatarUrl String
  role Enum [default: 'STUDENT', note: 'STUDENT or ADMIN']
  createdAt DateTime
  updatedAt DateTime
}

Table Subscriptions {
  id String [pk]
  userId String [ref: > Users.id]
  stripeCustomerId String
  stripeSubscriptionId String
  plan Enum [default: 'FREE', note: 'FREE, BASIC, PREMIUM']
  status String [note: 'active, canceled, past_due']
  currentPeriodEnd DateTime
}

Table Fields {
  id String [pk]
  name String
  slug String [unique]
}

Table Categories {
  id String [pk]
  fieldId String [ref: > Fields.id]
  name String
  slug String [unique]
}

Table Courses {
  id String [pk]
  categoryId String [ref: > Categories.id]
  title String
  description Text
  difficulty String [note: 'Beginner, Intermediate, Advanced']
  instructorId String [ref: > Users.id]
  coverImageUrl String
  createdAt DateTime
}

Table Lessons {
  id String [pk]
  courseId String [ref: > Courses.id]
  title String
  videoUrl String
  transcript Text
  orderIndex Int
}

Table Progress {
  id String [pk]
  userId String [ref: > Users.id]
  lessonId String [ref: > Lessons.id]
  isCompleted Boolean [default: false]
  watchTimeSeconds Int
}

Table Quizzes {
  id String [pk]
  lessonId String [ref: > Lessons.id]
  title String
  passingScore Int
}

Table Questions {
  id String [pk]
  quizId String [ref: > Quizzes.id]
  text String
  type String [note: 'MULTIPLE_CHOICE, TRUE_FALSE, SHORT_ANSWER']
  options Json [note: 'Array of choices if applicable']
  correctAnswer String
}

Table Results {
  id String [pk]
  userId String [ref: > Users.id]
  quizId String [ref: > Quizzes.id]
  score Int
  passed Boolean
  createdAt DateTime
}
```

---

## 3. API Endpoints

### Auth
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Authenticate and return JWT
- `POST /api/auth/logout` - Clear JWT cookie
- `POST /api/auth/reset-password` - Request password reset

### Users
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update profile
- `GET /api/users/me/progress` - Get user's course progress

### Subscriptions
- `POST /api/subscriptions/checkout` - Create Stripe checkout session
- `POST /api/subscriptions/webhook` - Stripe webhook for status updates
- `GET /api/subscriptions/plan` - Get current user plan

### Courses & Lessons
- `GET /api/courses` - List courses (pagination, filtering)
- `GET /api/courses/:id` - Get course details + lessons list
- `GET /api/lessons/:id` - Get lesson details (requires active sub)
- `POST /api/lessons/:id/complete` - Mark lesson as completed

### Quizzes (AI-Powered)
- `POST /api/quizzes/generate/:lessonId` - AI generates quiz from transcript
- `GET /api/quizzes/:lessonId` - Get quiz for lesson
- `POST /api/quizzes/:id/submit` - Submit answers and get result

### Admin (RBAC Protected)
- `POST /api/admin/courses` - Create a course
- `PUT /api/admin/courses/:id` - Edit a course
- `POST /api/admin/lessons` - Upload and create a lesson
- `GET /api/admin/analytics` - View platform stats

---

## 4. Folder Structure

### Frontend (Next.js)
```text
frontend/
├── src/
│   ├── app/                 # Next.js 13+ App Router
│   │   ├── (auth)/          # login, register
│   │   ├── (dashboard)/     # progress, active courses
│   │   ├── courses/         # catalog, course details
│   │   ├── lessons/         # video player, quiz
│   │   └── admin/           # admin panel
│   ├── components/
│   │   ├── ui/              # Buttons, Inputs, Modals (Tailwind)
│   │   ├── courses/         # CourseCard, VideoPlayer
│   │   └── quizzes/         # QuizForm, ResultCard
│   ├── lib/                 # Utilities, API client (Axios)
│   ├── hooks/               # Custom React hooks
│   └── store/               # Zustand state
├── tailwind.config.js
└── package.json
```

### Backend (NestJS)
```text
backend/
├── src/
│   ├── auth/                # JWT strategy, Guards, Services
│   ├── users/               # User CRUD
│   ├── subscriptions/       # Stripe integration
│   ├── courses/             # Courses & Categories
│   ├── lessons/             # Video handling, AWS S3
│   ├── quizzes/             # AI generation logic
│   ├── ai/                  # OpenAI service wrappers
│   ├── prisma/              # Prisma client and schema
│   ├── common/              # Decorators, Exceptions, Interceptors
│   └── app.module.ts
├── prisma/
│   └── schema.prisma        # Database schema
├── docker-compose.yml
└── package.json
```

---

## 5. Key Code Examples

### A. Auth System (NestJS JWT Strategy)

```typescript
// backend/src/auth/jwt.strategy.ts
import { Injectable, UnauthorizedException } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ExtractJwt, Strategy } from 'passport-jwt';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(private prisma: PrismaService) {
    super({
      jwtFromRequest: ExtractJwt.fromExtractors([
        (request) => {
          return request?.cookies?.Authentication;
        },
      ]),
      ignoreExpiration: false,
      secretOrKey: process.env.JWT_SECRET,
    });
  }

  async validate(payload: any) {
    const user = await this.prisma.user.findUnique({ where: { id: payload.sub } });
    if (!user) throw new UnauthorizedException();
    return user; // Attached to Request as req.user
  }
}
```

### B. Subscription Middleware / Guard

```typescript
// backend/src/common/guards/subscription.guard.ts
import { Injectable, CanActivate, ExecutionContext, ForbiddenException } from '@nestjs/common';
import { Reflector } from '@nestjs/core';

@Injectable()
export class SubscriptionGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredPlans = this.reflector.get<string[]>('plans', context.getHandler());
    if (!requiredPlans) return true; // No specific plan required

    const request = context.switchToHttp().getRequest();
    const user = request.user;

    if (!user || !user.subscription) {
      throw new ForbiddenException('No active subscription found.');
    }

    if (!requiredPlans.includes(user.subscription.plan) && user.role !== 'ADMIN') {
      throw new ForbiddenException('Upgrade your plan to access this content.');
    }

    return true;
  }
}

// Usage in Controller
// @UseGuards(JwtAuthGuard, SubscriptionGuard)
// @Plans('PREMIUM')
// @Get(':id/video')
```

### C. AI Quiz Generation (OpenAI Integration)

```typescript
// backend/src/ai/ai.service.ts
import { Injectable } from '@nestjs/common';
import { OpenAI } from 'openai';

@Injectable()
export class AiService {
  private openai: OpenAI;

  constructor() {
    this.openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
  }

  async generateQuizFromTranscript(transcript: string) {
    const prompt = `
      Based on the following lesson transcript, generate a 5-question quiz.
      Include a mix of multiple-choice and true/false questions.
      Format the output strictly as a JSON array of objects with keys: 
      "text", "type" ("MULTIPLE_CHOICE" or "TRUE_FALSE"), "options" (array of strings, empty for T/F), and "correctAnswer".
      
      Transcript: ${transcript}
    `;

    const response = await this.openai.chat.completions.create({
      model: 'gpt-4',
      messages: [{ role: 'system', content: prompt }],
      temperature: 0.3,
    });

    try {
      return JSON.parse(response.choices[0].message.content);
    } catch (error) {
      throw new Error('Failed to parse AI quiz generation response.');
    }
  }
}
```

---

## 6. UI Layout Descriptions

### Global Theme
- **Colors**: Primary: Soft Blue (`#3B82F6`), Background: Off-white (`#F9FAFB`), Text: Dark Slate (`#1E293B`), Accents: Subtle gradients (Blue to Indigo).
- **Typography**: Inter (clean, modern sans-serif).
- **Components**: Rounded corners (`rounded-xl`), slight drop shadows, glassmorphism on sticky headers.

### Landing Page
- **Hero Section**: Catchy title, gradient text, "Start Learning for Free" CTA, and a 3D isometric illustration of learning.
- **Features**: Grid showing AI testing, video streaming, trackable progress.
- **Pricing**: 3 clear cards (Free, Basic, Premium) with a toggle for Monthly/Annually.

### Dashboard (User)
- **Sidebar (Collapsible)**: Links to Home, My Courses, Achievements, Settings.
- **Main Content**:
  - **Top bar**: User avatar, notifications, current streak.
  - **In Progress**: Carousel of cards showing paused video thumbnails with a progress bar.
  - **AI Recommendations**: Horizontal row of course cards based on past completions.

### Video Lesson Page
- **Layout**: 
  - Left / Main (70%): Large video player. Below it: Tabs for Description, Transcript, Resources.
  - Right (30%): Scrollable list of lessons in the current course. Checkmarks next to completed ones. Locked icons on future ones.
- **Interaction**: Video finishes -> Screen dims -> "Ready for the Quiz?" overlay appears to transition to the testing phase.

### Quiz Page (AI Generated)
- **Layout**: Focused, distraction-free center card.
- **Content**: 
  - Progress bar at the top (e.g., Question 2 of 5).
  - Clean radio buttons for answers.
  - Instant AI-generated feedback pop-up upon submission explaining *why* the answer was wrong.

---

## 7. Deployment Guide

### Infrastructure overview
- **Frontend**: Vercel (optimal for Next.js).
- **Backend**: AWS ECS (Elastic Container Service) or DigitalOcean App Platform via Docker.
- **Database**: Managed PostgreSQL (AWS RDS or Supabase).
- **Storage**: AWS S3 (with CloudFront CDN for fast video delivery).

### Docker setup for Backend

**Dockerfile**
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
COPY prisma ./prisma/
RUN npm ci
COPY . .
RUN npx prisma generate
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/prisma ./prisma

EXPOSE 3000
CMD ["npm", "run", "start:prod"]
```

### Steps to Deploy
1. **Database Setup**: Provision a PostgreSQL database and run `npx prisma db push` to generate tables.
2. **Environment Variables**: Configure secrets (`DATABASE_URL`, `JWT_SECRET`, `STRIPE_SECRET_KEY`, `OPENAI_API_KEY`, `AWS_KEYS`) in your hosting environment.
3. **Backend Deployment**: Push your Docker image to a registry (Docker Hub/ECR) and deploy to your server container engine.
4. **Frontend Deployment**: Connect your GitHub repo to Vercel, set the `NEXT_PUBLIC_API_URL` to point to your deployed backend, and hit "Deploy". Built-in Edge Network will serve the UI globally.
5. **Storage Configuration**: Set up CORS on your AWS S3 bucket to only allow requests from your frontend domain. Enable CloudFront caching.
6. **Webhooks Setup**: Configure Stripe to send subscription lifecycle events to your `/api/subscriptions/webhook` endpoint.
