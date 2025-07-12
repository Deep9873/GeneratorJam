import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Textarea } from './ui/textarea';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  Sparkles, 
  Download, 
  Copy, 
  Heart, 
  History, 
  Trash2,
  Star,
  Clock,
  Hash,
  FileText,
  Image as ImageIcon,
  Zap,
  RefreshCw,
  AlertCircle
} from 'lucide-react';
import { useToast } from '../hooks/use-toast';
import { contentTemplates, getRandomLoadingMessage } from './mock';
import ApiService from '../services/api';

const GeneratorJam = () => {
  const [activeTab, setActiveTab] = useState('generate');
  const [selectedTemplate, setSelectedTemplate] = useState('blog');
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedContent, setGeneratedContent] = useState(null);
  const [history, setHistory] = useState([]);
  const [loadingMessage, setLoadingMessage] = useState('');
  const [historyLoading, setHistoryLoading] = useState(false);
  const [isOnline, setIsOnline] = useState(true);
  const { toast } = useToast();

  // Initialize history from API on mount
  useEffect(() => {
    loadHistory();
    checkHealth();
  }, []);

  // clear out old image/text when the user flips mode or template
useEffect(() => {
  setGeneratedContent(null);
}, [selectedTemplate, activeTab]);



  const checkHealth = async () => {
    try {
      await ApiService.healthCheck();
      setIsOnline(true);
    } catch (error) {
      setIsOnline(false);
      toast({
        title: "Connection Issue",
        description: "Unable to connect to the AI service. Please check your internet connection.",
        variant: "destructive",
      });
    }
  };

  const loadHistory = async () => {
    try {
      setHistoryLoading(true);
      const response = await ApiService.getHistory();
      setHistory(response.items || []);
    } catch (error) {
      console.error('Failed to load history:', error);
      toast({
        title: "History Load Failed",
        description: "Unable to load your generation history.",
        variant: "destructive",
      });
    } finally {
      setHistoryLoading(false);
    }
  };

  const generateContent = async () => {
    if (!prompt.trim()) {
      toast({
        title: "Prompt Required",
        description: "Please enter a prompt to generate content.",
        variant: "destructive",
      });
      return;
    }

    if (!isOnline) {
      toast({
        title: "Offline",
        description: "Please check your internet connection and try again.",
        variant: "destructive",
      });
      return;
    }

    setIsGenerating(true);
    setLoadingMessage(getRandomLoadingMessage());
    
    // Update loading message every 3 seconds
    const loadingInterval = setInterval(() => {
      setLoadingMessage(getRandomLoadingMessage());
    }, 3000);

    try {
      let result;
      
      if (selectedTemplate === 'image') {
        result = await ApiService.generateImageContent(prompt);
        // Format for frontend consumption
        result = {
          url: `data:image/png;base64,${result.image_base64}`,
          prompt: result.prompt,
          dimensions: result.dimensions,
          format: result.format
        };
      } else {
        result = await ApiService.generateTextContent(prompt, selectedTemplate);
      }
      
      setGeneratedContent(result);
      
      // Refresh history to show the new item
      await loadHistory();
      
      clearInterval(loadingInterval);
      setIsGenerating(false);
      setLoadingMessage('');
      
      toast({
        title: "Content Generated!",
        description: `Your ${contentTemplates[selectedTemplate].name.toLowerCase()} has been created successfully.`,
      });
    } catch (error) {
      clearInterval(loadingInterval);
      setIsGenerating(false);
      setLoadingMessage('');
      
      const errorMessage = error.message || 'Something went wrong. Please try again.';
      toast({
        title: "Generation Failed",
        description: errorMessage,
        variant: "destructive",
      });
    }
  };

  const copyToClipboard = async (content) => {
    try {
      const textToCopy = typeof content === 'string' ? content : 
                        content.content || content.title || 'Generated content';
      await navigator.clipboard.writeText(textToCopy);
      toast({
        title: "Copied!",
        description: "Content copied to clipboard.",
      });
    } catch (error) {
      toast({
        title: "Copy Failed",
        description: "Unable to copy content.",
        variant: "destructive",
      });
    }
  };

  const downloadContent = (content, type, filename) => {
    try {
      if (type === 'image') {
        const link = document.createElement('a');
        link.href = content.url;
        link.download = filename || 'generated-image.png';
        link.click();
      } else {
        const textContent = typeof content === 'string' ? content : 
                           content.content || content.title || 'Generated content';
        const blob = new Blob([textContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename || 'generated-content.txt';
        link.click();
        URL.revokeObjectURL(url);
      }
      
      toast({
        title: "Downloaded!",
        description: "Content has been downloaded successfully.",
      });
    } catch (error) {
      toast({
        title: "Download Failed",
        description: "Unable to download content.",
        variant: "destructive",
      });
    }
  };

  const toggleFavorite = async (id) => {
    try {
      await ApiService.toggleFavorite(id);
      
      // Update local state
      setHistory(prev => 
        prev.map(item => 
          item.id === id ? { ...item, is_favorite: !item.is_favorite } : item
        )
      );
      
      toast({
        title: "Updated!",
        description: "Favorite status updated.",
      });
    } catch (error) {
      toast({
        title: "Update Failed",
        description: "Unable to update favorite status.",
        variant: "destructive",
      });
    }
  };

  const deleteHistoryItem = async (id) => {
    try {
      await ApiService.deleteHistoryItem(id);
      setHistory(prev => prev.filter(item => item.id !== id));
      
      toast({
        title: "Deleted",
        description: "History item has been removed.",
      });
    } catch (error) {
      toast({
        title: "Delete Failed",
        description: "Unable to delete history item.",
        variant: "destructive",
      });
    }
  };

  const clearHistory = async () => {
    try {
      await ApiService.clearHistory();
      setHistory([]);
      
      toast({
        title: "History Cleared",
        description: "All history items have been removed.",
      });
    } catch (error) {
      toast({
        title: "Clear Failed",
        description: "Unable to clear history.",
        variant: "destructive",
      });
    }
  };

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="p-3 rounded-2xl">
              <img className="max-w-full h-auto max-h-24 lg:max-h-36" style={{
    width: '47rem',
    height: '9rem'
}} src="/logo.png" alt="Logo" />
            </div>
            {/* <h1 className="text-5xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              Generator Jam
            </h1> */}
          </div>
          <p className="text-base sm:text-lg md:text-xl lg:text-2xl text-gray-600 text-center">
            AI-Powered Content Creation at Your Fingertips
          </p>
          
          {/* Connection Status */}
          <div className="flex items-center justify-center gap-2 mt-4">
            <div className={`w-3 h-3 rounded-full ${isOnline ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-sm text-gray-600">
              {isOnline ? 'Connected to AI Services' : 'Offline - Check Connection'}
            </span>
            <Button
              variant="ghost"
              size="sm"
              onClick={checkHealth}
              className="p-1 h-auto"
            >
              <RefreshCw className="h-3 w-3" />
            </Button>
          </div>
        </div>

        {/* Main Content */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-8">
            <TabsTrigger value="generate" className="flex items-center gap-2">
              <Zap className="h-4 w-4" />
              Generate
            </TabsTrigger>
            <TabsTrigger value="history" className="flex items-center gap-2">
              <History className="h-4 w-4" />
              History ({history.length})
            </TabsTrigger>
          </TabsList>

          <TabsContent value="generate" className="space-y-6">
            {/* Template Selection */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="h-5 w-5" />
                  Choose Content Type
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {Object.entries(contentTemplates).map(([key, template]) => (
                    <Card
                      key={key}
                      className={`cursor-pointer transition-all duration-200 hover:shadow-lg ${
                        selectedTemplate === key
                          ? 'ring-2 ring-purple-500 bg-purple-50'
                          : 'hover:bg-gray-50'
                      }`}
                      onClick={() => setSelectedTemplate(key)}
                    >
                      <CardContent className="p-4">
                        <div className="flex items-center gap-3 mb-2">
                          <span className="text-2xl">{template.icon}</span>
                          <h3 className="font-semibold">{template.name}</h3>
                        </div>
                        <p className="text-sm text-gray-600">{template.description}</p>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Prompt Input */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Sparkles className="h-5 w-5" />
                  Describe What You Want
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <Textarea
                  placeholder={contentTemplates[selectedTemplate].placeholder}
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  className="min-h-32 resize-none"
                  disabled={isGenerating}
                />
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Badge variant="outline">
                      {contentTemplates[selectedTemplate].name}
                    </Badge>
                    <span className="text-xs sm:text-sm md:text-base text-gray-500">
                      {prompt.length} characters
                    </span>
                  </div>
                  <Button
                    onClick={generateContent}
                    disabled={isGenerating || !prompt.trim() || !isOnline}
                    className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
                  >
                    {isGenerating ? (
                      <>
                        <Sparkles className="h-4 w-4 mr-2 animate-spin" />
                        Generating...
                      </>
                    ) : (
                      <>
                        <Sparkles className="h-4 w-4 mr-2" />
                        Generate Content
                      </>
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Loading State */}
            {isGenerating && (
              <Card>
                <CardContent className="p-8">
                  <div className="text-center space-y-4">
                    <div className="flex justify-center">
                      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
                    </div>
                    <p className="text-lg font-medium text-purple-600">
                      {loadingMessage}
                    </p>
                    <div className="w-64 mx-auto bg-gray-200 rounded-full h-2">
                      <div className="bg-gradient-to-r from-purple-600 to-pink-600 h-2 rounded-full animate-pulse w-3/4"></div>
                    </div>
                    <p className="text-sm text-gray-500">
                      {selectedTemplate === 'image' ? 'This may take up to 2 minutes' : 'Usually takes 10-30 seconds'}
                    </p>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Generated Content */}
            {generatedContent && !isGenerating && (
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="flex items-center gap-2">
                      <Star className="h-5 w-5 text-yellow-500" />
                      Generated Content
                    </CardTitle>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => copyToClipboard(generatedContent)}
                      >
                        <Copy className="h-4 w-4 mr-1" />
                        Copy
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => downloadContent(
                          generatedContent,
                          selectedTemplate === 'image' ? 'image' : 'text',
                          `generated-${selectedTemplate}-${Date.now()}.${selectedTemplate === 'image' ? 'png' : 'txt'}`
                        )}
                      >
                        <Download className="h-4 w-4 mr-1" />
                        Download
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  {selectedTemplate === 'image' ? (
                    <div className="space-y-4">
                      <img
                        src={generatedContent.url}
                        alt="Generated"
                        className="w-full max-w-md mx-auto rounded-lg shadow-lg"
                      />
                      <div className="text-center space-y-2">
                        <p className="text-sm text-gray-600">
                          <strong>Prompt:</strong> {generatedContent.prompt}
                        </p>
                        <p className="text-sm text-gray-600">
                          <strong>Dimensions:</strong> {generatedContent.dimensions}
                        </p>
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {generatedContent.title && (
                        <h3 className="text-2xl font-bold text-gray-800">
                          {generatedContent.title}
                        </h3>
                      )}
                      <div className="prose max-w-none">
                        <pre className="whitespace-pre-wrap text-gray-700 font-sans">
                          {typeof generatedContent === 'string'
                              ? generatedContent
                              : generatedContent.content ?? ''}
                        </pre>
                      </div>
                      {generatedContent.hashtags && (
                        <div className="flex flex-wrap gap-2">
                          {generatedContent.hashtags.map((tag, index) => (
                            <Badge key={index} variant="secondary">
                              {tag}
                            </Badge>
                          ))}
                        </div>
                      )}
                      {(generatedContent.word_count || generatedContent.character_count) && (
                        <div className="flex gap-4 text-sm text-gray-600">
                          {generatedContent.word_count && (
                            <span>Words: {generatedContent.word_count}</span>
                          )}
                          {generatedContent.character_count && (
                            <span>Characters: {generatedContent.character_count}</span>
                          )}
                          {generatedContent.reading_time && (
                            <span>Reading time: {generatedContent.reading_time}</span>
                          )}
                        </div>
                      )}
                    </div>
                  )}
                </CardContent>
              </Card>
            )}
          </TabsContent>

          <TabsContent value="history" className="space-y-6">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center gap-2">
                    <History className="h-5 w-5" />
                    Content History
                  </CardTitle>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={loadHistory}
                      disabled={historyLoading}
                    >
                      <RefreshCw className={`h-4 w-4 mr-1 ${historyLoading ? 'animate-spin' : ''}`} />
                      Refresh
                    </Button>
                    {history.length > 0 && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={clearHistory}
                        className="text-red-600 hover:text-red-700"
                      >
                        <Trash2 className="h-4 w-4 mr-1" />
                        Clear All
                      </Button>
                    )}
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                {historyLoading ? (
                  <div className="text-center py-8">
                    <RefreshCw className="h-8 w-8 animate-spin text-purple-600 mx-auto mb-4" />
                    <p className="text-gray-500">Loading your history...</p>
                  </div>
                ) : history.length === 0 ? (
                  <div className="text-center py-8">
                    <History className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                    <p className="text-gray-500">No content generated yet.</p>
                    <p className="text-sm text-gray-400 mt-1">
                      Start generating content to see your history here!
                    </p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {history.map((item) => (
                      <Card key={item.id} className="hover:shadow-md transition-shadow">
                        <CardContent className="p-4">
                          <div className="flex items-start justify-between mb-3">
                            <div className="flex items-center gap-3">
                              <span className="text-2xl">
                                {contentTemplates[item.content_type]?.icon || '📄'}
                              </span>
                              <div>
                                <h4 className="font-semibold text-gray-800">
                                  {contentTemplates[item.content_type]?.name || 'Content'}
                                </h4>
                                <div className="flex items-center gap-2 text-sm text-gray-500">
                                  <Clock className="h-3 w-3" />
                                  {formatDate(item.timestamp)}
                                </div>
                              </div>
                            </div>
                            <div className="flex items-center gap-2">
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => toggleFavorite(item.id)}
                                className={item.is_favorite ? 'text-red-500' : 'text-gray-400'}
                              >
                                <Heart className={`h-4 w-4 ${item.is_favorite ? 'fill-current' : ''}`} />
                              </Button>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => copyToClipboard(item.result)}
                              >
                                <Copy className="h-4 w-4" />
                              </Button>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => downloadContent(
                                  item.result,
                                  item.type,
                                  `${item.content_type}-${item.id}.${item.type === 'image' ? 'png' : 'txt'}`
                                )}
                              >
                                <Download className="h-4 w-4" />
                              </Button>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => deleteHistoryItem(item.id)}
                                className="text-red-500 hover:text-red-700"
                              >
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            </div>
                          </div>
                          <p className="text-sm text-gray-600 mb-3">
                            <strong>Prompt:</strong> {item.prompt}
                          </p>
                          <div className="bg-gray-50 rounded-lg p-3 max-h-32 overflow-y-auto">
                            {item.type === 'image' ? (
                              <img
                                src={item.result.url || `data:image/png;base64,${item.result.image_base64}`}
                                alt="Generated"
                                className="w-20 h-20 object-cover rounded"
                              />
                            ) : (
                              <pre className="text-sm whitespace-pre-wrap text-gray-700 font-sans">
                                {typeof item.result === 'string' 
                                  ? item.result.slice(0, 200) + (item.result.length > 200 ? '...' : '')
                                  : (item.result.content || item.result.title || 'Generated content').slice(0, 200) + '...'
                                }
                              </pre>
                            )}
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default GeneratorJam;