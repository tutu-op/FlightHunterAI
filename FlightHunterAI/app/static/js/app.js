const formulario = document.getElementById("busqueda");
const resultados = document.getElementById("resultados");

formulario.addEventListener("submit", async function (e) {

    e.preventDefault();

    resultados.innerHTML = `
        <h2 style="color:white;text-align:center;">
            🔍 Buscando los mejores vuelos...
        </h2>
    `;

    const origen = document.getElementById("origen").value.toUpperCase();
    const destino = document.getElementById("destino").value.toUpperCase();
    const fecha_salida = document.getElementById("fecha_salida").value;
    const fecha_regreso = document.getElementById("fecha_regreso").value;
    const adultos = document.getElementById("adultos").value;

    try {

        const respuesta = await fetch(
            `/vuelos?origen=${origen}&destino=${destino}&fecha_salida=${fecha_salida}&fecha_regreso=${fecha_regreso}&adultos=${adultos}`
        );

        const vuelos = await respuesta.json();

        resultados.innerHTML = "";

        if (vuelos.length === 0) {

            resultados.innerHTML = `
                <div class="tarjeta">
                    <h2>No se encontraron vuelos.</h2>
                </div>
            `;

            return;
        }

        vuelos.forEach(vuelo => {

            resultados.innerHTML += `

            <div class="tarjeta">

                <div class="encabezado">

                    <div class="aerolinea">
                        ✈ ${vuelo.aerolinea}
                    </div>

                    <div class="precio">
                        $${Number(vuelo.precio).toLocaleString()} ${vuelo.moneda}
                    </div>

                </div>

                <div class="info">

                    <div class="item">
                        <div class="titulo">Proveedor</div>
                        <div class="valor">${vuelo.proveedor}</div>
                    </div>

                    <div class="item">
                        <div class="titulo">Origen</div>
                        <div class="valor">${vuelo.origen}</div>
                    </div>

                    <div class="item">
                        <div class="titulo">Destino</div>
                        <div class="valor">${vuelo.destino}</div>
                    </div>

                    <div class="item">
                        <div class="titulo">Salida</div>
                        <div class="valor">${vuelo.salida}</div>
                    </div>

                    <div class="item">
                        <div class="titulo">Llegada</div>
                        <div class="valor">${vuelo.llegada}</div>
                    </div>

                    <div class="item">
                        <div class="titulo">Escalas</div>
                        <div class="valor">${vuelo.escalas}</div>
                    </div>

                </div>

            </div>

            `;

        });

    } catch (error) {

        console.error(error);

        resultados.innerHTML = `
            <div class="tarjeta">
                <h2>Error al consultar los vuelos.</h2>
            </div>
        `;
    }

});