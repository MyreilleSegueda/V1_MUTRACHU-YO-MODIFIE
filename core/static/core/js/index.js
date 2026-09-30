document.addEventListener("DOMContentLoaded", function () {

    // SIDEBAR MOBILE
    const toggle = document.getElementById("sidebarToggle");
    const sidebar = document.querySelector(".sidebar");

    toggle?.addEventListener("click", function () {
        sidebar.classList.toggle("open");
    });


    // =====================================================
    // EVOLUTION DES ENROLEMENTS
    // =====================================================

    const enrolmentCanvas =
        document.getElementById("enrolmentChart");

    if (enrolmentCanvas) {

        new Chart(enrolmentCanvas, {

            type: "line",

            data: {

                labels: [
                    "Jan",
                    "Fév",
                    "Mar",
                    "Avr",
                    "Mai",
                    "Juin",
                    "Juil",
                    "Août",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Déc"
                ],

                datasets: [{
                    data: [
                        25,
                        50,
                        70,
                        95,
                        95,
                        125,
                        120,
                        150,
                        165,
                        200,
                        200,
                        220
                    ],

                    borderColor: "#1687f8",
                    backgroundColor: "rgba(22,135,248,.12)",

                    borderWidth: 2,

                    pointBackgroundColor: "#1687f8",
                    pointBorderColor: "#1687f8",

                    pointRadius: 4,
                    pointHoverRadius: 5,

                    tension: 0,

                    fill: true
                }]

            },

            options: {

                responsive: true,
                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        display: false
                    }

                },

                scales: {

                    x: {

                        grid: {
                            color: "#edf2f7"
                        },

                        border: {
                            display: false
                        },

                        ticks: {
                            color: "#435d82",
                            font: {
                                size: 11
                            }
                        }

                    },

                    y: {

                        beginAtZero: true,
                        max: 250,

                        ticks: {
                            stepSize: 50,
                            color: "#435d82",
                            font: {
                                size: 11
                            }
                        },

                        grid: {
                            color: "#e6eef6"
                        },

                        border: {
                            display: false
                        }

                    }

                }

            }

        });

    }


    // =====================================================
    // REPARTITION HOMMES / FEMMES
    // =====================================================

    const genderCanvas =
        document.getElementById("genderChart");

    if (genderCanvas) {

        new Chart(genderCanvas, {

            type: "doughnut",

            data: {

                labels: [
                    "Hommes",
                    "Femmes"
                ],

                datasets: [{
                    data: [62, 38],

                    backgroundColor: [
                        "#2794f7",
                        "#fb536b"
                    ],

                    borderColor: "#ffffff",
                    borderWidth: 2,

                    hoverOffset: 0
                }]

            },

            options: {

                responsive: true,
                maintainAspectRatio: false,

                cutout: "52%",

                plugins: {

                    legend: {
                        display: false
                    },

                    tooltip: {
                        enabled: true
                    }

                }

            }

        });

    }


    // =====================================================
    // TRANCHES D'AGE
    // =====================================================

    const ageCanvas =
        document.getElementById("ageChart");

    if (ageCanvas) {

        new Chart(ageCanvas, {

            type: "bar",

            data: {

                labels: [
                    "0 - 5 ans",
                    "6 - 10 ans",
                    "11 - 15 ans",
                    "16 - 20 ans",
                    "21 ans et +"
                ],

                datasets: [{
                    data: [
                        480,
                        980,
                        1120,
                        920,
                        419
                    ],

                    backgroundColor: [
                        "#5ba7ef",
                        "#55c77b",
                        "#ffac3c",
                        "#9862e9",
                        "#f84d62"
                    ],

                    borderRadius: 5,

                    maxBarThickness: 64
                }]

            },

            options: {

                responsive: true,
                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        display: false
                    }

                },

                scales: {

                    x: {

                        grid: {
                            display: false
                        },

                        border: {
                            display: false
                        },

                        ticks: {
                            color: "#17325f",
                            font: {
                                size: 11,
                                weight: "600"
                            }
                        }

                    },

                    y: {

                        beginAtZero: true,
                        max: 1200,

                        ticks: {
                            stepSize: 300,
                            color: "#435d82",
                            font: {
                                size: 11
                            }
                        },

                        grid: {
                            color: "#e6eef6"
                        },

                        border: {
                            display: false
                        }

                    }

                }

            },

            plugins: [{

                afterDatasetsDraw(chart) {

                    const ctx = chart.ctx;

                    ctx.save();

                    ctx.font = "bold 13px Inter";
                    ctx.fillStyle = "#0a2454";
                    ctx.textAlign = "center";

                    chart.getDatasetMeta(0).data.forEach(
                        (bar, index) => {

                            const value =
                                chart.data.datasets[0].data[index];

                            ctx.fillText(
                                value.toLocaleString("fr-FR"),
                                bar.x,
                                bar.y - 9
                            );

                        }
                    );

                    ctx.restore();

                }

            }]

        });

    }

});