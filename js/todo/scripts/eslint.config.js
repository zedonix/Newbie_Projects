// eslint.config.js
export default [
  {
    files: ["**/*.js"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "script"
    },
    env: {
      browser: true,
      node: true
    },
    rules: {}
  }
]
