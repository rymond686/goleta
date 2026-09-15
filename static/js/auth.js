(() => {
    const root = document.querySelector("[data-auth-app]");
    if (!root || !window.Vue) {
        return;
    }

    const state = window.Vue.reactive({
        loginPassword: "",
        password: "",
        passwordConfirmation: "",
        showLoginPassword: false,
        showPassword: false,
        showPasswordConfirmation: false,
    });

    root.querySelectorAll("[data-password-input]").forEach((input) => {
        const stateKey = input.dataset.passwordInput;
        state[stateKey] = input.value;
        input.addEventListener("input", () => {
            state[stateKey] = input.value;
        });
    });

    root.querySelectorAll("[data-password-toggle]").forEach((button) => {
        button.addEventListener("click", () => {
            const input = document.getElementById(button.dataset.passwordToggle);
            const stateKey = button.dataset.passwordState;
            if (!input || !(stateKey in state)) return;

            state[stateKey] = !state[stateKey];
            input.type = state[stateKey] ? "text" : "password";
            button.setAttribute("aria-pressed", state[stateKey].toString());
            const label = button.querySelector("[data-toggle-label]");
            if (label) label.textContent = state[stateKey] ? "Hide" : "Show";
            input.focus();
        });
    });

    window.Vue.watchEffect(() => {
        const hasLength = state.password.length >= 8;
        const hasLetterAndNumber = /[A-Za-z]/.test(state.password) && /\d/.test(state.password);
        const strengthScore = state.password
            ? [
                  hasLength,
                  /[A-Za-z]/.test(state.password),
                  /\d/.test(state.password),
                  /[^A-Za-z0-9]/.test(state.password),
              ].filter(Boolean).length
            : 0;
        const strengthLabel = ["Enter a password", "Weak", "Fair", "Good", "Strong"][strengthScore];

        const meter = root.querySelector("[data-strength-meter]");
        if (meter) meter.value = strengthScore;

        const label = root.querySelector("[data-strength-label]");
        if (label) label.textContent = strengthLabel;

        const rules = { length: hasLength, mixed: hasLetterAndNumber };
        root.querySelectorAll("[data-password-rule]").forEach((icon) => {
            const isSatisfied = rules[icon.dataset.passwordRule];
            icon.classList.toggle("bi-circle", !isSatisfied);
            icon.classList.toggle("bi-check-circle-fill", isSatisfied);
            icon.classList.toggle("rule-pass", isSatisfied);
        });

        const match = root.querySelector("[data-password-match]");
        if (match) {
            const passwordsMatch = Boolean(state.passwordConfirmation) && state.password === state.passwordConfirmation;
            match.textContent = !state.passwordConfirmation
                ? "Repeat your password."
                : passwordsMatch
                  ? "Passwords match."
                  : "Passwords do not match yet.";
            match.classList.toggle("rule-pass", passwordsMatch);
        }
    });
})();
