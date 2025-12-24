import React, { useState, useEffect } from 'react';
import {
  LayoutDashboard,
  Play,
  Pause,
  Plus,
  Target,
  MousePointer2,
  Eye,
  Trash2,
  Edit,
  Terminal,
  Clock,
  LogOut,
  Menu,
  X,
  Hand,
  ExternalLink
} from 'lucide-react';
import { BotTarget, BotStats } from './types';
import { CampaignModal } from './components/CampaignModal';
import { useAuth } from './AuthContext';
import { Login } from './components/Login';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001';

interface LogEntry {
  id: number;
  target_id: number;
  status: string;
  pages: number;
  ads: number;
  buttons?: number;    // NUEVO: Botones clickeados
  windows?: number;    // NUEVO: Ventanas abiertas
  duration: number;
  time: string;
}

function App() {
  const { isAuthenticated, logout } = useAuth();

  // All hooks must be declared at the top before any conditional returns
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [targets, setTargets] = useState<BotTarget[]>([]);
  const [stats, setStats] = useState<BotStats>({ total_sessions: 0, total_pageviews: 0, total_ad_clicks: 0 });
  const [schedulerStatus, setSchedulerStatus] = useState({ running: false, active_sessions: 0 });
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTarget, setEditingTarget] = useState<BotTarget | null>(null);
  const [liveLogs, setLiveLogs] = useState<LogEntry[]>([]);

  // Show login screen if not authenticated (after all hooks are declared)
  if (!isAuthenticated) {
    return <Login />;
  }

  // Poll data
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [targetsRes, statusRes, logsRes] = await Promise.all([
          fetch(`${API_BASE}/targets`),
          fetch(`${API_BASE}/scheduler/status`),
          fetch(`${API_BASE}/sessions/live`)
        ]);

        const targetsData = await targetsRes.json();
        const statusData = await statusRes.json();
        const logsData = await logsRes.json();

        if (targetsData.status === 'success') setTargets(targetsData.data);
        if (statusData.status === 'success') {
          setSchedulerStatus({
            running: statusData.data.running,
            active_sessions: statusData.data.active_sessions
          });
          setStats(statusData.data.stats);
        }
        if (logsData.status === 'success') {
          setLiveLogs(logsData.data);
        }

      } catch (e) {
        console.error("Error fetching data", e);
      }
    };

    fetchData(); // Initial
    const interval = setInterval(fetchData, 3000); // 3s poll specifically for logs
    return () => clearInterval(interval);
  }, []);

  const handleToggleScheduler = async () => {
    const endpoint = schedulerStatus.running ? 'stop' : 'start';
    try {
      await fetch(`${API_BASE}/scheduler/${endpoint}`, { method: 'POST' });
      // Optimistic update
      setSchedulerStatus(prev => ({ ...prev, running: !prev.running }));
    } catch (e) {
      console.error("Error toggling scheduler", e);
    }
  };

  const handleAddTarget = async (newTarget: any) => {
    // Refresh handled by polling
  };

  const handleDeleteTarget = async (id: number) => {
    if (!confirm("Are you sure you want to delete this target?")) return;
    try {
      const res = await fetch(`${API_BASE}/targets/${id}`, { method: 'DELETE' });
      if (!res.ok) throw new Error("Server returned error");
      // Poll will update, but we can optimistically remove
      setTargets(prev => prev.filter(t => t.id !== id));
    } catch (e) {
      console.error("Error deleting", e);
      alert("Error deleting target. Check backend logs.");
    }
  };

  const handleEditTarget = (target: BotTarget) => {
    setEditingTarget(target);
    setIsModalOpen(true);
  };

  const totalTargets = targets.length;

  return (
    <div className="flex h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-slate-200 font-sans selection:bg-blue-500/30 overflow-hidden">

      {/* Mobile Menu Overlay */}
      {isMobileMenuOpen && (
        <div
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`fixed lg:static inset-y-0 left-0 w-72 bg-slate-900/80 backdrop-blur-xl border-r border-slate-700/50 flex flex-col z-50 transition-transform duration-300 ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}`}>
        {/* Header */}
        <div className="p-6 flex items-center justify-between border-b border-slate-700/50 bg-gradient-to-br from-blue-600/10 to-purple-600/10">
          <div className="flex items-center space-x-3">
            <div className="bg-gradient-to-br from-blue-600 to-purple-600 p-2.5 rounded-xl shadow-lg shadow-blue-500/30">
              <Target size={24} className="text-white" />
            </div>
            <div>
              <h1 className="font-bold text-white tracking-tight text-lg">TrafficBot Pro</h1>
              <p className="text-xs text-emerald-400 font-medium tracking-wide flex items-center gap-1">
                <span className="h-1.5 w-1.5 bg-emerald-400 rounded-full animate-pulse"></span>
                SYSTEM ONLINE
              </p>
            </div>
          </div>
          <button
            onClick={() => setIsMobileMenuOpen(false)}
            className="lg:hidden text-slate-400 hover:text-white transition-colors"
          >
            <X size={24} />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
          <div className="w-full flex items-center space-x-3 px-4 py-3.5 rounded-xl bg-gradient-to-r from-blue-600/20 to-purple-600/20 text-blue-400 border border-blue-500/30 shadow-lg shadow-blue-500/20">
            <LayoutDashboard size={20} />
            <span className="font-medium">Bot Control</span>
          </div>

          <div className="mt-6 px-4 py-3 bg-slate-950/50 rounded-xl border border-slate-700/50">
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Monetag Stats</div>
            <div className="space-y-1 text-sm">
              <div className="flex justify-between text-slate-400">
                <span>Popunders:</span>
                <span className="text-emerald-400 font-medium">{stats.total_ad_clicks}</span>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Pageviews:</span>
                <span className="text-blue-400 font-medium">{stats.total_pageviews}</span>
              </div>
            </div>
          </div>
        </nav>

        {/* Bot Engine Status */}
        <div className="p-4 border-t border-slate-700/50 space-y-3">
          <div className="bg-slate-950/50 backdrop-blur-sm rounded-xl p-4 border border-slate-700/50">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-slate-300">Bot Engine</span>
              <div className={`h-2.5 w-2.5 rounded-full ${schedulerStatus.running ? 'bg-emerald-500 animate-pulse shadow-lg shadow-emerald-500/50' : 'bg-red-500 shadow-lg shadow-red-500/50'}`}></div>
            </div>
            <p className="text-xs text-slate-400 mb-3">{schedulerStatus.active_sessions} Active Sessions</p>
            <button
              onClick={handleToggleScheduler}
              className={`w-full py-2.5 rounded-lg text-sm font-medium flex items-center justify-center space-x-2 transition-all duration-200 ${schedulerStatus.running ? 'bg-red-500/20 text-red-400 hover:bg-red-500/30 border border-red-500/30' : 'bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500/30 border border-emerald-500/30'}`}
            >
              {schedulerStatus.running ? <><Pause size={16} /> <span>Stop Bot</span></> : <><Play size={16} /> <span>Start Bot</span></>}
            </button>
          </div>

          {/* Logout Button */}
          <button
            onClick={logout}
            className="w-full bg-slate-950/50 backdrop-blur-sm hover:bg-red-500/10 border border-slate-700/50 hover:border-red-500/50 text-slate-400 hover:text-red-400 py-2.5 rounded-lg text-sm font-medium flex items-center justify-center space-x-2 transition-all duration-200"
          >
            <LogOut size={16} />
            <span>Logout</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-full overflow-hidden relative">
        {/* Header */}
        <header className="h-16 bg-slate-900/50 backdrop-blur-xl border-b border-slate-700/50 flex items-center justify-between px-4 md:px-8 sticky top-0 z-10">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setIsMobileMenuOpen(true)}
              className="lg:hidden text-slate-400 hover:text-white transition-colors"
            >
              <Menu size={24} />
            </button>
            <h2 className="text-lg md:text-xl font-semibold text-white">
              Bot Control Center - Monetag Traffic
            </h2>
          </div>
          <div className="flex items-center gap-3">
            <div className="hidden md:flex items-center gap-2 text-sm text-slate-400">
              <div className="h-2 w-2 bg-emerald-400 rounded-full animate-pulse"></div>
              <span>Authenticated</span>
            </div>
            {/* Mobile Logout Button */}
            <button
              onClick={logout}
              className="lg:hidden bg-red-500/10 hover:bg-red-500/20 border border-red-500/30 text-red-400 px-3 py-2 rounded-lg text-sm font-medium flex items-center gap-2 transition-all"
            >
              <LogOut size={16} />
              <span className="hidden sm:inline">Logout</span>
            </button>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8 space-y-6 md:space-y-8">
          {/* Stats Grid - MODO USUARIO NORMAL */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
                {/* Card 1: Botones Clickeados */}
                <div className="group bg-gradient-to-br from-slate-900/80 to-slate-800/50 backdrop-blur-sm border border-slate-700/50 hover:border-blue-500/50 p-6 rounded-2xl transition-all duration-300 hover:shadow-xl hover:shadow-blue-500/10 hover:-translate-y-1">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="text-slate-400 text-sm font-medium mb-1">Botones Clickeados</p>
                      <h3 className="text-3xl md:text-4xl font-bold text-blue-400 mt-2 tabular-nums">{stats.total_buttons_clicked || 0}</h3>
                      <p className="text-xs text-slate-500 mt-1">Clicks totales en botones</p>
                    </div>
                    <div className="bg-blue-500/10 p-3 rounded-xl group-hover:bg-blue-500/20 transition-colors">
                      <Hand className="text-blue-400" size={28} />
                    </div>
                  </div>
                </div>

                {/* Card 2: Páginas Visitadas */}
                <div className="group bg-gradient-to-br from-slate-900/80 to-slate-800/50 backdrop-blur-sm border border-slate-700/50 hover:border-emerald-500/50 p-6 rounded-2xl transition-all duration-300 hover:shadow-xl hover:shadow-emerald-500/10 hover:-translate-y-1">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="text-slate-400 text-sm font-medium mb-1">Páginas Visitadas</p>
                      <h3 className="text-3xl md:text-4xl font-bold text-emerald-400 mt-2 tabular-nums">{stats.total_pageviews}</h3>
                      <p className="text-xs text-slate-500 mt-1">Navegación interna</p>
                    </div>
                    <div className="bg-emerald-500/10 p-3 rounded-xl group-hover:bg-emerald-500/20 transition-colors">
                      <Eye className="text-emerald-400" size={28} />
                    </div>
                  </div>
                </div>

                {/* Card 3: Direct Links Abiertos (Monetag) */}
                <div className="group bg-gradient-to-br from-slate-900/80 to-slate-800/50 backdrop-blur-sm border border-slate-700/50 hover:border-orange-500/50 p-6 rounded-2xl transition-all duration-300 hover:shadow-xl hover:shadow-orange-500/10 hover:-translate-y-1">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="text-slate-400 text-sm font-medium mb-1">Direct Links Abiertos</p>
                      <h3 className="text-3xl md:text-4xl font-bold text-orange-400 mt-2 tabular-nums">{stats.total_windows_opened || 0}</h3>
                      <p className="text-xs text-slate-500 mt-1">Ventanas de Monetag</p>
                    </div>
                    <div className="bg-orange-500/10 p-3 rounded-xl group-hover:bg-orange-500/20 transition-colors">
                      <ExternalLink className="text-orange-400" size={28} />
                    </div>
                  </div>
                </div>

                {/* Card 4: Targets Activos */}
                <div className="group bg-gradient-to-br from-slate-900/80 to-slate-800/50 backdrop-blur-sm border border-slate-700/50 hover:border-purple-500/50 p-6 rounded-2xl transition-all duration-300 hover:shadow-xl hover:shadow-purple-500/10 hover:-translate-y-1">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="text-slate-400 text-sm font-medium mb-1">Targets Activos</p>
                      <h3 className="text-3xl md:text-4xl font-bold text-purple-400 mt-2 tabular-nums">{targets.length}</h3>
                      <p className="text-xs text-slate-500 mt-1">Sitios configurados</p>
                    </div>
                    <div className="bg-purple-500/10 p-3 rounded-xl group-hover:bg-purple-500/20 transition-colors">
                      <Target className="text-purple-400" size={28} />
                    </div>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 xl:grid-cols-3 gap-4 md:gap-6">
                {/* Targets List */}
                <div className="xl:col-span-2 space-y-4 md:space-y-6">
                  <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3">
                    <h3 className="text-lg md:text-xl font-bold text-white">Traffic Targets</h3>
                    <button
                      onClick={() => { setEditingTarget(null); setIsModalOpen(true); }}
                      className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white px-4 py-2.5 rounded-xl flex items-center justify-center space-x-2 transition-all duration-200 shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50"
                    >
                      <Plus size={18} />
                      <span className="font-medium">Add Target</span>
                    </button>
                  </div>

                  <div className="bg-gradient-to-br from-slate-900/80 to-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl overflow-hidden">
                    {/* Desktop Table View */}
                    <div className="hidden md:block overflow-x-auto">
                      <table className="w-full text-left">
                        <thead className="bg-slate-950/50 text-slate-400 text-xs uppercase font-semibold">
                          <tr>
                            <th className="px-6 py-4">URL</th>
                            <th className="px-6 py-4">Config</th>
                            <th className="px-6 py-4">Status</th>
                            <th className="px-6 py-4 text-right">Actions</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-700/50">
                          {targets.map((target) => (
                            <tr key={target.id} className="hover:bg-slate-800/50 transition-colors">
                              <td className="px-6 py-4">
                                <div className="font-medium text-white break-all max-w-md">{target.url}</div>
                              </td>
                              <td className="px-6 py-4 text-sm text-slate-400">
                                <div className="flex flex-col gap-1">
                                  <span className="flex items-center gap-1"><Eye size={12} /> {target.target_pageviews} views</span>
                                  <span className="flex items-center gap-1"><MousePointer2 size={12} /> {(target.ad_click_probability * 100).toFixed(0)}% ad click</span>
                                </div>
                              </td>
                              <td className="px-6 py-4">
                                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                                  ACTIVE
                                </span>
                              </td>
                              <td className="px-6 py-4 text-right">
                                <div className="flex justify-end gap-2">
                                  <button onClick={() => handleEditTarget(target)} className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-700/50 transition-all"><Edit size={16} /></button>
                                  <button onClick={() => handleDeleteTarget(target.id)} className="p-2 rounded-lg text-red-400 hover:text-red-300 hover:bg-red-500/10 transition-all"><Trash2 size={16} /></button>
                                </div>
                              </td>
                            </tr>
                          ))}
                          {targets.length === 0 && (
                            <tr>
                              <td colSpan={4} className="px-6 py-12 text-center text-slate-500">
                                No active targets. Add one to start generating traffic.
                              </td>
                            </tr>
                          )}
                        </tbody>
                      </table>
                    </div>

                    {/* Mobile Card View */}
                    <div className="md:hidden divide-y divide-slate-700/50">
                      {targets.map((target) => (
                        <div key={target.id} className="p-4 hover:bg-slate-800/30 transition-colors">
                          <div className="flex justify-between items-start mb-3">
                            <div className="flex-1 min-w-0 pr-2">
                              <div className="font-medium text-white break-all text-sm mb-2">{target.url}</div>
                              <div className="flex flex-wrap gap-2 text-xs text-slate-400">
                                <span className="flex items-center gap-1 bg-slate-800/50 px-2 py-1 rounded">
                                  <Eye size={12} /> {target.target_pageviews} views
                                </span>
                                <span className="flex items-center gap-1 bg-slate-800/50 px-2 py-1 rounded">
                                  <MousePointer2 size={12} /> {(target.ad_click_probability * 100).toFixed(0)}%
                                </span>
                              </div>
                            </div>
                            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 whitespace-nowrap">
                              ACTIVE
                            </span>
                          </div>
                          <div className="flex gap-2">
                            <button
                              onClick={() => handleEditTarget(target)}
                              className="flex-1 bg-slate-800/50 hover:bg-slate-700/50 text-slate-300 px-3 py-2 rounded-lg flex items-center justify-center gap-2 text-sm transition-colors"
                            >
                              <Edit size={14} /> Edit
                            </button>
                            <button
                              onClick={() => handleDeleteTarget(target.id)}
                              className="flex-1 bg-red-500/10 hover:bg-red-500/20 text-red-400 px-3 py-2 rounded-lg flex items-center justify-center gap-2 text-sm transition-colors"
                            >
                              <Trash2 size={14} /> Delete
                            </button>
                          </div>
                        </div>
                      ))}
                      {targets.length === 0 && (
                        <div className="px-6 py-12 text-center text-slate-500">
                          No active targets. Add one to start generating traffic.
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Live Logs */}
                <div className="xl:col-span-1 space-y-4 md:space-y-6">
                  <h3 className="text-lg md:text-xl font-bold text-white flex items-center gap-2">
                    <Terminal size={20} className="text-blue-400" /> Live Bot Activity
                  </h3>
                  <div className="bg-gradient-to-br from-slate-950/80 to-slate-900/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-4 h-[400px] md:h-[500px] overflow-y-auto font-mono text-xs">
                    <div className="space-y-3">
                      {liveLogs.map((log) => (
                        <div key={log.id} className="border-b border-slate-700/50 pb-3 last:border-0 hover:bg-slate-800/30 p-2 rounded-lg transition-colors">
                          <div className="flex justify-between text-slate-500 mb-1.5">
                            <span className="flex items-center gap-1"><Clock size={10} /> {log.time}</span>
                            <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${log.status === 'completed' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-blue-500/20 text-blue-400 border border-blue-500/30'}`}>
                              {log.status.toUpperCase()}
                            </span>
                          </div>
                          <div className="text-slate-300 font-medium mb-1.5">Target #{log.target_id}</div>
                          <div className="text-slate-400 flex flex-wrap gap-2">
                            <span className="bg-slate-800/50 px-2 py-0.5 rounded">📄 Páginas: {log.pages}</span>
                            <span className="bg-blue-500/10 text-blue-400 px-2 py-0.5 rounded border border-blue-500/30">🖐️ Botones: {log.buttons || 0}</span>
                            <span className="bg-orange-500/10 text-orange-400 px-2 py-0.5 rounded border border-orange-500/30">🔗 Links: {log.windows || 0}</span>
                            <span className="bg-slate-800/50 px-2 py-0.5 rounded">⏱️ {log.duration.toFixed(1)}s</span>
                          </div>
                        </div>
                      ))}
                      {liveLogs.length === 0 && (
                        <div className="text-slate-600 text-center mt-10 flex flex-col items-center gap-3">
                          <Terminal size={32} className="opacity-20" />
                          <p>Waiting for sessions...</p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
        </div>
      </main>

      <CampaignModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSave={handleAddTarget}
        initialData={editingTarget}
      />
    </div>
  );
}

export default App;