'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, Copy, Check, Loader2 } from 'lucide-react';

export default function Generator() {
  const [prompt, setPrompt] = useState('');
  const [vibe, setVibe] = useState('Professional');
  const [bio, setBio] = useState('');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const generateBio = async () => {
    if (!prompt) return;
    setLoading(true);
    setBio('');
    
    try {
      const response = await fetch('http://localhost:5328/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, vibe }),
      });
      const data = await response.json();
      setBio(data.bio);
    } catch (error) {
      console.error("Error:", error);
      setBio("Error connecting to the creative engine. Please ensure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(bio);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-6">
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="glass-panel rounded-2xl p-8 space-y-6"
      >
        <div className="space-y-2">
          <label className="text-sm text-gray-400 uppercase tracking-wider font-semibold">Describe Yourself</label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g. A software engineer who loves hiking and photography..."
            className="w-full h-32 glass-input rounded-xl p-4 text-lg resize-none"
          />
        </div>

        <div className="space-y-2">
          <label className="text-sm text-gray-400 uppercase tracking-wider font-semibold">Select Vibe</label>
          <div className="flex gap-3 flex-wrap">
            {['Professional', 'Creative', 'Witty', 'Minimalist', 'Bold'].map((v) => (
              <button
                key={v}
                onClick={() => setVibe(v)}
                className={`px-4 py-2 rounded-full text-sm transition-all ${
                  vibe === v 
                    ? 'bg-white text-black font-bold shadow-lg scale-105' 
                    : 'bg-white/5 text-gray-300 hover:bg-white/10'
                }`}
              >
                {v}
              </button>
            ))}
          </div>
        </div>

        <button
          onClick={generateBio}
          disabled={loading || !prompt}
          className="w-full py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl font-bold text-lg shadow-lg hover:shadow-blue-500/25 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 group"
        >
          {loading ? (
            <Loader2 className="w-5 h-5 animate-spin" />
          ) : (
            <>
              <Sparkles className="w-5 h-5 group-hover:rotate-12 transition-transform" />
              Generate Bio
            </>
          )}
        </button>
      </motion.div>

      <AnimatePresence>
        {bio && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            className="mt-8 glass-panel rounded-2xl p-8 relative group"
          >
            <div className="absolute top-4 right-4">
              <button
                onClick={copyToClipboard}
                className="p-2 rounded-lg bg-white/5 hover:bg-white/10 transition-colors"
              >
                {copied ? <Check className="w-5 h-5 text-green-400" /> : <Copy className="w-5 h-5 text-gray-400" />}
              </button>
            </div>
            <h3 className="text-sm text-gray-400 uppercase tracking-wider font-semibold mb-4">Your Bio</h3>
            <p className="text-xl leading-relaxed font-medium text-white/90">{bio}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
