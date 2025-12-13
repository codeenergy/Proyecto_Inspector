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
      const response = await fetch('http://localhost:8001/explore/website', {
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
      setError('Error conectando con el servidor. Asegúrate que el backend esté corriendo en http://localhost:8001');
    } finally {
      setIsExploring(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl p-6 text-white">
        <div className="flex items-center space-x-3 mb-2">
          <Globe size={32} />
          <div>
            <h2 className="text-2xl font-bold">Explorador Web</h2>
            <p className="text-purple-100">Navega cualquier dominio como un usuario real</p>
          </div>
        </div>
      </div>

      {/* Form */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">
            URL del sitio a explorar
          </label>
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://ejemplo.com"
            className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-blue-500"
            disabled={isExploring}
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Profundidad máxima
            </label>
            <input
              type="number"
              value={maxDepth}
              onChange={(e) => setMaxDepth(parseInt(e.target.value))}
              min="1"
              max="5"
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-blue-500"
              disabled={isExploring}
            />
            <p className="text-xs text-slate-500 mt-1">Niveles de enlaces a seguir (1-5)</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Páginas máximas
            </label>
            <input
              type="number"
              value={maxPages}
              onChange={(e) => setMaxPages(parseInt(e.target.value))}
              min="5"
              max="100"
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-blue-500"
              disabled={isExploring}
            />
            <p className="text-xs text-slate-500 mt-1">Límite de páginas a visitar (5-100)</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Dispositivo
            </label>
            <select
              value={viewport}
              onChange={(e) => setViewport(e.target.value as any)}
              className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-blue-500"
              disabled={isExploring}
            >
              <option value="desktop">Desktop (1920x1080)</option>
              <option value="mobile">Mobile (375x667)</option>
              <option value="tablet">Tablet (768x1024)</option>
            </select>
            <p className="text-xs text-slate-500 mt-1">Resolución de pantalla</p>
          </div>
        </div>

        <button
          onClick={handleExplore}
          disabled={isExploring || !url}
          className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 disabled:cursor-not-allowed text-white py-3 rounded-lg flex items-center justify-center space-x-2 transition-colors font-medium"
        >
          {isExploring ? (
            <>
              <Loader2 className="animate-spin" size={20} />
              <span>Explorando sitio... Esto puede tomar varios minutos</span>
            </>
          ) : (
            <>
              <Play size={20} />
              <span>Iniciar Exploración</span>
            </>
          )}
        </button>

        {error && (
          <div className="bg-red-500/10 border border-red-500/50 rounded-lg p-4 flex items-start space-x-3">
            <AlertCircle className="text-red-400 shrink-0 mt-0.5" size={20} />
            <div className="text-red-200 text-sm">{error}</div>
          </div>
        )}
      </div>

      {/* Results */}
      {result && (
        <div className="space-y-4">
          {/* Stats Cards */}
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="flex items-center space-x-2 text-slate-400 text-sm mb-1">
                <Globe size={16} />
                <span>Páginas</span>
              </div>
              <div className="text-2xl font-bold text-white">{result.total_pages_visited}</div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="flex items-center space-x-2 text-slate-400 text-sm mb-1">
                <MousePointer size={16} />
                <span>Botones</span>
              </div>
              <div className="text-2xl font-bold text-blue-400">{result.total_buttons_clicked}</div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="flex items-center space-x-2 text-slate-400 text-sm mb-1">
                <LinkIcon size={16} />
                <span>Enlaces</span>
              </div>
              <div className="text-2xl font-bold text-emerald-400">{result.total_links_followed}</div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="flex items-center space-x-2 text-slate-400 text-sm mb-1">
                <AlertCircle size={16} />
                <span>Anuncios</span>
              </div>
              <div className="text-2xl font-bold text-orange-400">{result.total_ads_found}</div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-4">
              <div className="flex items-center space-x-2 text-slate-400 text-sm mb-1">
                <FileText size={16} />
                <span>Formularios</span>
              </div>
              <div className="text-2xl font-bold text-purple-400">{result.total_forms_found}</div>
            </div>
          </div>

          {/* Success Message */}
          <div className="bg-emerald-500/10 border border-emerald-500/50 rounded-lg p-4 flex items-start space-x-3">
            <CheckCircle className="text-emerald-400 shrink-0 mt-0.5" size={20} />
            <div>
              <div className="text-emerald-200 font-medium">Exploración completada con éxito</div>
              <div className="text-emerald-300/70 text-sm mt-1">
                Se exploraron {result.total_pages_visited} página(s) y se interactuó con {result.total_buttons_clicked} elemento(s)
              </div>
            </div>
          </div>

          {/* Sitemap */}
          {result.sitemap && result.sitemap.length > 0 && (
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center space-x-2">
                <Globe size={20} />
                <span>Páginas Exploradas</span>
              </h3>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {result.sitemap.map((page, index) => (
                  <div
                    key={index}
                    className="bg-slate-950 border border-slate-800 rounded-lg p-3 flex items-center space-x-3 hover:border-blue-500/50 transition-colors"
                  >
                    <div className="bg-blue-500/10 text-blue-400 rounded-full w-8 h-8 flex items-center justify-center text-sm font-medium shrink-0">
                      {index + 1}
                    </div>
                    <a
                      href={page}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-400 hover:text-blue-300 text-sm break-all"
                    >
                      {page}
                    </a>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Info Box */}
          <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
            <div className="flex items-start space-x-3">
              <Image className="text-blue-400 shrink-0 mt-0.5" size={20} />
              <div className="text-blue-200 text-sm">
                <p className="font-medium mb-1">Screenshots capturados</p>
                <p className="text-blue-300/70">
                  Los screenshots se guardaron en: <code className="bg-slate-950 px-2 py-1 rounded text-xs">backend/screenshots/</code>
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Info Box */}
      {!result && !isExploring && (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <h3 className="text-white font-medium mb-3">ℹ️ Cómo funciona</h3>
          <div className="space-y-2 text-sm text-slate-400">
            <p>• El bot navega el sitio como un <span className="text-white">usuario real</span></p>
            <p>• Hace <span className="text-white">scroll</span>, mueve el mouse, y espera tiempos naturales</p>
            <p>• Hace <span className="text-white">click en todos los botones</span> que encuentra</p>
            <p>• <span className="text-white">Detecta anuncios</span> (Google Ads, Facebook Ads, banners)</p>
            <p>• Sigue <span className="text-white">enlaces internos</span> del mismo dominio</p>
            <p>• Captura <span className="text-white">screenshots</span> de cada página visitada</p>
          </div>
        </div>
      )}
    </div>
  );
}
