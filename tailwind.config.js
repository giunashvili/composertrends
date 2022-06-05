module.exports = {
  content: ["./resources/**/*.{html,js}"],
  theme: {
    extend: {
        colors: {
            rose: 'rgb(244, 63, 94)',
        }
    },
  },
  plugins: [
        require('@tailwindcss/forms'),
  ],
}
