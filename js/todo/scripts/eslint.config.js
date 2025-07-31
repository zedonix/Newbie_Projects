export default [
    {
        files: ["**/*.js"],
        languageOptions: {
            ecmaVersion: "latest",
            sourceType: "script",
            globals: {
                window: true,
                document: true,
                console: true,
                setTimeout: true,
                clearTimeout: true,
                setInterval: true,
                clearInterval: true,
                alert: true,
                prompt: true,
                confirm: true,
                location: true,
                navigator: true,
                history: true,
            },
        },
        rules: {
            "no-unused-vars": "warn",
            "no-undef": "error",
            "no-console": "off",
            "eqeqeq": "warn",
            "curly": ["error", "multi"],
            "no-empty": "warn",
            "no-fallthrough": "error",
            "no-redeclare": "error",
        },
    },
];
