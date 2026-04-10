"use client";

import { useEffect, useState } from 'react';
import styles from './page.module.css';

export default function Home() {
  const [meetings, setMeetings] = useState<any[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    fetchMeetings();
  }, []);

  const fetchMeetings = async () => {
    try {
      const res = await fetch('http://localhost:8000/meetings');
      const data = await res.json();
      setMeetings(data);
    } catch (err) {
      console.error("Failed to fetch meetings:", err);
    }
  };

  const handleUpload = async (e: any) => {
    const file = e.target.files[0];
    if (!file) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      await res.json();
      fetchMeetings();
    } catch (err) {
      console.error("Upload failed:", err);
    } finally {
      setIsUploading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery) return;
    setIsSearching(true);
    try {
      const res = await fetch(`http://localhost:8000/search?query=${encodeURIComponent(searchQuery)}`);
      const data = await res.json();
      setSearchResults(data);
    } catch (err) {
      console.error("Search failed:", err);
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <main className="container">
      <header style={{ padding: '60px 0', textAlign: 'center' }}>
        <h1 style={{ fontSize: '3.5rem', marginBottom: '1rem', background: 'linear-gradient(to right, #ffffff, #00d4ff)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          AI Meeting Assistant
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1.2rem', maxWidth: '600px', margin: '0 auto' }}>
          Transform your ephemeral meetings into persistent, searchable knowledge. Automatically extract summaries, tasks, and decisions.
        </p>
      </header>

      <section className="glass card" style={{ marginBottom: '40px' }}>
        <div className="upload-zone" onClick={() => document.getElementById('fileInput')?.click()}>
          <input 
            type="file" 
            id="fileInput" 
            hidden 
            accept="audio/*,video/*" 
            onChange={handleUpload}
            disabled={isUploading}
          />
          <div style={{ fontSize: '3rem', marginBottom: '20px' }}>{isUploading ? "⚙️" : "☁️"}</div>
          <h3>{isUploading ? "Processing Meeting..." : "Upload Meeting Audio"}</h3>
          <p style={{ color: 'var(--text-muted)' }}>Drag & drop or click to select a file (MP3, WAV, M4A)</p>
          {isUploading && <div className={styles.loader}></div>}
        </div>
      </section>

      <section>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
          <h2>Recent Meetings</h2>
          <div className="glass" style={{ padding: '8px 16px', display: 'flex', alignItems: 'center' }}>
            <span style={{ marginRight: '10px' }}>🔍</span>
            <input 
              type="text" 
              placeholder="Search knowledge..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              style={{ background: 'transparent', border: 'none', color: 'white', outline: 'none' }}
            />
          </div>
        </div>

        {searchResults.length > 0 && (
          <div className="glass" style={{ padding: '24px', marginBottom: '40px', borderColor: 'var(--primary-color)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '15px' }}>
              <h3 style={{ color: 'var(--primary-color)' }}>Knowledge Search Results</h3>
              <button className="btn btn-secondary" style={{ padding: '4px 12px' }} onClick={() => setSearchResults([])}>Clear</button>
            </div>
            {searchResults.map((res, i) => (
              <div key={i} style={{ padding: '15px 0', borderBottom: i < searchResults.length - 1 ? '1px solid var(--border-color)' : 'none' }}>
                <p style={{ fontSize: '0.95rem', lineHeight: '1.5' }}>"{res.content}"</p>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '8px' }}>
                  Source: Meeting ID {res.metadata.meeting_id}
                </div>
              </div>
            ))}
          </div>
        )}

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' }}>
          {meetings.length > 0 ? meetings.map((m) => (
            <div key={m.id} className="glass card">
              <div style={{ color: 'var(--primary-color)', fontSize: '0.8rem', fontWeight: 600, marginBottom: '10px' }}>
                {new Date(m.date).toLocaleDateString()}
              </div>
              <h3>{m.title}</h3>
              <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', margin: '15px 0', lineClamp: 3, display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                {m.summary || "Processing summary..."}
              </p>
              <div style={{ display: 'flex', gap: '10px' }}>
                <button className="btn btn-secondary" style={{ flex: 1, padding: '8px' }}>History</button>
                <button className="btn btn-primary" style={{ flex: 1, padding: '8px' }}>Open Knowledge</button>
              </div>
            </div>
          )) : (
            <div style={{ gridColumn: '1/-1', textAlign: 'center', padding: '100px', color: 'var(--text-muted)' }}>
              No meetings found. Upload your first meeting to get started!
            </div>
          )}
        </div>
      </section>

      <style jsx>{`
        .${styles.loader} {
          width: 48px;
          height: 48px;
          border: 5px solid var(--border-color);
          border-bottom-color: var(--primary-color);
          border-radius: 50%;
          display: inline-block;
          box-sizing: border-box;
          animation: rotation 1s linear infinite;
          margin-top: 20px;
        }

        @keyframes rotation {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </main>
  );
}
