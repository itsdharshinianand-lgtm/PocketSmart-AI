async function api(url, options = {}) {

    const response = await fetch(
        url,
        {
            credentials: "same-origin",
            ...options
        }
    );


    const data =
        await response
            .json()
            .catch(() => ({}));


    if (!response.ok) {

        throw new Error(
            data.detail ||
            "Request failed"
        );

    }


    return data;
}


function money(number) {

    return new Intl.NumberFormat(
        "en-IN",
        {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 0
        }
    ).format(number || 0);
}


function escapeHtml(value) {

    return String(
        value ?? ""
    ).replace(
        /[&<>"']/g,
        character => {

            const map = {

                "&": "&amp;",
                "<": "&lt;",
                ">": "&gt;",
                '"': "&quot;",
                "'": "&#039;"

            };

            return map[character];

        }
    );
}


function escapeAttr(value) {

    return String(
        value ?? ""
    ).replace(
        /"/g,
        "&quot;"
    );
}


function renderResults(data) {

    const results =
        document.querySelector(
            "#results"
        );


    if (!results) {
        return;
    }


    results.innerHTML = `

        <div class="result-head">

            <div>

                <span class="badge">

                    ${
                        data.ai_powered
                        ? "GEMINI AI"
                        : "DEMO FALLBACK"
                    }

                </span>


                <h2>
                    ${escapeHtml(data.summary)}
                </h2>

            </div>


            <div>

                <strong>
                    Total:
                    ${money(data.total_estimated)}
                </strong>

                <br>

                <span class="meta">

                    Remaining:
                    ${money(data.remaining_budget)}

                </span>

            </div>

        </div>


        <div class="result-grid">

            ${
                data.recommendations
                    .map(item => `

                    <article class="recommendation">

                        <h3>
                            ${escapeHtml(item.name)}
                        </h3>


                        <div class="price">

                            ${money(
                                item.estimated_price
                            )}

                            ×

                            ${item.quantity}

                        </div>


                        <p class="meta">

                            ${escapeHtml(
                                item.category
                            )}

                            ·

                            ${escapeHtml(
                                item.platform
                            )}

                        </p>


                        <p>

                            ${escapeHtml(
                                item.reason
                            )}

                        </p>


                        <a
                            href="${escapeAttr(
                                item.url
                            )}"
                            target="_blank"
                            rel="noopener"
                        >

                            Search on
                            ${escapeHtml(
                                item.platform
                            )}

                            →

                        </a>

                    </article>

                `)
                .join("")
            }

        </div>
    `;
}


document.addEventListener(
    "DOMContentLoaded",
    () => {


        // --------------------------------
        // LOGIN
        // --------------------------------

        const login =
            document.querySelector(
                "#login-form"
            );


        if (login) {

            login.addEventListener(
                "submit",
                async event => {

                    event.preventDefault();


                    const message =
                        document.querySelector(
                            "#form-message"
                        );


                    try {

                        const body =
                            Object.fromEntries(
                                new FormData(login)
                            );


                        await api(
                            "/login",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body:
                                    JSON.stringify(body)
                            }
                        );


                        window.location.href =
                            "/dashboard";


                    } catch (error) {

                        message.textContent =
                            error.message;

                        message.className =
                            "message error";

                    }

                }
            );

        }


        // --------------------------------
        // REGISTER
        // --------------------------------

        const register =
            document.querySelector(
                "#register-form"
            );


        if (register) {

            register.addEventListener(
                "submit",
                async event => {

                    event.preventDefault();


                    const message =
                        document.querySelector(
                            "#form-message"
                        );


                    try {

                        const body =
                            Object.fromEntries(
                                new FormData(register)
                            );


                        await api(
                            "/register",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body:
                                    JSON.stringify(body)
                            }
                        );


                        window.location.href =
                            "/dashboard";


                    } catch (error) {

                        message.textContent =
                            error.message;

                        message.className =
                            "message error";

                    }

                }
            );

        }


        // --------------------------------
        // PLANNERS
        // --------------------------------

        const form =
            document.querySelector(
                "#planner-form"
            );


        if (form) {

            form.addEventListener(
                "submit",
                async event => {

                    event.preventDefault();


                    const message =
                        document.querySelector(
                            "#form-message"
                        );


                    message.textContent =
                        "Generating recommendations...";


                    try {

                        const formData =
                            new FormData(form);


                        // HOME
                        if (
                            form.dataset.endpoint
                            === "/generate-home"
                        ) {

                            const rooms =
                                String(
                                    formData.get(
                                        "rooms"
                                    ) || ""
                                )
                                .split(",")
                                .map(
                                    value =>
                                        value.trim()
                                )
                                .filter(Boolean);


                            formData.delete(
                                "rooms"
                            );


                            const payload =
                                Object.fromEntries(
                                    formData
                                );


                            payload.budget =
                                Number(
                                    payload.budget
                                );


                            payload.rooms =
                                rooms;


                            const data =
                                await api(
                                    form.dataset.endpoint,
                                    {
                                        method: "POST",

                                        headers: {
                                            "Content-Type":
                                                "application/json"
                                        },

                                        body:
                                            JSON.stringify(
                                                payload
                                            )
                                    }
                                );


                            renderResults(
                                data
                            );

                        }


                        // PARTY
                        else if (
                            form.dataset.endpoint
                            === "/generate-party"
                        ) {

                            const payload =
                                Object.fromEntries(
                                    formData
                                );


                            payload.budget =
                                Number(
                                    payload.budget
                                );


                            payload.guests =
                                Number(
                                    payload.guests
                                );


                            const data =
                                await api(
                                    form.dataset.endpoint,
                                    {
                                        method: "POST",

                                        headers: {
                                            "Content-Type":
                                                "application/json"
                                        },

                                        body:
                                            JSON.stringify(
                                                payload
                                            )
                                    }
                                );


                            renderResults(
                                data
                            );

                        }


                        // JEWELRY
                        else {

                            const data =
                                await api(
                                    form.dataset.endpoint,
                                    {
                                        method: "POST",

                                        body:
                                            formData
                                    }
                                );


                            renderResults(
                                data
                            );

                        }


                        message.textContent =
                            "Recommendations generated successfully.";

                        message.className =
                            "message success";


                    } catch (error) {

                        message.textContent =
                            error.message;

                        message.className =
                            "message error";

                    }

                }
            );

        }


        // --------------------------------
        // HISTORY
        // --------------------------------

        const history =
            document.querySelector(
                "#history-list"
            );


        if (history) {

            (async () => {

                try {

                    const data =
                        await api(
                            "/history"
                        );


                    if (!data.length) {

                        history.innerHTML =
                            `
                            <div class="card">

                                No recommendations yet.

                            </div>
                            `;

                        return;

                    }


                    history.innerHTML =
                        data
                            .map(
                                item => `

                                <article class="card">

                                    <h3>

                                        ${escapeHtml(
                                            item.planner
                                        )}
                                        planner

                                    </h3>


                                    <p>

                                        ${money(
                                            item.budget
                                        )}

                                    </p>


                                    <a
                                        href="/recommendations-details/${item.id}"
                                        target="_blank"
                                    >

                                        Open result →

                                    </a>

                                </article>

                            `
                            )
                            .join("");


                } catch (error) {

                    const message =
                        document.querySelector(
                            "#history-message"
                        );


                    if (message) {

                        message.textContent =
                            error.message;

                    }

                }

            })();

        }


        // --------------------------------
        // DASHBOARD USER
        // --------------------------------

        const welcome =
            document.querySelector(
                "#welcome"
            );


        if (welcome) {

            api(
                "/session-info"
            )

                .then(
                    data => {

                        welcome.textContent =
                            `Welcome, ${data.name}`;

                    }
                )

                .catch(
                    () => {}
                );

        }

    }
);