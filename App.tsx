import React, { useState, useEffect } from 'react';
import {
  LayoutDashboard,
  Play,
  Pause,
  Plus,
  Monitor,
  Target,
  MousePointer2,
  Eye,
  Activity,
  Globe,
  Trash2,
  Edit,
  Terminal,
  Clock
} from 'lucide-react';
import { BotTarget, BotStats } from './types';
import { CampaignModal } from './components/CampaignModal';
import { WebExplorer } from './components/WebExplorer';

const API_BASE = 'http://localhost:8001';

interface LogEntry {
  id: number;
  target_id: number;
  status: string;
  pages: number;
  ads: number;
  duration: number;
  time: string;
}

function App() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'targets' | 'explorer'>('dashboard');
  const [targets, setTargets] = useState<BotTarget[]>([]);
  const [stats, setStats] = useState<BotStats>({ total_sessions: 0, total_pageviews: 0, total_ad_clicks: 0 });
  const [schedulerStatus, setSchedulerStatus] = useState({ running: false, active_sessions: 0 });
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTarget, setEditingTarget] = useState<BotTarget | null>(null);
  const [liveLogs, setLiveLogs] = useState<LogEntry[]>([]);

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
    <div className="flex h-screen bg-slate-950 text-slate-200 font-sans selection:bg-blue-500/30">

      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col z-20">
        <div className="p-6 flex items-center space-x-3 border-b border-slate-800">
          <div className="bg-blue-600 p-2 rounded-lg">
            <Target size={24} className="text-white" />
          </div>
          <div>
            <h1 className="font-bold text-white tracking-tight">TrafficBot Pro</h1>
            <p className="text-xs text-emerald-400 font-medium tracking-wide">SYSTEM ONLINE</p>
          </div>
        </div>

        <nav className="flex-1 px-4 py-6 space-y-2">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all ${activeTab === 'dashboard' ? 'bg-blue-600/10 text-blue-400 border border-blue-600/20' : 'hover:bg-slate-800 text-slate-400'}`}
          >
            <LayoutDashboard size={20} />
            <span className="font-medium">Bot Control</span>
          </button>

          <button
            onClick={() => setActiveTab('explorer')}
            className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all ${activeTab === 'explorer' ? 'bg-blue-600/10 text-blue-400 border border-blue-600/20' : 'hover:bg-slate-800 text-slate-400'}`}
          >
            <Globe size={20} />
            <span className="font-medium">Web Explorer</span>
          </button>
        </nav>

        <div className="p-4 border-t border-slate-800">
          <div className="bg-slate-950 rounded-xl p-4 border border-slate-800">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-slate-400">Bot Engine</span>
              <div className={`h-2.5 w-2.5 rounded-full ${schedulerStatus.running ? 'bg-emerald-500 animate-pulse' : 'bg-red-500'}`}></div>
            </div>
            <p className="text-xs text-slate-500 mb-3">{schedulerStatus.active_sessions} Active Sessions</p>
            <button
              onClick={handleToggleScheduler}
              className={`w-full py-2 rounded-lg text-sm font-medium flex items-center justify-center space-x-2 transition-colors ${schedulerStatus.running ? 'bg-red-500/10 text-red-400 hover:bg-red-500/20' : 'bg-emerald-500/10 text-emerald-400 hover:bg-emerald-500/20'}`}
            >
              {schedulerStatus.running ? <><Pause size={16} /> <span>Stop Bot</span></> : <><Play size={16} /> <span>Start Bot</span></>}
            </button>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-full overflow-hidden relative">
        <header className="h-16 bg-slate-900/50 backdrop-blur-md border-b border-slate-800 flex items-center justify-between px-8 sticky top-0 z-10">
          <h2 className="text-xl font-semibold text-white">
            {activeTab === 'dashboard' && 'Bot Control Center'}
            {activeTab === 'explorer' && 'Manual Web Explorer'}
          </h2>
        </header>

        <div className="flex-1 overflow-y-auto p-8 space-y-8">

          {activeTab === 'dashboard' && (
            <>
              {/* Stats Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="text-slate-400 text-sm font-medium">Total Sessions</p>
                      <h3 className="text-3xl font-bold text-white mt-2">{stats.total_sessions}</h3>
                    </div>
                    <Activity className="text-blue-500 opacity-20" size={32} />
                  </div>
                </div>
                <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="text-slate-400 text-sm font-medium">Pages Visited</p>
                      <h3 className="text-3xl font-bold text-emerald-400 mt-2">{stats.total_pageviews}</h3>
                    </div>
                    <Eye className="text-emerald-500 opacity-20" size={32} />
                  </div>
                </div>
                <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="text-slate-400 text-sm font-medium">Ads Clicked</p>
                      <h3 className="text-3xl font-bold text-yellow-400 mt-2">{stats.total_ad_clicks}</h3>
                    </div>
                    <MousePointer2 className="text-yellow-500 opacity-20" size={32} />
                  </div>
                </div>
                <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl">
                  <div className="flex justify-between items-start">
                    <div>
                      <p className="text-slate-400 text-sm font-medium">Active Targets</p>
                      <h3 className="text-3xl font-bold text-purple-400 mt-2">{targets.length}</h3>
                    </div>
                    <Target className="text-purple-500 opacity-20" size={32} />
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
                {/* Targets List */}
                <div className="xl:col-span-2 space-y-6">
                  <div className="flex justify-between items-center">
                    <h3 className="text-lg font-bold text-white">Traffic Targets</h3>
                    <button
                      onClick={() => { setEditingTarget(null); setIsModalOpen(true); }}
                      className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg flex items-center space-x-2 transition-colors"
                    >
                      <Plus size={18} />
                      <span>Add Target</span>
                    </button>
                  </div>

                  <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden">
                    <table className="w-full text-left">
                      <thead className="bg-slate-950 text-slate-400 text-xs uppercase font-semibold">
                        <tr>
                          <th className="px-6 py-4">URL</th>
                          <th className="px-6 py-4">Config</th>
                          <th className="px-6 py-4">Status</th>
                          <th className="px-6 py-4 text-right">Actions</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800">
                        {targets.map((target) => (
                          <tr key={target.id} className="hover:bg-slate-800/50 transition-colors">
                            <td className="px-6 py-4">
                              <div className="font-medium text-white break-all">{target.url}</div>
                            </td>
                            <td className="px-6 py-4 text-sm text-slate-400">
                              <div className="flex flex-col gap-1">
                                <span className="flex items-center gap-1"><Eye size={12} /> {target.target_pageviews} views</span>
                                <span className="flex items-center gap-1"><MousePointer2 size={12} /> {(target.ad_click_probability * 100).toFixed(0)}% ad click</span>
                              </div>
                            </td>
                            <td className="px-6 py-4">
                              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400">
                                ACTIVE
                              </span>
                            </td>
                            <td className="px-6 py-4 text-right">
                              <div className="flex justify-end gap-2">
                                <button onClick={() => handleEditTarget(target)} className="text-slate-400 hover:text-white transition-colors"><Edit size={16} /></button>
                                <button onClick={() => handleDeleteTarget(target.id)} className="text-red-400 hover:text-red-300 transition-colors"><Trash2 size={16} /></button>
                              </div>
                            </td>
                          </tr>
                        ))}
                        {targets.length === 0 && (
                          <tr>
                            <td colSpan={4} className="px-6 py-8 text-center text-slate-500">
                              No active targets. Add one to start generating traffic.
                            </td>
                          </tr>
                        )}
                      </tbody>
                    </table>
                  </div>
                </div>

                {/* Live Logs */}
                <div className="xl:col-span-1 space-y-6">
                  <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    <Terminal size={20} /> Live Bot Activity
                  </h3>
                  <div className="bg-slate-950 border border-slate-800 rounded-2xl p-4 h-[500px] overflow-y-auto font-mono text-xs">
                    <div className="space-y-3">
                      {liveLogs.map((log) => (
                        <div key={log.id} className="border-b border-slate-800 pb-2 last:border-0">
                          <div className="flex justify-between text-slate-500 mb-1">
                            <span className="flex items-center gap-1"><Clock size={10} /> {log.time}</span>
                            <span className={`${log.status === 'completed' ? 'text-emerald-400' : 'text-blue-400'}`}>{log.status.toUpperCase()}</span>
                          </div>
                          <div className="text-slate-300">Target #{log.target_id}</div>
                          <div className="text-slate-400 mt-1 flex gap-3">
                            <span>Visited: {log.pages}</span>
                            <span>Ads: {log.ads}</span>
                            <span>{log.duration.toFixed(1)}s</span>
                          </div>
                        </div>
                      ))}
                      {liveLogs.length === 0 && (
                        <div className="text-slate-600 text-center mt-10">Waiting for sessions...</div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </>
          )}

          {activeTab === 'explorer' && (
            <WebExplorer />
          )}

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