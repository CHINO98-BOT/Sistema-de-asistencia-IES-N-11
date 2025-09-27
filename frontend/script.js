const API_BASE = 'http://127.0.0.1:5000/api';

// Función genérica para cargar estudiantes en selects/tablas
async function cargarEstudiantes() {
    const response = await fetch(`${API_BASE}/estudiantes`);
    const estudiantes = await response.json();
    const select = document.getElementById('estudiante-select');
    const tbody = document.querySelector('#tabla-estudiantes tbody') || document.querySelector('#reportes-tbody');
    if (select) {
        select.innerHTML = '<option value="">Selecciona...</option>' + estudiantes.map(e => `<option value="${e.id}">${e.nombre}</option>`).join('');
    }
    if (tbody) {
        tbody.innerHTML = estudiantes.map(e => `<tr><td>${e.id}</td><td>${e.nombre}</td><td>${e.email || ''}</td><td><button onclick="eliminarEst(${e.id})">Eliminar</button></td></tr>`).join('');
    }
}

// Agregar estudiante
document.getElementById('form-estudiante')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        nombre: document.getElementById('nombre').value,
        email: document.getElementById('email').value
    };
    if (!data.nombre) return alert('Nombre requerido');
    await fetch(`${API_BASE}/estudiantes`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
    alert('Estudiante agregado');
    cargarEstudiantes();