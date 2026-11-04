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
    if (showFailures && value !== "")
        setFeedback(form, "password", "", result);
    else
        resetFeedback(form, "password");
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

const EDIT_PROFILE_RULES = {
    full_name: {
        test: (v) => /^[a-zA-Zа-яА-ЯёЁ]+([ '-][a-zA-Zа-яА-ЯёЁ]+)*$/.test(v),
        message: "Недопустимые символы в имени",
    },
    email: {
        test: (v) => /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(v),
        message: "Неверный формат почты. Проверьте, пожалуйста, адрес",
    },
    phone_number: {
        test: (v) => /^(\+7|8)\d{10}$/.test(v),
        message: "Неверный формат номера телефона. Проверьте, пожалуйста, номер: (+7|8)XXXXXXXXXX",
    },
}

function checkField(form, field, showFailures = false) {
    const value = form.elements.namedItem(field).value;

    if (value === "") {
        resetFeedback(form, field);
        return true;
    }

    const valid = EDIT_PROFILE_RULES[field].test(value);
    const message = valid ? "" : EDIT_PROFILE_RULES[field].message;

    if (showFailures || !valid) {
        setFeedback(form, field, message, valid);
    } else {
        resetFeedback(form, field);
    }
    return valid;
}



async function setupProfileForm(form) {
    const errorAlert = document.getElementById("error_alert");
    const deleteAvatar = form.elements.namedItem("delete_icon");
    const photoInput = form.elements.namedItem("photo");

    deleteAvatar.addEventListener("change", () => {
        photoInput.disabled = deleteAvatar.checked;
    });

    const fields = ["full_name", "email", "phone_number"];

    fields.forEach(name => {
        const el = form.elements.namedItem(name);
        el.addEventListener("blur", () => checkField(form, name, true));
        el.addEventListener("input", () => resetFeedback(form, name));
    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        clearFeedback(form);

        const fail = fields.map(name => checkField(form, name, true)).includes(false);
        if (fail) return;

        try {
            const response = await fetch(form.action, {
                method: "POST",
                body: new FormData(form),
                headers: { Accept: "application/json" },
            });
            const data = await response.json().catch(() => ({}));

            if (!response.ok) {
                if ([413, 415].includes(response.status)) {
                    setFeedback(form, "photo", data["detail"]);
                }
                errorAlert.classList.remove("d-none");
                errorAlert.querySelector("#message").textContent = data["detail"] || "Что-то пошло не так, попробуйте еще раз";
                return;
            }

            window.location.assign(data.redirect);
        } catch {
            errorAlert.classList.remove("d-none");
            errorAlert.querySelector("#message").textContent = "Не удалось выполнить запрос";
        }
    });
}

document.querySelectorAll("[data-profile-form]").forEach(setupProfileForm);