/**
 * CrossGridBackground — subtle "+" pattern grid overlay,
 * a signature visual element from Chakra's design.
 * Pure CSS, no images needed.
 */
function CrossGridBackground({ className = '', opacity = 0.15 }) {
  return (
    <div
      className={`absolute inset-0 pointer-events-none overflow-hidden ${className}`}
      style={{ zIndex: 0 }}
    >
      <svg
        className="absolute inset-0 w-full h-full"
        style={{ opacity }}
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <pattern
            id="cross-grid"
            x="0"
            y="0"
            width="48"
            height="48"
            patternUnits="userSpaceOnUse"
          >
            {/* Horizontal tick */}
            <line
              x1="20"
              y1="24"
              x2="28"
              y2="24"
              stroke="#2DD4BF"
              strokeWidth="1"
            />
            {/* Vertical tick */}
            <line
              x1="24"
              y1="20"
              x2="24"
              y2="28"
              stroke="#2DD4BF"
              strokeWidth="1"
            />
          </pattern>

          {/* Fade mask so grid is strongest at edges, fades toward center */}
          <radialGradient id="grid-fade" cx="50%" cy="50%" r="70%">
            <stop offset="0%" stopColor="white" stopOpacity="0" />
            <stop offset="100%" stopColor="white" stopOpacity="1" />
          </radialGradient>
          <mask id="fade-mask">
            <rect width="100%" height="100%" fill="url(#grid-fade)" />
          </mask>
        </defs>

        <rect
          width="100%"
          height="100%"
          fill="url(#cross-grid)"
          mask="url(#fade-mask)"
        />
      </svg>
    </div>
  );
}

export default CrossGridBackground;
