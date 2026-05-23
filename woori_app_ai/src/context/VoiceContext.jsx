import { createContext, useContext, useRef, useState, useCallback } from 'react';

const VoiceCtx = createContext(null);

export function VoiceProvider({ children }) {
  const [isPlaying, setIsPlaying]       = useState(false);
  const [activeWordIdx, setActiveWordIdx] = useState(-1);
  const [currentScript, setCurrentScript] = useState('');

  const getKoVoice = () => {
    const voices = window.speechSynthesis?.getVoices() ?? [];
    return voices.find(v => v.lang === 'ko-KR' || v.lang === 'ko_KR') ?? null;
  };

  const speak = useCallback((text) => {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    setCurrentScript(text);
    setActiveWordIdx(-1);

    const utt = new SpeechSynthesisUtterance(text);
    utt.lang   = 'ko-KR';
    utt.rate   = 0.9;
    utt.pitch  = 1.05;
    utt.volume = 1.0;

    const doSpeak = () => {
      const v = getKoVoice();
      if (v) utt.voice = v;
      window.speechSynthesis.speak(utt);
    };

    utt.onboundary = (e) => {
      if (e.name !== 'word') return;
      const idx = text.slice(0, e.charIndex).split(/\s+/).filter(Boolean).length;
      setActiveWordIdx(idx);
    };
    utt.onstart = () => setIsPlaying(true);
    utt.onend   = () => { setIsPlaying(false); setActiveWordIdx(-1); };
    utt.onerror = () => { setIsPlaying(false); setActiveWordIdx(-1); };

    if (window.speechSynthesis.getVoices().length === 0) {
      window.speechSynthesis.onvoiceschanged = doSpeak;
    } else {
      doSpeak();
    }
  }, []);

  const stop = useCallback(() => {
    window.speechSynthesis?.cancel();
    setIsPlaying(false);
    setActiveWordIdx(-1);
  }, []);

  const replay = useCallback(() => {
    if (currentScript) speak(currentScript);
  }, [currentScript, speak]);

  return (
    <VoiceCtx.Provider value={{ isPlaying, activeWordIdx, currentScript, speak, stop, replay }}>
      {children}
    </VoiceCtx.Provider>
  );
}

export const useVoice = () => useContext(VoiceCtx);
