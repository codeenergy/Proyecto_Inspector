import React, { useState } from 'react';
import { BotTarget } from '../types';
import { X, Save, Target, MousePointer2, Eye } from 'lucide-react';

interface CampaignModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (target: any) => void;
  initialData?: BotTarget | null; // Support edit mode
}

const API_BASE = 'http://localhost:8001';

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
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm">
      <div className="bg-slate-900 border border-slate-700 rounded-xl shadow-2xl w-full max-w-lg p-6">
        <div className="flex justify-between items-center mb-6">
          <div className="flex items-center gap-2">
            <Target className="text-blue-500" />
            <h2 className="text-xl font-bold text-white">
              {initialData ? 'Edit Target' : 'Add Traffic Target'}
            </h2>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors">
            <X size={24} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-1">Target URL</label>
            <input
              required
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="https://example.com/blog-post"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-1 flex items-center gap-2">
                <Eye size={16} /> Pages / Session
              </label>
              <input
                type="number"
                min="1"
                max="50"
                value={pageviews}
                onChange={(e) => setPageviews(Number(e.target.value))}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-400 mb-1 flex items-center gap-2">
                <MousePointer2 size={16} /> Ad Click %
              </label>
              <input
                type="number"
                min="0"
                max="1.0"
                step="0.05"
                value={adProb}
                onChange={(e) => setAdProb(Number(e.target.value))}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <p className="text-xs text-slate-500 mt-1">0.0 to 1.0 (e.g. 0.2 = 20%)</p>
            </div>
          </div>

          <div className="pt-4 flex justify-end space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-500 flex items-center space-x-2 transition-colors disabled:opacity-50"
            >
              <Save size={18} />
              <span>{isSubmitting ? 'Creating...' : 'Create Target'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};