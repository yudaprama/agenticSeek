import { useState, useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import axios from 'axios';
import { 
  Send, 
  Square, 
  Code, 
  Monitor, 
  ChevronDown, 
  ChevronRight, 
  Brain,
  Wifi,
  WifiOff,
  User,
  Bot
} from 'lucide-react';

import { Button } from './components/ui/button';
import { Input } from './components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';
import { Badge } from './components/ui/badge';
import { ScrollArea } from './components/ui/scroll-area';
import { cn } from './lib/utils';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

function App() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentView, setCurrentView] = useState('blocks');
  const [responseData, setResponseData] = useState(null);
  const [isOnline, setIsOnline] = useState(false);
  const [status, setStatus] = useState('Agents ready');
  const [expandedReasoning, setExpandedReasoning] = useState(new Set());
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const intervalId = setInterval(() => {
      checkHealth();
      fetchLatestAnswer();
      fetchScreenshot();
    }, 3000);
    return () => clearInterval(intervalId);
  }, [messages]);

  const checkHealth = async () => {
    try {
      await axios.get(`${BACKEND_URL}/health`);
      setIsOnline(true);
    } catch {
      setIsOnline(false);
    }
  };

  const fetchScreenshot = async () => {
    try {
      const timestamp = new Date().getTime();
      const res = await axios.get(`${BACKEND_URL}/screenshots/updated_screen.png?timestamp=${timestamp}`, {
        responseType: 'blob'
      });
      const imageUrl = URL.createObjectURL(res.data);
      setResponseData((prev) => {
        if (prev?.screenshot && prev.screenshot !== 'placeholder.png') {
          URL.revokeObjectURL(prev.screenshot);
        }
        return {
          ...prev,
          screenshot: imageUrl,
          screenshotTimestamp: new Date().getTime()
        };
      });
    } catch (err) {
      setResponseData((prev) => ({
        ...prev,
        screenshot: 'placeholder.png',
        screenshotTimestamp: new Date().getTime()
      }));
    }
  };

  const normalizeAnswer = (answer) => {
    return answer
      .trim()
      .toLowerCase()
      .replace(/\s+/g, ' ')
      .replace(/[.,!?]/g, '')
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const toggleReasoning = (messageIndex) => {
    setExpandedReasoning(prev => {
      const newSet = new Set(prev);
      if (newSet.has(messageIndex)) {
        newSet.delete(messageIndex);
      } else {
        newSet.add(messageIndex);
      }
      return newSet;
    });
  };

  const fetchLatestAnswer = async () => {
    try {
      const res = await axios.get(`${BACKEND_URL}/latest_answer`);
      const data = res.data;

      updateData(data);
      if (!data.answer || data.answer.trim() === '') {
        return;
      }
      const normalizedNewAnswer = normalizeAnswer(data.answer);
      const answerExists = messages.some(
        (msg) => normalizeAnswer(msg.content) === normalizedNewAnswer
      );
      if (!answerExists) {
        setMessages((prev) => [
          ...prev,
          {
            type: 'agent',
            content: data.answer,
            reasoning: data.reasoning,
            agentName: data.agent_name,
            status: data.status,
            uid: data.uid,
          },
        ]);
        setStatus(data.status);
        scrollToBottom();
      }
    } catch (error) {
      console.error('Error fetching latest answer:', error);
    }
  };

  const updateData = (data) => {
    setResponseData((prev) => ({
      ...prev,
      blocks: data.blocks || prev?.blocks || null,
      done: data.done,
      answer: data.answer,
      agent_name: data.agent_name,
      status: data.status,
      uid: data.uid,
    }));
  };

  const handleStop = async (e) => {
    e.preventDefault();
    checkHealth();
    setIsLoading(false);
    setError(null);
    try {
      await axios.get(`${BACKEND_URL}/stop`);
      setStatus("Requesting stop...");
    } catch (err) {
      console.error('Error stopping the agent:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    checkHealth();
    if (!query.trim()) {
      return;
    }
    setMessages((prev) => [...prev, { type: 'user', content: query }]);
    setIsLoading(true);
    setError(null);

    try {
      const res = await axios.post(`${BACKEND_URL}/query`, {
        query,
        tts_enabled: false
      });
      const data = res.data;
      updateData(data);
    } catch (err) {
      console.error('Error:', err);
      setError('Failed to process query.');
      setMessages((prev) => [
        ...prev,
        { type: 'error', content: 'Error: Unable to get a response.' },
      ]);
    } finally {
      setIsLoading(false);
      setQuery('');
    }
  };

  return (
    <div className="h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 flex flex-col">
      {/* Header */}
      <header className="border-b bg-white/90 backdrop-blur-sm dark:bg-slate-900/90 px-6 py-3 flex-shrink-0">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              AgenticSeek
            </h1>
          </div>
          <div className="flex items-center space-x-3">
            <Badge variant={isOnline ? "success" : "destructive"} className="flex items-center space-x-1">
              {isOnline ? <Wifi className="w-3 h-3" /> : <WifiOff className="w-3 h-3" />}
              <span>{isOnline ? 'Online' : 'Offline'}</span>
            </Badge>
            <Badge variant="outline" className="text-sm">
              {status}
            </Badge>
          </div>
        </div>
      </header>

      <div className="flex-1 flex gap-4 p-4 min-h-0">
        <div className="flex flex-col w-1/2 min-h-0">
          {/* Chat Section */}
          <Card className="flex flex-col h-full">
            <CardHeader className="pb-3 px-4 py-3 flex-shrink-0">
              <CardTitle className="flex items-center space-x-2 text-lg">
                <User className="w-5 h-5" />
                <span>Chat Interface</span>
              </CardTitle>
            </CardHeader>
            <CardContent className="flex-1 flex flex-col p-0 min-h-0">
              <ScrollArea className="flex-1 px-4 min-h-0">
                <div className="space-y-3 pb-4">
                  {messages.length === 0 ? (
                    <div className="text-center text-muted-foreground py-12">
                      <Bot className="w-16 h-16 mx-auto mb-4 opacity-50" />
                      <p className="text-lg">No messages yet. Type below to start!</p>
                    </div>
                  ) : (
                    messages.map((msg, index) => (
                      <div key={index} className="space-y-2">
                        <div className={cn(
                          "flex",
                          msg.type === 'user' ? 'justify-end' : 'justify-start'
                        )}>
                          <div className={cn(
                            "max-w-[85%] rounded-lg px-4 py-3",
                            msg.type === 'user'
                              ? 'bg-primary text-primary-foreground'
                              : msg.type === 'error'
                              ? 'bg-destructive text-destructive-foreground'
                              : 'bg-muted'
                          )}>
                            {msg.type === 'agent' && (
                              <div className="flex items-center space-x-2 mb-2">
                                <Bot className="w-4 h-4" />
                                <span className="text-xs font-medium">{msg.agentName}</span>
                              </div>
                            )}
                            <div className="prose prose-sm max-w-none dark:prose-invert">
                              <ReactMarkdown>{msg.content}</ReactMarkdown>
                            </div>
                          </div>
                        </div>
                        
                        {msg.type === 'agent' && msg.reasoning && (
                          <div className="ml-4">
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => toggleReasoning(index)}
                              className="h-6 px-2 text-xs"
                            >
                              {expandedReasoning.has(index) ? (
                                <ChevronDown className="w-3 h-3 mr-1" />
                              ) : (
                                <ChevronRight className="w-3 h-3 mr-1" />
                              )}
                              <Brain className="w-3 h-3 mr-1" />
                              Reasoning
                            </Button>
                            {expandedReasoning.has(index) && (
                              <div className="mt-2 p-3 bg-muted/50 rounded-md text-sm">
                                <ReactMarkdown>{msg.reasoning}</ReactMarkdown>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    ))
                  )}
                  <div ref={messagesEndRef} />
                </div>
              </ScrollArea>

              {/* Input Form */}
              <div className="border-t p-4 flex-shrink-0">
                <form onSubmit={handleSubmit} className="flex space-x-3">
                  <Input
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Type your query..."
                    disabled={isLoading || !isOnline}
                    className="flex-1 h-10"
                  />
                  <Button type="submit" disabled={isLoading || !isOnline} size="default" className="px-6">
                    <Send className="w-4 h-4 mr-2" />
                    Send
                  </Button>
                  <Button
                    type="button"
                    variant="outline"
                    onClick={handleStop}
                    size="default"
                    className="px-4"
                  >
                    <Square className="w-4 h-4 mr-2" />
                    Stop
                  </Button>
                </form>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Computer View Section */}
        <div className="flex flex-col w-1/2 min-h-0">
          <Card className="flex flex-col h-full">
            <CardHeader className="pb-3 px-4 py-3 flex-shrink-0">
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center space-x-2 text-lg">
                  <Monitor className="w-5 h-5" />
                  <span>Computer View</span>
                </CardTitle>
                <div className="flex space-x-1">
                  <Button
                    variant={currentView === 'blocks' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setCurrentView('blocks')}
                  >
                    <Code className="w-4 h-4 mr-2" />
                    Editor
                  </Button>
                  <Button
                    variant={currentView === 'screenshot' ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setCurrentView('screenshot')}
                  >
                    <Monitor className="w-4 h-4 mr-2" />
                    Browser
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent className="flex-1 p-0 min-h-0">
              <ScrollArea className="h-full px-4 pb-4 min-h-0">
                {error && (
                  <div className="mb-4 p-3 bg-destructive/10 border border-destructive/20 rounded-md text-destructive text-sm">
                    {error}
                  </div>
                )}
                
                {currentView === 'blocks' ? (
                  <div className="space-y-3">
                    {responseData && responseData.blocks && Object.values(responseData.blocks).length > 0 ? (
                      Object.values(responseData.blocks).map((block, index) => (
                        <Card key={index} className="border-l-4 border-l-blue-500">
                          <CardHeader className="pb-2 px-3 py-2">
                            <div className="flex items-center justify-between">
                              <Badge variant="outline" className="text-xs">{block.tool_type}</Badge>
                              <Badge variant={block.success ? "success" : "destructive"} className="text-xs">
                                {block.success ? 'Success' : 'Failure'}
                              </Badge>
                            </div>
                          </CardHeader>
                          <CardContent className="space-y-2 px-3 pb-3">
                            <div className="bg-muted rounded-md p-3">
                              <pre className="text-sm overflow-x-auto font-mono">{block.block}</pre>
                            </div>
                            {block.feedback && (
                              <div className="text-sm text-muted-foreground">
                                <strong>Feedback:</strong> {block.feedback}
                              </div>
                            )}
                          </CardContent>
                        </Card>
                      ))
                    ) : (
                      <Card className="border-dashed h-full">
                        <CardContent className="flex flex-col items-center justify-center h-full text-center py-12">
                          <Code className="w-16 h-16 text-muted-foreground mb-4" />
                          <p className="text-muted-foreground text-lg">No tools in use</p>
                          <p className="text-sm text-muted-foreground">Code execution will appear here</p>
                        </CardContent>
                      </Card>
                    )}
                  </div>
                ) : (
                  <div className="h-full">
                    <Card className="h-full">
                      <CardContent className="p-4 h-full">
                        <img
                          src={responseData?.screenshot || '/placeholder.png'}
                          alt="Browser Screenshot"
                          className="w-full h-full object-contain rounded-md border"
                          onError={(e) => {
                            e.target.src = '/placeholder.png';
                          }}
                          key={responseData?.screenshotTimestamp || 'default'}
                        />
                      </CardContent>
                    </Card>
                  </div>
                )}
              </ScrollArea>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

export default App;
