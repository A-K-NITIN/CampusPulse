/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      colors: {
        brand: {
          50: "#eef2ff",
          100: "#e0e7ff",
          500: "#6366f1",
          600: "#4f46e5",
          700: "#4338ca",
        },
        risk: {
          low: "#16a34a",
          medium: "#d97706",
          high: "#dc2626",
        },
      },
      boxShadow: {
        card: "0 1px 2px rgba(15,23,42,0.04), 0 4px 12px rgba(15,23,42,0.04)",
        cardHover: "0 4px 8px rgba(15,23,42,0.06), 0 12px 24px rgba(15,23,42,0.08)",
      },
    },
  },
  plugins: [],
};
