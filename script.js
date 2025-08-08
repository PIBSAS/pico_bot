// CONFIGURA TU USUARIO Y REPO
const usuario = "PIBSAS"; // ejemplo: "eliasmonzon"
const repo = "pico_bot";       // ejemplo: "pico_bot"

const listaArchivos = document.getElementById("lista-archivos");

fetch(`https://api.github.com/repos/${usuario}/${repo}/contents/`)
    .then(response => response.json())
    .then(data => {
        data.forEach(file => {
            if (file.name.endsWith(".py") || file.name.endsWith(".pdf")) {
                let nombre = file.name.replace(/\.[^/.]+$/, ""); // sin extensión
                let enlace = document.createElement("a");
                enlace.href = file.download_url;
                enlace.download = file.name;
                enlace.textContent = nombre;

                let li = document.createElement("li");
                li.appendChild(enlace);
                listaArchivos.appendChild(li);
            }
        });
    })
    .catch(error => {
        console.error("Error al cargar archivos:", error);
        listaArchivos.innerHTML = "<li>No se pudieron cargar los archivos.</li>";
    });
