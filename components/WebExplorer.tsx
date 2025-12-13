import React, { useState } from 'react';
import { Globe, Play, Loader2, CheckCircle, AlertCircle, MousePointer, Link as LinkIcon, FileText, Image } from 'lucide-react';

interface ExplorationResult {
  base_url: string;
  total_pages_visited: number;
  total_buttons_clicked: number;
  total_links_followed: number;
  total_ads_found: number;
  total_forms_found: number;
  sitemap: string[];
  screenshots: string[];
}

export function WebExplorer() {
  const [url, setUrl] = useState('');
  const [maxDepth, setMaxDepth] = useState(2);
  const [maxPages, setMaxPages] = useState(30);
  const [viewport, setViewport] = useState<'desktop' | 'mobile' | 'tablet'>('desktop');
  const [isExploring, setIsExploring] = useState(false);
  const [result, setResult] = useState<ExplorationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleExplore = async () => {
    if (!url) {
      setError('Por favor ingresa una URL');
      return;
    }

    setIsExploring(true);
    setError(null);
    setResult(null);

    try {
      const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001';
      const response = await fetch(`${API_BASE}/explore/website`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url,
          max_depth: maxDepth,
          max_pages: maxPages,
          viewport
        }),
      });

      const data = await response.json();

      if (data.status === 'success') {
        setResult(data.data);
      } else {
        setError(data.message || 'Error en la exploración');
      }
    } catch (err) {
      setError('Error conectando con el servidor. Verifica que el backend esté disponible.');
    } finally {
      setIsExploring(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-br from-purple-600 via-blue-600 to-purple-600 rounded-2xl p-6 md:p-8 text-white shadow-xl shadow-purple-500/20 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent pointer-events-none"></div>
        <div className="relative flex flex-col md:flex-row md:items-center gap-4">
          <div className="bg-white/20 backdrop-blur-sm p-3 rounded-xl w-fit">
            <Globe size={32} />
          </div>
          <div>
            <h2 className="text-2xl md:text-3xl font-bold mb-1">Web Explorer</h2>
            <p className="text-purple-100">Navigate any domain like a real user</p>
          </div>
        </div>
      </div>

      {/* Form */}
      <div className="bg-gradient-to-br from-slate-900/80 to-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-6 md:p-8 space-y-5 shadow-xl">
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">
            Website URL to explore
          </label>
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            className="w-full bg-slate-950/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all"
            disabled={isExploring}
          />
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Max Depth
            </label>
            <input
              type="number"
              value={maxDepth}
              onChange={(e) => setMaxDepth(parseInt(e.target.value))}
              min="1"
              max="5"
              className="w-full bg-slate-950/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all"
              disabled={isExploring}
            />
            <p className="text-xs text-slate-500 mt-1.5">Link levels to follow (1-5)</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Max Pages
            </label>
            <input
              type="number"
              value={maxPages}
              onChange={(e) => setMaxPages(parseInt(e.target.value))}
              min="5"
              max="100"
              className="w-full bg-slate-950/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all"
              disabled={isExploring}
            />
            <p className="text-xs text-slate-500 mt-1.5">Page visit limit (5-100)</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Device
            </label>
            <select
              value={viewport}
              onChange={(e) => setViewport(e.target.value as any)}
              className="w-full bg-slate-950/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all"
              disabled={isExploring}
            >
              <option value="desktop">Desktop (1920x1080)</option>
              <option value="mobile">Mobile (375x667)</option>
              <option value="tablet">Tablet (768x1024)</option>
            </select>
            <p className="text-xs text-slate-500 mt-1.5">Screen resolution</p>
          </div>
        </div>

        <button
          onClick={handleExplore}
          disabled={isExploring || !url}
          className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 disabled:from-slate-700 disabled:to-slate-700 disabled:cursor-not-allowed text-white py-3.5 rounded-xl flex items-center justify-center space-x-2 transition-all font-medium shadow-lg shadow-purple-500/30 hover:shadow-purple-500/50"
        >
          {isExploring ? (
            <>
              <Loader2 className="animate-spin" size={20} />
              <span className="hidden sm:inline">Exploring site... This may take several minutes</span>
              <span className="sm:hidden">Exploring...</span>
            </>
          ) : (
            <>
              <Play size={20} />
              <span>Start Exploration</span>
            </>
          )}
        </button>

        {error && (
          <div className="bg-red-500/10 border border-red-500/50 rounded-xl p-4 flex items-start space-x-3 animate-shake">
            <AlertCircle className="text-red-400 shrink-0 mt-0.5" size={20} />
            <div className="text-red-200 text-sm">{error}</div>
          </div>
        )}
      </div>

      {/* Results */}
      {result && (
        <div className="space-y-6">
          {/* Stats Cards */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3 md:gap-4">
            <div className="bg-gradient-to-br from-slate-900/80 to-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-4 hover:border-purple-500/50 transition-all">
              <div className="flex items-center space-x-2 text-slate-400 text-xs md:text-sm mb-2">
                <Globe size={16} />
                <span>Pages</span>
              </div>
              <div className="text-2xl md:text-3xl font-bold text-white tabular-nums">{result.total_pages_visited}</div>
            </div>

            <div className="bg-gradient-to-br from-slate-900/80 to-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-4 hover:border-blue-500/50 transition-all">
              <div className="flex items-center space-x-2 text-slate-400 text-xs md:text-sm mb-2">
                <MousePointer size={16} />
                <span>Buttons</span>
              </div>
              <div className="text-2xl md:text-3xl font-bold text-blue-400 tabular-nums">{result.total_buttons_clicked}</div>
            </div>

            <div className="bg-gradient-to-br from-slate-900/80 to-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-4 hover:border-emerald-500/50 transition-all">
              <div className="flex items-center space-x-2 text-slate-400 text-xs md:text-sm mb-2">
                <LinkIcon size={16} />
                <span>Links</span>
              </div>
              <div className="text-2xl md:text-3xl font-bold text-emerald-400 tabular-nums">{result.total_links_followed}</div>
            </div>

            <div className="bg-gradient-to-br from-slate-900/80 to-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-4 hover:border-orange-500/50 transition-all">
              <div className="flex items-center space-x-2 text-slate-400 text-xs md:text-sm mb-2">
                <AlertCircle size={16} />
                <span>Ads</span>
              </div>
              <div className="text-2xl md:text-3xl font-bold text-orange-400 tabular-nums">{result.total_ads_found}</div>
            </div>

            <div className="bg-gradient-to-br from-slate-900/80 to-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-4 hover:border-purple-500/50 transition-all col-span-2 sm:col-span-1">
              <div className="flex items-center space-x-2 text-slate-400 text-xs md:text-sm mb-2">
                <FileText size={16} />
                <span>Forms</span>
              </div>
              <div className="text-2xl md:text-3xl font-bold text-purple-400 tabular-nums">{result.total_forms_found}</div>
            </div>
          </div>

          {/* Success Message */}
          <div className="bg-emerald-500/10 border border-emerald-500/50 rounded-xl p-4 md:p-5 flex items-start space-x-3">
            <CheckCircle className="text-emerald-400 shrink-0 mt-0.5" size={20} />
            <div>
              <div className="text-emerald-200 font-medium mb-1">Exploration completed successfully</div>
              <div className="text-emerald-300/70 text-sm">
                Explored {result.total_pages_visited} page(s) and interacted with {result.total_buttons_clicked} element(s)
              </div>
            </div>
          </div>

          {/* Sitemap */}
          {result.sitemap && result.sitemap.length > 0 && (
            <div className="bg-gradient-to-br from-slate-900/80 to-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-6 md:p-8">
              <h3 className="text-lg md:text-xl font-bold text-white mb-4 md:mb-6 flex items-center space-x-2">
                <Globe size={20} className="text-purple-400" />
                <span>Explored Pages</span>
              </h3>
              <div className="space-y-2 max-h-96 overflow-y-auto pr-2 scrollbar-thin">
                {result.sitemap.map((page, index) => (
                  <div
                    key={index}
                    className="bg-slate-950/50 border border-slate-700/50 rounded-xl p-3 md:p-4 flex items-center space-x-3 hover:border-purple-500/50 hover:bg-slate-800/30 transition-all group"
                  >
                    <div className="bg-gradient-to-br from-purple-600/20 to-blue-600/20 text-purple-400 rounded-full w-8 h-8 flex items-center justify-center text-sm font-medium shrink-0 group-hover:from-purple-600/30 group-hover:to-blue-600/30 transition-all">
                      {index + 1}
                    </div>
                    <a
                      href={page}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-400 hover:text-blue-300 text-xs md:text-sm break-all transition-colors"
                    >
                      {page}
                    </a>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Info Box */}
          <div className="bg-blue-500/10 border border-blue-500/30 rounded-xl p-4 md:p-5">
            <div className="flex items-start space-x-3">
              <div className="bg-blue-500/20 p-2 rounded-lg">
                <Image className="text-blue-400 shrink-0" size={20} />
              </div>
              <div className="text-blue-200 text-sm">
                <p className="font-medium mb-1">Screenshots captured</p>
                <p className="text-blue-300/70">
                  Screenshots were saved to: <code className="bg-slate-950/50 px-2 py-1 rounded text-xs">backend/screenshots/</code>
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Info Box */}
      {!result && !isExploring && (
        <div className="bg-gradient-to-br from-slate-900/80 to-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-6 md:p-8">
          <h3 className="text-white font-semibold mb-4 flex items-center gap-2">
            <div className="bg-blue-500/20 p-2 rounded-lg">
              <Globe size={20} className="text-blue-400" />
            </div>
            How It Works
          </h3>
          <div className="space-y-3 text-sm text-slate-400">
            <p className="flex items-start gap-2">
              <span className="text-blue-400 shrink-0">•</span>
              The bot navigates the site like a <span className="text-white font-medium">real user</span>
            </p>
            <p className="flex items-start gap-2">
              <span className="text-purple-400 shrink-0">•</span>
              Performs <span className="text-white font-medium">scrolling</span>, moves the mouse, and waits for natural timings
            </p>
            <p className="flex items-start gap-2">
              <span className="text-emerald-400 shrink-0">•</span>
              <span className="text-white font-medium">Clicks all buttons</span> it finds
            </p>
            <p className="flex items-start gap-2">
              <span className="text-orange-400 shrink-0">•</span>
              <span className="text-white font-medium">Detects ads</span> (Google Ads, Facebook Ads, banners)
            </p>
            <p className="flex items-start gap-2">
              <span className="text-yellow-400 shrink-0">•</span>
              Follows <span className="text-white font-medium">internal links</span> from the same domain
            </p>
            <p className="flex items-start gap-2">
              <span className="text-pink-400 shrink-0">•</span>
              Captures <span className="text-white font-medium">screenshots</span> of each page visited
            </p>
          </div>
        </div>
      )}

      <style>{`
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-5px); }
          75% { transform: translateX(5px); }
        }
        .animate-shake {
          animation: shake 0.3s ease-in-out;
        }
        .scrollbar-thin::-webkit-scrollbar {
          width: 6px;
        }
        .scrollbar-thin::-webkit-scrollbar-track {
          background: rgba(51, 65, 85, 0.3);
          border-radius: 3px;
        }
        .scrollbar-thin::-webkit-scrollbar-thumb {
          background: rgba(139, 92, 246, 0.5);
          border-radius: 3px;
        }
        .scrollbar-thin::-webkit-scrollbar-thumb:hover {
          background: rgba(139, 92, 246, 0.7);
        }
      `}</style>
    </div>
  );
}
