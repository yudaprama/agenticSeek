# AgenticSeek Frontend v2

A modern, responsive frontend for AgenticSeek built with React, Vite, Tailwind CSS, and shadcn/ui.

## Features

- 🎨 **Modern UI**: Clean, professional design with shadcn/ui components
- 🖥️ **Desktop-Optimized**: Full-screen layout designed for desktop productivity
- 🌙 **Dark Mode Ready**: Built-in dark mode support
- ⚡ **Fast**: Powered by Vite for lightning-fast development and builds
- 🎯 **Type-Safe**: Built with modern React patterns and best practices

## Tech Stack

- **React 18** - Modern React with hooks
- **Vite** - Next generation frontend tooling
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - High-quality, accessible UI components
- **Lucide React** - Beautiful, customizable icons
- **Axios** - HTTP client for API calls
- **React Markdown** - Markdown rendering

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and navigate to `http://localhost:5173`

### Environment Variables

Create a `.env` file in the root directory:

```env
VITE_BACKEND_URL=http://localhost:8000
```

## Features

### Chat Interface
- Real-time messaging with AgenticSeek agents
- Markdown support for rich text formatting
- Expandable reasoning sections for agent thought processes
- Message history with user and agent differentiation

### Computer View
- **Editor View**: See code execution blocks with syntax highlighting
- **Browser View**: Live screenshots of browser automation
- Real-time status updates and health monitoring

### UI Components
- Full-screen desktop layout with side-by-side panels
- Fixed-height design optimizing screen real estate
- Status badges and indicators
- Smooth animations and transitions
- Accessible design patterns

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Project Structure

```
src/
├── components/
│   └── ui/           # shadcn/ui components
├── lib/
│   └── utils.js      # Utility functions
├── App.jsx           # Main application component
├── main.jsx          # Application entry point
└── index.css         # Global styles and Tailwind imports
```

## Deployment

1. Build the project:
```bash
npm run build
```

2. The `dist` folder contains the production-ready files

3. Deploy to your preferred hosting service (Vercel, Netlify, etc.)

## Comparison with v1

### Improvements
- **Modern Design**: Clean, professional UI vs basic styling
- **Better UX**: Improved layout, navigation, and interactions
- **Performance**: Vite vs Create React App for faster builds
- **Maintainability**: Better component structure and modern patterns
- **Accessibility**: Built-in accessibility features from shadcn/ui
- **Desktop-Optimized**: Full-screen layout maximizing productivity

### Migration
This is a complete rewrite with the same functionality but modern architecture. The API integration remains compatible with the existing backend.
