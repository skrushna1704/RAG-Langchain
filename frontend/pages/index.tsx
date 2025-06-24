import { useState, useEffect, useRef } from 'react';
import { Upload, Send, FileText, Trash2, Brain, Database, Clock, Sparkles, MessageCircle, FolderOpen } from 'lucide-react';

interface Document {
  id: string;
  filename: string;
  upload_date: string;
  chunk_count: number;
  content_preview: string;
}

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  sources?: any[];
  confidence_score?: number;
  processing_time?: number;
}

interface Stats {
  total_documents: number;
  total_chunks: number;
  vector_db_size: number;
  system_status: string;
}

export default function Home() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [stats, setStats] = useState<Stats | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

  useEffect(() => {
    fetchDocuments();
    fetchStats();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchDocuments = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/documents/`);
      const data = await response.json();
      setDocuments(data.documents);
    } catch (error) {
      console.error('Error fetching documents:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/stats/`);
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const handleFileUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch(`${API_BASE_URL}/documents/upload`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      console.log('Upload successful:', data);
      setSelectedFile(null);
      fetchDocuments();
      fetchStats();
    } catch (error) {
      console.error('Upload error:', error);
      alert('Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteDocument = async (documentId: string) => {
    try {
      await fetch(`${API_BASE_URL}/documents/${documentId}`, {
        method: 'DELETE',
      });
      fetchDocuments();
      fetchStats();
    } catch (error) {
      console.error('Delete error:', error);
    }
  };

  const handleAskQuestion = async () => {
    if (!question.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: question,
    };

    setMessages(prev => [...prev, userMessage]);
    setQuestion('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/qa/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question,
        }),
      });

      const data = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: data.answer,
        sources: data.sources,
        confidence_score: data.confidence_score,
        processing_time: data.processing_time,
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error asking question:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: 'Sorry, I encountered an error while processing your question. Please try again.',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Header */}
      <header className="backdrop-blur-lg bg-white/80 shadow-xl border-b border-white/20 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-3 sm:py-6">
            <div className="flex items-center space-x-2 sm:space-x-4">
              <div className="relative">
                <Brain className="h-8 w-8 sm:h-10 sm:w-10 text-gradient bg-gradient-to-r from-blue-600 to-purple-600 p-1.5 sm:p-2 rounded-xl bg-white shadow-lg" />
                <Sparkles className="h-3 w-3 sm:h-4 sm:w-4 text-yellow-400 absolute -top-0.5 -right-0.5 sm:-top-1 sm:-right-1" />
              </div>
              <div>
                <h1 className="text-lg sm:text-2xl lg:text-3xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent">
                  RAG Intelligence
                </h1>
                <p className="text-xs sm:text-sm text-gray-500 font-medium hidden sm:block">Document Intelligence Platform</p>
              </div>
            </div>
            <div className="flex items-center space-x-2 sm:space-x-6">
              <div className="flex items-center space-x-1 sm:space-x-2 bg-white/70 backdrop-blur-sm px-2 sm:px-4 py-1 sm:py-2 rounded-full shadow-md">
                <Database className="h-4 w-4 sm:h-5 sm:w-5 text-blue-600" />
                <span className="font-semibold text-gray-700 text-sm">{stats?.total_documents || 0}</span>
                <span className="text-xs sm:text-sm text-gray-500 hidden sm:inline">docs</span>
              </div>
              <div className="flex items-center space-x-1 sm:space-x-2 bg-white/70 backdrop-blur-sm px-2 sm:px-4 py-1 sm:py-2 rounded-full shadow-md">
                <FileText className="h-4 w-4 sm:h-5 sm:w-5 text-purple-600" />
                <span className="font-semibold text-gray-700 text-sm">{stats?.total_chunks || 0}</span>
                <span className="text-xs sm:text-sm text-gray-500 hidden sm:inline">chunks</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 py-4 sm:py-8">
        <div className="flex flex-col lg:grid lg:grid-cols-3 gap-4 sm:gap-8">
          {/* Document Management */}
          <div className="lg:col-span-1 space-y-4 sm:space-y-6 order-2 lg:order-1">
            {/* Upload Section */}
            <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-xl border border-white/20 p-4 sm:p-6 hover:shadow-2xl transition-all duration-300">
              <div className="flex items-center space-x-2 sm:space-x-3 mb-4 sm:mb-6">
                <Upload className="h-5 w-5 sm:h-6 sm:w-6 text-blue-600" />
                <h2 className="text-lg sm:text-xl font-bold text-gray-800">Upload Documents</h2>
              </div>
              
              <div className="mb-4 sm:mb-6">
                <div className="relative border-2 border-dashed border-blue-200 rounded-2xl p-4 sm:p-8 text-center bg-gradient-to-br from-blue-50 to-indigo-50 hover:from-blue-100 hover:to-indigo-100 transition-all duration-300 group">
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-600/5 to-purple-600/5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                  <Upload className="mx-auto h-12 w-12 sm:h-16 sm:w-16 text-blue-400 group-hover:text-blue-600 transition-colors duration-300" />
                  <div className="mt-4 sm:mt-6 relative z-10">
                    <input
                      type="file"
                      accept=".txt,.pdf,.docx,.md"
                      onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
                      className="hidden"
                      id="file-upload"
                    />
                    <label
                      htmlFor="file-upload"
                      className="cursor-pointer bg-gradient-to-r from-blue-600 to-blue-700 text-white px-4 sm:px-8 py-2 sm:py-3 rounded-xl hover:from-blue-700 hover:to-blue-800 transform hover:scale-105 transition-all duration-200 shadow-lg font-semibold text-sm sm:text-base"
                    >
                      Choose File
                    </label>
                  </div>
                  {selectedFile && (
                    <div className="mt-3 sm:mt-4 bg-white/80 backdrop-blur-sm rounded-lg p-2 sm:p-3 border border-blue-200">
                      <p className="text-xs sm:text-sm font-medium text-gray-700 truncate">{selectedFile.name}</p>
                    </div>
                  )}
                </div>
                
                {selectedFile && (
                  <button
                    onClick={handleFileUpload}
                    disabled={uploading}
                    className="mt-4 sm:mt-6 w-full bg-gradient-to-r from-green-600 to-emerald-600 text-white py-2 sm:py-3 px-4 sm:px-6 rounded-xl hover:from-green-700 hover:to-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg font-semibold text-sm sm:text-base"
                  >
                    {uploading ? (
                      <div className="flex items-center justify-center space-x-2">
                        <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                        <span>Uploading...</span>
                      </div>
                    ) : (
                      'Upload Document'
                    )}
                  </button>
                )}
              </div>
            </div>

            {/* Documents List */}
            <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-xl border border-white/20 p-4 sm:p-6 hover:shadow-2xl transition-all duration-300">
              <div className="flex items-center space-x-2 sm:space-x-3 mb-4 sm:mb-6">
                <FolderOpen className="h-5 w-5 sm:h-6 sm:w-6 text-purple-600" />
                <h3 className="text-lg sm:text-xl font-bold text-gray-800">Your Documents</h3>
              </div>
              
              <div className="space-y-3 sm:space-y-4 max-h-64 sm:max-h-96 overflow-y-auto">
                {documents.map((doc) => (
                  <div key={doc.id} className="group bg-gradient-to-r from-white to-gray-50 border border-gray-200 rounded-xl p-3 sm:p-4 hover:shadow-lg hover:border-blue-300 transition-all duration-300">
                    <div className="flex justify-between items-start">
                      <div className="flex-1 min-w-0">
                        <h4 className="font-bold text-gray-800 mb-1 sm:mb-2 text-sm sm:text-base truncate">{doc.filename}</h4>
                        <div className="flex flex-col sm:flex-row sm:items-center sm:space-x-4 text-xs text-gray-500 mb-1 sm:mb-2 space-y-1 sm:space-y-0">
                          <span className="bg-blue-100 text-blue-700 px-2 py-1 rounded-full font-medium inline-block w-fit">
                            {doc.chunk_count} chunks
                          </span>
                          <span className="flex items-center space-x-1">
                            <Clock className="h-3 w-3" />
                            <span>{formatDate(doc.upload_date)}</span>
                          </span>
                        </div>
                        <p className="text-xs text-gray-600 bg-gray-50 p-2 rounded-lg border-l-4 border-blue-200 truncate">
                          {doc.content_preview}
                        </p>
                      </div>
                      <button
                        onClick={() => handleDeleteDocument(doc.id)}
                        className="text-gray-400 hover:text-red-500 ml-2 sm:ml-4 p-1 sm:p-2 rounded-lg hover:bg-red-50 transition-all duration-200 opacity-100 sm:opacity-0 group-hover:opacity-100 flex-shrink-0"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                ))}
                {documents.length === 0 && (
                  <div className="text-center py-8 sm:py-12">
                    <FileText className="mx-auto h-12 w-12 sm:h-16 sm:w-16 text-gray-300 mb-3 sm:mb-4" />
                    <p className="text-gray-500 font-medium text-sm sm:text-base">No documents uploaded yet</p>
                    <p className="text-xs sm:text-sm text-gray-400 mt-1">Upload your first document to get started</p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Chat Interface */}
          <div className="lg:col-span-2 order-1 lg:order-2">
            <div className="bg-white/80 backdrop-blur-lg rounded-2xl shadow-xl border border-white/20 h-[500px] sm:h-[600px] lg:h-[700px] flex flex-col hover:shadow-2xl transition-all duration-300">
              {/* Chat Header */}
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 sm:p-6 rounded-t-2xl">
                <div className="flex items-center space-x-2 sm:space-x-3">
                  <MessageCircle className="h-5 w-5 sm:h-6 sm:w-6" />
                  <div>
                    <h2 className="text-lg sm:text-xl font-bold">AI Assistant</h2>
                    <p className="text-blue-100 text-xs sm:text-sm">
                      Ask questions about your uploaded documents
                    </p>
                  </div>
                </div>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-3 sm:p-6 space-y-4 sm:space-y-6 bg-gradient-to-b from-gray-50/50 to-white/50">
                {messages.length === 0 && (
                  <div className="text-center py-8 sm:py-16">
                    <Brain className="mx-auto h-16 w-16 sm:h-20 sm:w-20 text-gray-300 mb-4 sm:mb-6" />
                    <h3 className="text-lg sm:text-xl font-bold text-gray-600 mb-2">Ready to help!</h3>
                    <p className="text-gray-500 text-sm sm:text-base">Start by asking a question about your documents</p>
                  </div>
                )}
                
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${
                      message.type === 'user' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    <div
                      className={`max-w-[85%] sm:max-w-md px-3 sm:px-6 py-3 sm:py-4 rounded-2xl shadow-lg transform hover:scale-[1.02] transition-all duration-200 ${
                        message.type === 'user'
                          ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white'
                          : 'bg-white border border-gray-200 text-gray-800'
                      }`}
                    >
                      <p className="text-sm leading-relaxed">{message.content}</p>
                      
                      {message.type === 'assistant' && message.sources && (
                        <div className="mt-3 sm:mt-4 pt-3 sm:pt-4 border-t border-gray-100">
                          <p className="text-xs font-bold mb-2 sm:mb-3 text-gray-600 uppercase tracking-wide">Sources</p>
                          <div className="space-y-2 sm:space-y-3">
                            {message.sources.slice(0, 3).map((source, index) => (
                              <div key={index} className="text-xs bg-gradient-to-r from-blue-50 to-indigo-50 p-2 sm:p-3 rounded-xl border border-blue-100">
                                <p className="font-bold text-blue-800 mb-1">{source.filename}</p>
                                <p className="text-gray-600 leading-relaxed">
                                  {source.content.substring(0, 80)}...
                                </p>
                              </div>
                            ))}
                          </div>
                          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mt-3 sm:mt-4 pt-2 sm:pt-3 border-t border-gray-100 space-y-2 sm:space-y-0">
                            {message.confidence_score && (
                              <div className="flex items-center space-x-2">
                                <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                                <span className="text-xs text-gray-500 font-medium">
                                  {(message.confidence_score * 100).toFixed(1)}% confidence
                                </span>
                              </div>
                            )}
                            {message.processing_time && (
                              <div className="flex items-center space-x-1 text-xs text-gray-500">
                                <Clock className="h-3 w-3" />
                                <span>{message.processing_time}s</span>
                              </div>
                            )}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
                
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-white border border-gray-200 max-w-[85%] sm:max-w-md px-3 sm:px-6 py-3 sm:py-4 rounded-2xl shadow-lg">
                      <div className="flex items-center space-x-3">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                          <div className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                        </div>
                        <span className="text-sm text-gray-600 font-medium">AI is thinking...</span>
                      </div>
                    </div>
                  </div>
                )}
                
                <div ref={messagesEndRef} />
              </div>

              {/* Input */}
              <div className="p-3 sm:p-6 bg-white/90 backdrop-blur-sm rounded-b-2xl border-t border-gray-100">
                <div className="flex space-x-2 sm:space-x-4">
                  <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleAskQuestion()}
                    placeholder="Ask a question about your documents..."
                    className="flex-1 border-2 border-gray-200 rounded-xl px-3 sm:px-4 py-2 sm:py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white/80 backdrop-blur-sm placeholder-gray-500 text-gray-800 shadow-sm text-sm sm:text-base"
                    disabled={isLoading}
                  />
                  <button
                    onClick={handleAskQuestion}
                    disabled={isLoading || !question.trim()}
                    className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-4 sm:px-6 py-2 sm:py-3 rounded-xl hover:from-blue-700 hover:to-blue-800 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg flex-shrink-0"
                  >
                    <Send className="h-4 w-4 sm:h-5 sm:w-5" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}