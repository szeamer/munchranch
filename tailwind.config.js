module.exports = {
  content: ["app/templates/**/*.html"],
  theme: {
    extend: {},
  },
  plugins: [require('tailwindcss'),
    require('autoprefixer'),
    require('flowbite/plugin')],
}
