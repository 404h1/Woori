export default function BotAvatar({ size = 44 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ flexShrink: 0 }}>
      <circle cx="22" cy="22" r="22" fill="#4899E8" />
      <rect x="20.5" y="5" width="3" height="8" rx="1.5" fill="white" opacity="0.9" />
      <circle cx="22" cy="4.5" r="2.5" fill="white" />
      <rect x="8" y="13" width="28" height="21" rx="7" fill="white" />
      <circle cx="16.5" cy="22" r="3.5" fill="#1b64da" />
      <circle cx="27.5" cy="22" r="3.5" fill="#1b64da" />
      <circle cx="17.5" cy="21" r="1.2" fill="white" />
      <circle cx="28.5" cy="21" r="1.2" fill="white" />
      <path d="M17 28 Q22 31.5 27 28" stroke="#1b64da" strokeWidth="1.8" strokeLinecap="round" fill="none" />
      <path d="M8 22 Q8 13 22 13 Q36 13 36 22" stroke="#1b64da" strokeWidth="2.5" strokeLinecap="round" fill="none" />
      <rect x="5.5" y="20.5" width="4" height="6" rx="2" fill="#1b64da" />
      <rect x="34.5" y="20.5" width="4" height="6" rx="2" fill="#1b64da" />
    </svg>
  );
}
