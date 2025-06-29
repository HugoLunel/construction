/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./**/*.html",
    "./src/**/*.{js,jsx,ts,tsx,vue}",
  ],
  theme: {
    extend: {
      fontFamily: {
        inter: ['Inter', '"Noto Sans"', 'sans-serif'],
      },
      minWidth: {
        40: '10rem',
      },
      minHeight: {
        36: '9rem',
      },
      colors: {
        'slate-50': '#f8fafc',
        '0d141c': '#0d141c',
        'e7edf4': '#e7edf4',
        '49739c': '#49739c',
        '0c7ff2': '#0c7ff2',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries'),
  ],
}
