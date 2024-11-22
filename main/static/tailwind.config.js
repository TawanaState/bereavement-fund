/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./../**/*.html'],
  theme: {
    extend: {
      colors :{
        // Using modern `rgb`
        primary: 'rgb(var(--primary-rgb) / <alpha-value>)',
        secondary : 'rgb(var(--secondary-rgb) / <alpha-value>)',
        highlight : 'rgb(var(--highlight-rgb) / <alpha-value>)',
        color : 'rgb(var(--text-color-rgb) / <alpha-value>)',
        light : 'rgb(var(--light-rgb) / <alpha-value>)'
      }
    },
  },
  plugins: [],
}

