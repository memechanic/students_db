const USERNAME_RULE = [
    {
        test: (v) => v.length >= 3 && v.length <= 30,
        message: "Имя пользователя должно содержать от 3 до 30 символов",
    },
    {
        test: (v) => /[A-Za-z]+/.test(v),
        message: "Имя пользователя не может содержать только цифры или _"
    },
    {
        test: (v) => /^[A-Za-z_0-9]+$/.test(v),
        message: "Имя пользователя может содержать латинские буквы, цифры или _"
    }
];

const PASSWORD_RULES = {
    length: v => v.length >= 8,
    uppercase: v => /[A-Z]/.test(v),
    lowercase: v => /[a-z]/.test(v),
    digit: v => /[0-9]/.test(v),
    special: v => /[()!@#$%^&*]/.test(v),
};

const RULE_STYLES = {
    idle: { text: "text-body-secondary", icon: "bi-record" },
    ok: { text: "text-success", icon: "bi-check" },
    fail: { text: "text-danger", icon: "bi-x" },
};


function setFeedback(form, fieldName, message, valid = false) {
    const input = form.elements.namedItem(fieldName);
    const feedback = form.querySelector(`[data-error-field="${fieldName}"]`);

    input?.classList.toggle("is-invalid", !valid);
    input?.classList.toggle("is-valid", valid);

    if (feedback) feedback.textContent = message;
}

function resetFeedback(form, fieldName) {
    form.elements.namedItem(fieldName).classList.remove("is-valid", "is-invalid");
    const feedback = form.querySelector(`[data-error-field="${fieldName}"]`);
    if (feedback) feedback.textContent = "";
}

function clearFeedback(form) {
    form.querySelectorAll(".is-invalid, .is-valid")
        .forEach(el => el.classList.remove("is-invalid", "is-valid"));
    form.querySelectorAll("[data-error-field]")
        .forEach(el => { el.textContent = ""; });
}

function checkUsername(form) {
    const value = form.elements.namedItem("username").value;

    const failedRule = USERNAME_RULE.find((rule) => !rule.test(value));
    const valid = !failedRule;
    const message = failedRule ? failedRule.message : "";

    setFeedback(form, "username", message, valid);
    return valid;
}

function checkPassword(form, showFailures) {
    const value = form.elements.namedItem("password").value;

    form.querySelectorAll("#password-rules [data-rule]").forEach((item) => {
        const passed = PASSWORD_RULES[item.dataset.rule](value);
        const state = passed ? "ok" : showFailures && value ? "fail" : "idle";  //if elif else

        item.className = RULE_STYLES[state].text;
        item.querySelector("i").className = `bi ${RULE_STYLES[state].icon}`;
    });
    const result = Object.values(PASSWORD_RULES).every(test => test(value));

    setFeedback(form, "password", "", result)
    return result
}

function checkRepeatPassword(form) {
    const password = form.elements.namedItem("password");
    const repeat = form.elements.namedItem("repeat_password");

    if (password.value === "" && repeat.value === "") {
        resetFeedback(form, "repeat_password");
        return true;
    }

    const valid = repeat.value !== "" && repeat.value === password.value;
    setFeedback(form, "repeat_password", valid ? "" : "Пароли не совпадают", valid);
    return valid;
}

function setupPasswordToggles(form) {
    form.querySelectorAll(".eye-btn").forEach((button) => {
        button.addEventListener("click", () => {
            const input = document.getElementById(button.dataset.input);
            const icon = button.querySelector("i");
            const isHidden = input.type === "password";

            input.type = isHidden ? "text" : "password";
            icon.classList.toggle("bi-eye", isHidden);
            icon.classList.toggle("bi-eye-slash", !isHidden);
        });
    });
}

function setupRegistration(form) {
    const username = form.elements.namedItem("username");
    const password = form.elements.namedItem("password");
    const repeat = form.elements.namedItem("repeat_password");

    username.addEventListener("input", () => resetFeedback(form, "username"));
    username.addEventListener("blur", () => checkUsername(form));

    password.addEventListener("input", () => {
        checkPassword(form, false);
        resetFeedback(form, "repeat_password");
    });
    password.addEventListener("blur", () => checkPassword(form, true));

    repeat.addEventListener("input", () => resetFeedback(form, "repeat_password"));
    repeat.addEventListener("blur", () => checkRepeatPassword(form));

    setupPasswordToggles(form);
    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        clearFeedback(form);

        const results = [
            checkUsername(form),
            checkPassword(form, true),
            checkRepeatPassword(form),
        ];
        if (results.includes(false)) return;

        await submitAuthForm(form);
    });
}

function setupLogin(form) {
    const resetAllFeedback = () => {
        resetFeedback(form, "username");
        resetFeedback(form, "password");
    };
    ["username", "password"].forEach(name => {
        const el = form.elements.namedItem(name);
        el.addEventListener("input", resetAllFeedback);
        el.addEventListener("blur", resetAllFeedback);
    });

    setupPasswordToggles(form);
    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        clearFeedback(form);
        await submitAuthForm(form);
    });
}

async function submitAuthForm(form) {
    try {
        const response = await fetch(form.action, {
            method: "POST",
            body: new FormData(form),
            headers: { Accept: "application/json" },
        });

        const data = await response.json().catch(() => { });

        if (!response.ok) {
            setFeedback(form, "username", data.message || "Не удалось выполнить запрос. Попробуйте еще раз");
            return;
        }

        if (data.redirect) window.location.assign(data.redirect);
    } catch {
        setFeedback(form, "username", "Не удалось выполнить запрос. Попробуйте еще раз");
    }
}

document.querySelectorAll("[data-auth-form]").forEach(form => {
    const type = form.dataset.authForm;
    if (type === "login") setupLogin(form);
    else if (type === "register") setupRegistration(form);
});



// Редактирование профиля

async function setupProfileForm(form) {
    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        try {
            const response = await fetch(form.action, {
                method: "POST",
                body: new FormData(form),
                headers: { Accept: "application/json" },
            });
            const data = await response.json().catch(() => ({}));

            if (!response.ok) {
                alert(JSON.stringify(data) || "Не удалось сохранить");
                return;
            }

            window.location.assign(data.redirect);
        } catch {
            alert("Не удалось выполнить запрос");
        }
    });
}

document.querySelectorAll("[data-profile-form]").forEach(setupProfileForm);