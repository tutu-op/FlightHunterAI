const formulario = document.getElementById("busqueda");
const resultados = document.getElementById("resultados");

const origenInput = document.getElementById("origen");
const destinoInput = document.getElementById("destino");

const sugerenciasOrigen = document.getElementById("sugerenciasOrigen");
const sugerenciasDestino = document.getElementById("sugerenciasDestino");

formulario.addEventListener("submit", async function (e) {

    e.preventDefault();

    resultados.innerHTML = `
        <h2 style="text-align:center;">
            🔍 Buscando los mejores vuelos...
        </h2>
    `;

    const origen = origenInput.dataset.iata || origenInput.value.toUpperCase();
    const destino = destinoInput.dataset.iata || destinoInput.value.toUpperCase();

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

        vuelos.forEach((vuelo, indice) => {

    resultados.innerHTML += `

    <div class="tarjeta">

        <div class="encabezado">

            <div class="aerolinea">

                <div style="display:flex;align-items:center;gap:12px;">

                    <img
                        src="https://images.kiwi.com/airlines/64/${vuelo.codigo_aerolinea}.png"
                        class="logo-aerolinea"
                        alt="${vuelo.aerolinea}"
                        onerror="this.style.display='none';"
                    />

                    <div>

                        <div style="font-weight:bold;font-size:18px;">
                            ${vuelo.aerolinea}
                        </div>

                        <small style="color:#666;">
                            ${vuelo.proveedor}
                        </small>

                    </div>

                </div>

                ${
                    indice === 0
                    ? '<span class="badge mejor">🏆 Mejor opción</span>'
                    : ''
                }

            </div>

            <div class="precio">

                $${Number(vuelo.precio).toLocaleString()}
                <small>${vuelo.moneda}</small>

            </div>

        </div>


        <div class="ruta">

            <div class="ciudad">

                <div class="hora">
                    ${vuelo.salida ? vuelo.salida.substring(11,16) : "-"}
                </div>

                <div class="codigo">
                    ${vuelo.origen}
                </div>

            </div>


            <div class="centro">

                <div class="linea"></div>

                <div class="escalas">

                    ${
                        vuelo.escalas==0
                        ? "🟢 Directo"
                        : `🟠 ${vuelo.escalas} escala(s)`
                    }

                </div>

                ${
                    vuelo.duracion
                    ? `<div class="duracion">${vuelo.duracion}</div>`
                    : ""
                }

            </div>


            <div class="ciudad">

                <div class="hora">
                   ${vuelo.llegada ? vuelo.llegada.substring(11,16) : "-"}
                </div>

                <div class="codigo">
                    ${vuelo.destino}
                </div>

            </div>

        </div>


        ${
            vuelo.score
            ?

            `<div class="score">

                <div class="score-header">

                    ⭐ FlightHunter Score

                    <span>${vuelo.score}/100</span>

                </div>

                <div class="barra-score">

                    <div
                        class="barra-score-fill"
                        style="width:${vuelo.score}%">
                    </div>

                </div>

                <ul>

                    ${(vuelo.razones || []).map(r=>`<li>${r}</li>`).join("")}

                </ul>

            </div>`

            : ""

        }


        ${
            vuelo.offer_id
            ?

            `<button
                class="boton-reservar"
                onclick="reservar('${vuelo.offer_id}')">

                ✈ Reservar

            </button>`

            :

            `<button
                class="boton-reservar"
                disabled>

                Próximamente

            </button>`

        }

    </div>

    `;

});

    }

    catch(error){

        console.error(error);

        resultados.innerHTML = `
            <div class="tarjeta">
                <h2>Error al consultar los vuelos.</h2>
            </div>
        `;

    }

});

async function autocompletar(input, contenedor){

    const texto = input.value.trim();

    if(texto.length < 2){

        contenedor.innerHTML = "";
        return;

    }

    const respuesta = await fetch(`/aeropuertos?buscar=${texto}`);

    const aeropuertos = await respuesta.json();

    contenedor.innerHTML = "";

    aeropuertos.forEach(aeropuerto=>{

        const opcion = document.createElement("div");

        opcion.className = "item-sugerencia";

        opcion.innerHTML = `
            ✈ ${aeropuerto.ciudad} (${aeropuerto.iata})
            <br>
            <small>${aeropuerto.nombre}</small>
        `;

        opcion.onclick = ()=>{

            input.value = aeropuerto.ciudad;
            input.dataset.iata = aeropuerto.iata;

            contenedor.innerHTML = "";

        };

        contenedor.appendChild(opcion);

    });

}

origenInput.addEventListener("input", ()=>{

    autocompletar(origenInput,sugerenciasOrigen);

});

destinoInput.addEventListener("input", ()=>{

    autocompletar(destinoInput,sugerenciasDestino);

});

async function reservar(offerId) {

    try {

        const respuesta = await fetch(`/oferta/${offerId}`);

        const datos = await respuesta.json();

        if (!datos.ok) {

            alert("⚠️ Esta oferta ya no está disponible.");

            return;
        }

        // La oferta está disponible.
        // Pasamos directamente a los datos del pasajero.

        iniciarDatosPasajero(
            datos.offer_id,
            datos.precio,
            datos.moneda
        );

    } catch (error) {

        console.error(error);

        alert(
            "❌ No fue posible verificar la oferta."
        );

    }

}


function cerrarModal() {

    const modal = document.querySelector(".modal-reserva");

    if (modal) {

        modal.remove();

    }

}


async function continuarReserva(event, offerId) {

    event.preventDefault();

    try {

        const formulario = document.getElementById("formularioPasajero");

        const datosPasajero = {

            nombre: formulario.nombre.value,
            apellido: formulario.apellido.value,
            fecha_nacimiento: formulario.fecha_nacimiento.value,
            genero: formulario.genero.value,
            email: formulario.email.value,
            telefono: formulario.telefono.value,
            nacionalidad: formulario.nacionalidad.value

        };

        const respuesta = await fetch(`/oferta/${offerId}`);

        const datos = await respuesta.json();

        if (!datos.ok) {

            cerrarModal();

            alert("⚠️ Esta oferta ya no está disponible.");

            return;

        }

        const modalAnterior = document.querySelector(".modal-reserva");

        if (modalAnterior) {

            modalAnterior.remove();

        }

        const modal = document.createElement("div");

        modal.className = "modal-reserva";

        modal.innerHTML = `

            <div class="modal-contenido">

                <button
                    class="modal-cerrar"
                    onclick="cerrarModal()">

                    ✕

                </button>


                <div class="modal-icono">

                    ✈️

                </div>


                <h2>

                    Revisar reserva

                </h2>


                <p class="modal-subtitulo">

                    Revisa los datos antes de continuar.

                </p>


                <div class="confirmacion-ruta">

                    <div>

                        <span>Origen</span>

                        <strong>
                            ${datos.origen || "GDL"}
                        </strong>

                    </div>


                    <div class="flecha">

                        →

                    </div>


                    <div>

                        <span>Destino</span>

                        <strong>
                            ${datos.destino || "YUL"}
                        </strong>

                    </div>

                </div>


                <div class="modal-precio">

                    <span>

                        Precio actualizado

                    </span>

                    <strong>

                        $${Number(datos.precio).toLocaleString()}
                        ${datos.moneda}

                    </strong>

                </div>


                <div class="modal-dato">

                    <span>

                        Pasajero

                    </span>

                    <strong>

                        ${datosPasajero.nombre}
                        ${datosPasajero.apellido}

                    </strong>

                </div>


                <div class="modal-dato">

                    <span>

                        Correo

                    </span>

                    <strong>

                        ${datosPasajero.email}

                    </strong>

                </div>


                <div class="modal-dato">

                    <span>

                        Teléfono

                    </span>

                    <strong>

                        ${datosPasajero.telefono}

                    </strong>

                </div>


                <div class="modal-dato">

                    <span>

                        Nacionalidad

                    </span>

                    <strong>

                        ${datosPasajero.nacionalidad}

                    </strong>

                </div>


                <div class="modal-advertencia">

                    ⚠️ El precio y la disponibilidad pueden cambiar
                    antes de completar la compra.

                </div>


                <div class="modal-dato">

                    <span>

                        Offer ID

                    </span>

                    <strong>

                        ${datos.offer_id}

                    </strong>

                </div>


                <button
                    class="modal-continuar"
                    onclick='confirmarReserva(
                        ${JSON.stringify(datos.offer_id)},
                        ${JSON.stringify(datosPasajero)}
                    )'>

                    💳 Continuar con la reserva

                </button>


                <button
                    class="modal-cancelar"
                    onclick="cerrarModal()">

                    Regresar

                </button>

            </div>

        `;

        document.body.appendChild(modal);

    }

    catch (error) {

        console.error(error);

        alert(
            "❌ No fue posible verificar nuevamente la oferta."
        );

    }

}


async function confirmarReserva(offerId, datosPasajero) {

    try {

        const respuesta = await fetch(
            `/reserva/preparar/${offerId}`,
            {
                method: "POST"
            }
        );

        const datos = await respuesta.json();

        if (!datos.ok) {

            cerrarModal();

            alert(
                "⚠️ La oferta ya no está disponible."
            );

            return;

        }

        const modal = document.querySelector(".modal-reserva");

        if (modal) {

            modal.remove();

        }

        const nuevoModal = document.createElement("div");

        nuevoModal.className = "modal-reserva";

        nuevoModal.innerHTML = `

            <div class="modal-contenido">

                <button
                    class="modal-cerrar"
                    onclick="cerrarModal()">

                    ✕

                </button>


                <div class="modal-icono">

                    💳

                </div>


                <h2>

                    Reserva lista

                </h2>


                <p class="modal-subtitulo">

                    La oferta fue verificada correctamente.
                    Revisa los datos antes de crear la reserva.

                </p>


                <div class="modal-precio">

                    <span>

                        Precio actual

                    </span>

                    <strong>

                        $${Number(datos.precio).toLocaleString()}
                        ${datos.moneda}

                    </strong>

                </div>


                <div class="modal-dato">

                    <span>

                        Pasajero

                    </span>

                    <strong>

                        ${datosPasajero.nombre}
                        ${datosPasajero.apellido}

                    </strong>

                </div>


                <div class="modal-dato">

                    <span>

                        Correo

                    </span>

                    <strong>

                        ${datosPasajero.email}

                    </strong>

                </div>


                <div class="modal-dato">

                    <span>

                        Teléfono

                    </span>

                    <strong>

                        ${datosPasajero.telefono}

                    </strong>

                </div>


                <div class="modal-dato">

                    <span>

                        Offer ID

                    </span>

                    <strong>

                        ${datos.offer_id}

                    </strong>

                </div>


                <div class="modal-advertencia">

                    ⚠️ Todavía no se ha creado ninguna reserva.
                    Al continuar se iniciará el proceso de creación
                    de la orden.

                </div>


                <button
                    class="modal-continuar"
                    onclick="crearReservaReal(
                        ${JSON.stringify(datos.offer_id)},
                        ${JSON.stringify(datosPasajero)}
                    )">

                    ✈️ Crear reserva

                </button>


                <button
                    class="modal-cancelar"
                    onclick="cerrarModal()">

                    Cancelar

                </button>

            </div>

        `;

        document.body.appendChild(nuevoModal);

    }

    catch (error) {

        console.error(error);

        alert(
            "❌ No fue posible preparar la reserva."
        );

    }

}

function iniciarDatosPasajero(offerId, precio, moneda) {

    const modalAnterior = document.querySelector(".modal-reserva");

    if (modalAnterior) {
        modalAnterior.remove();
    }

    const nuevoModal = document.createElement("div");

    nuevoModal.className = "modal-reserva";

    nuevoModal.innerHTML = `

        <div class="modal-contenido modal-pasajero">

            <button
                class="modal-cerrar"
                onclick="cerrarModal()">

                ✕

            </button>

            <div class="modal-icono">

                👤

            </div>

            <h2>

                Datos del pasajero

            </h2>

            <p class="modal-subtitulo">

                Ingresa los datos del pasajero principal.

            </p>

            <div class="modal-precio">

                <span>
                    Precio actual
                </span>

                <strong>
                    $${Number(precio).toLocaleString()} ${moneda}
                </strong>

            </div>

            <form
                id="formularioPasajero"
                onsubmit="continuarReserva(event, '${offerId}')">

                <div class="campo">

                    <label for="nombre">
                        Nombre
                    </label>

                    <input
                        type="text"
                        id="nombre"
                        name="nombre"
                        placeholder="Ej. Armando"
                        required
                    >

                </div>

                <div class="campo">

                    <label for="apellido">
                        Apellidos
                    </label>

                    <input
                        type="text"
                        id="apellido"
                        name="apellido"
                        placeholder="Ej. Valenzuela Rivera"
                        required
                    >

                </div>

                <div class="campo">

                    <label for="fecha_nacimiento">
                        Fecha de nacimiento
                    </label>

                    <input
                        type="date"
                        id="fecha_nacimiento"
                        name="fecha_nacimiento"
                        max="2008-12-31"
                        required
                    >

                </div>

                <div class="campo">

                    <label for="genero">
                        Género
                    </label>

                    <select
                        id="genero"
                        name="genero"
                        required>

                        <option value="">
                            Seleccionar
                        </option>

                        <option value="m">
                            Masculino
                        </option>

                        <option value="f">
                            Femenino
                        </option>

                    </select>

                </div>

                <div class="campo">

                    <label for="email">
                        Correo electrónico
                    </label>

                    <input
                        type="email"
                        id="email"
                        name="email"
                        placeholder="correo@ejemplo.com"
                        required
                    >

                </div>

                <div class="campo">

                    <label for="telefono">
                        Teléfono
                    </label>

                    <input
                        type="tel"
                        id="telefono"
                        name="telefono"
                        placeholder="+52 123 456 7890"
                        required
                    >

                </div>

                <div class="campo">

                    <label for="nacionalidad">
                        Nacionalidad
                    </label>

                    <input
                        type="text"
                        id="nacionalidad"
                        name="nacionalidad"
                        placeholder="Ej. Mexicana"
                        value="Mexicana"
                        required
                    >

                </div>

                <div class="modal-advertencia">

                    🔒 Tus datos se utilizarán únicamente
                    para preparar la reserva del vuelo.

                </div>

                <button
                    type="submit"
                    class="modal-continuar">

                    Continuar →

                </button>

                <button
                    type="button"
                    class="modal-cancelar"
                    onclick="cerrarModal()">

                    Cancelar

                </button>

            </form>

        </div>

    `;

    document.body.appendChild(nuevoModal);

}


function continuarReserva(event, offerId) {

    event.preventDefault();

    const datos = {

        offer_id: offerId,

        nombre:
            document.getElementById("nombre").value,

        apellido:
            document.getElementById("apellido").value,

        fecha_nacimiento:
            document.getElementById("fecha_nacimiento").value,

        genero:
            document.getElementById("genero").value,

        email:
            document.getElementById("email").value,

        telefono:
            document.getElementById("telefono").value,

        nacionalidad:
            document.getElementById("nacionalidad").value

    };

    console.log("Datos del pasajero:");

    console.log(datos);

    crearReservaReal(
        datos.offer_id,
        datos
    );

}

async function crearReservaReal(offerId, pasajero) {

    try {

        const respuesta = await fetch(

            `/reserva/crear/${offerId}`,

            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(pasajero)
            }

        );

        const datos = await respuesta.json();

        if (!datos.ok) {

            alert(
                "❌ No fue posible crear la reserva."
            );

            return;

        }

        cerrarModal();

        alert(

`✅ Reserva creada

✈️ Vuelo: ${datos.vuelo || "Sin información"}

👤 Pasajero: ${datos.pasajero || "Sin información"}

💰 Precio: $${datos.precio || "?"} ${datos.moneda || ""}

🎫 Referencia: ${datos.referencia || "Pendiente"}

📋 Order ID: ${datos.order_id || "Sin información"}

Estado: ${datos.estado || "Sin información"}`

        );

    }

    catch (error) {

        console.error(error);

        alert(
            "❌ Ocurrió un error al crear la reserva."
        );

    }

}