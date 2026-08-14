/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{ts,tsx}"],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {
      colors: {
        forest: "#2E4A3F",
        moss: "#5B7361",
        sage: "#8DA590",
        clay: "#B07A5B",
        stone: "#E8E2D5",
        cream: "#F7F4ED",
      },
    },
  },
  plugins: [],
};
