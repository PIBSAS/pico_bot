// CONFIGURA TU USUARIO Y REPO
const usuario = "PIBSAS"; // ejemplo: "eliasmonzon"
const repo = "pico_bot";       // ejemplo: "pico_bot"

const listaArchivos = document.getElementById("lista-archivos");
const listaPDF = document.getElementById("lista-pdf");

let orden = ["Pico_bot"];
for (let i = 1; i <= 99; i++) {
    orden.push(`Leccion_${i}`);
}
orden.push("motores y servo", "mando", "ssd1306");

fetch(`https://api.github.com/repos/${usuario}/${repo}/contents/`)
    .then(response => response.json())
    .then(data => {
        let archivosPy = [];
        let archivosPDF = [];

        data.forEach(file => {
            if (file.name.endsWith(".py")) {
                archivosPy.push({
                    nombre: file.name.replace(/\.[^/.]+$/, ""),
                    url: file.download_url
                });
            } else if (file.name.endsWith(".pdf")) {
                archivosPDF.push({
                    nombre: file.name.replace(/\.[^/.]+$/, ""),
                    url: file.download_url
                });
            }
        });

        archivosPy.sort((a, b) => {
            let ia = orden.indexOf(a.nombre);
            let ib = orden.indexOf(b.nombre);
            ia = ia === -1 ? Number.MAX_SAFE_INTEGER : ia;
            ib = ib === -1 ? Number.MAX_SAFE_INTEGER : ib;
            return ia - ib;
        });

        archivosPy.forEach(archivo => {
            let li = document.createElement("li");
            let enlace = document.createElement("a");
            enlace.href = archivo.url;
            enlace.download = archivo.nombre + ".py";
            enlace.textContent = archivo.nombre;
            li.appendChild(enlace);
            listaArchivos.appendChild(li);
        });

        archivosPDF.forEach(pdf => {
            let li = document.createElement("li");
            let enlace = document.createElement("a");
            enlace.href = pdf.url;
            enlace.download = pdf.nombre + ".pdf";
            enlace.textContent = `${pdf.nombre} (PDF)`;
            li.appendChild(enlace);
            listaPDF.appendChild(li);
        });
    })
    .catch(error => {
        console.error("Error al cargar archivos:", error);
        listaArchivos.innerHTML = "<li>No se pudieron cargar los archivos.</li>";
    });
