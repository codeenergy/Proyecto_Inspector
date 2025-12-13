import React, { useState } from 'react';
import { BotTarget } from '../types';
import { X, Save, Target, MousePointer2, Eye } from 'lucide-react';

interface CampaignModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (target: any) => void;
  initialData?: BotTarget | null; // Support edit mode
}

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001';

export const CampaignModal: React.FC<CampaignModalProps> = ({ isOpen, onClose, onSave, initialData }) => {
  const [url, setUrl] = useState('');
  const [pageviews, setPageviews] = useState(10);
  const [adProb, setAdProb] = useState(0.2);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Initialize form with data if editing
  React.useEffect(() => {
    if (initialData) {
      setUrl(initialData.url);
      setPageviews(initialData.target_pageviews);
      setAdProb(initialData.ad_click_probability);
    } else {
      setUrl('');
      setPageviews(10);
      setAdProb(0.2);
    }
  }, [initialData, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    const targetData = {
      url,
      target_pageviews: Number(pageviews),
      ad_click_probability: Number(adProb),
      viewport: { width: 1920, height: 1080 }, // Default desktop
      enabled: true
    };

    try {
      let res;
      if (initialData) {
        // Edit Mode
        res = await fetch(`${API_BASE}/targets/${initialData.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(targetData)
        });
      } else {
        // Create Mode
        res = await fetch(`${API_BASE}/targets`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(targetData)
        });
      }

      if (res.ok) {
        onSave(targetData);
        onClose();
      } else {
        alert("Error saving target");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Connection error");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-md p-4 animate-fadeIn">
      {/* Glassmorphism Modal */}
      <div className="relative w-full max-w-lg animate-slideUp">
        {/* Gradient Glow Effect */}
        <div className="absolute -inset-1 bg-gradient-to-r from-blue-600/30 to-purple-600/30 rounded-2xl blur-xl"></div>

        {/* Modal Content */}
        <div className="relative bg-slate-900/90 backdrop-blur-2xl border border-slate-700/50 rounded-2xl shadow-2xl overflow-hidden">
          {/* Gradient Overlay */}
          <div className="absolute inset-0 bg-gradient-to-br from-blue-600/5 to-purple-600/5 pointer-events-none"></div>

          <div className="relative z-10 p-6 md:p-8">
            {/* Header */}
            <div className="flex justify-between items-center mb-6 md:mb-8">
              <div className="flex items-center gap-3">
                <div className="bg-gradient-to-br from-blue-600 to-purple-600 p-2.5 rounded-xl shadow-lg shadow-blue-500/30">
                  <Target className="text-white" size={20} />
                </div>
                <h2 className="text-xl md:text-2xl font-bold text-white">
                  {initialData ? 'Edit Target' : 'Add Traffic Target'}
                </h2>
              </div>
              <button
                onClick={onClose}
                className="text-slate-400 hover:text-white hover:bg-slate-800/50 p-2 rounded-lg transition-all"
              >
                <X size={24} />
              </button>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-5">
              {/* URL Input */}
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Target URL</label>
                <input
                  required
                  type="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  className="w-full bg-slate-950/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all"
                  placeholder="https://example.com/blog-post"
                />
              </div>

              {/* Grid Inputs */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2 flex items-center gap-2">
                    <Eye size={16} className="text-blue-400" /> Pages / Session
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="50"
                    value={pageviews}
                    onChange={(e) => setPageviews(Number(e.target.value))}
                    className="w-full bg-slate-950/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-2 flex items-center gap-2">
                    <MousePointer2 size={16} className="text-purple-400" /> Ad Click %
                  </label>
                  <input
                    type="number"
                    min="0"
                    max="1.0"
                    step="0.05"
                    value={adProb}
                    onChange={(e) => setAdProb(Number(e.target.value))}
                    className="w-full bg-slate-950/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all"
                  />
                  <p className="text-xs text-slate-500 mt-1.5">0.0 to 1.0 (e.g. 0.2 = 20%)</p>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="pt-4 flex flex-col sm:flex-row gap-3 sm:justify-end">
                <button
                  type="button"
                  onClick={onClose}
                  className="w-full sm:w-auto px-6 py-3 rounded-xl bg-slate-800/50 border border-slate-700/50 text-slate-300 hover:bg-slate-700/50 hover:text-white transition-all"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full sm:w-auto px-6 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-medium flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50"
                >
                  {isSubmitting ? (
                    <>
                      <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                      <span>Saving...</span>
                    </>
                  ) : (
                    <>
                      <Save size={18} />
                      <span>{initialData ? 'Update Target' : 'Create Target'}</span>
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <style>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes slideUp {
          from { transform: translateY(20px); opacity: 0; }
          to { transform: translateY(0); opacity: 1; }
        }
        .animate-fadeIn {
          animation: fadeIn 0.2s ease-out;
        }
        .animate-slideUp {
          animation: slideUp 0.3s ease-out;
        }
      `}</style>
    </div>
  );
};