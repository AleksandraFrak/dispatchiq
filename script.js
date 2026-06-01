const hamburger = document.querySelector('.hamburger');
const navList = document.querySelector('.nav-list');
const incidentsList = document.querySelector('#incidents-list');
const incidentsSummary = document.querySelector('#incidents-summary');
const refreshIncidents = document.querySelector('#refresh-incidents');
const incidentForm = document.querySelector('#incident-form');
const incidentMessage = document.querySelector('#incident-message');
const saveIncidentButton = document.querySelector('#save-incident');
const cancelEditButton = document.querySelector('#cancel-edit');
const incidentIdInput = document.querySelector('#incident-id');

hamburger.addEventListener('click', () => {
  const isOpen = navList.classList.toggle('active');
  hamburger.setAttribute('aria-expanded', isOpen);
});

const navLinks = document.querySelectorAll('.nav-list a');

navLinks.forEach((link) => {
  link.addEventListener('click', () => {
    navList.classList.remove('active');
    hamburger.setAttribute('aria-expanded', 'false');
  });
});

const priorityClassMap = {
  Krytyczny: 'critical',
  Wysoki: 'high',
  Średni: 'medium',
  Niski: 'low',
};

let incidentsCache = [];

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function createIncidentCard(incident) {
  const priorityClass = priorityClassMap[incident.priority] || 'low';

  return `
    <article class="incident-card" data-id="${incident.id}">
      <div class="incident-card__top">
        <span class="incident-code">${escapeHtml(incident.code)}</span>
        <span class="priority priority--${priorityClass}">${escapeHtml(incident.priority)}</span>
      </div>
      <h3>${escapeHtml(incident.title)}</h3>
      <dl class="incident-details">
        <div>
          <dt>Dzielnica</dt>
          <dd>${escapeHtml(incident.district)}</dd>
        </div>
        <div>
          <dt>Jednostka</dt>
          <dd>${escapeHtml(incident.unit)}</dd>
        </div>
        <div>
          <dt>Status</dt>
          <dd>${escapeHtml(incident.status)}</dd>
        </div>
        <div>
          <dt>ETA</dt>
          <dd>${incident.eta_minutes === 0 ? 'na miejscu' : `${incident.eta_minutes} min`}</dd>
        </div>
      </dl>
      <div class="incident-actions">
        <button class="refresh-btn" type="button" data-action="edit" data-id="${incident.id}">Edytuj</button>
        <button class="delete-btn" type="button" data-action="delete" data-id="${incident.id}">Usuń</button>
      </div>
    </article>
  `;
}

function getIncidentFormData() {
  const formData = new FormData(incidentForm);

  return {
    code: formData.get('code').trim(),
    title: formData.get('title').trim(),
    priority: formData.get('priority'),
    district: formData.get('district').trim(),
    unit: formData.get('unit').trim(),
    status: formData.get('status'),
    eta_minutes: Number(formData.get('eta_minutes')),
  };
}

function setMessage(message, type = 'neutral') {
  if (!incidentMessage) {
    return;
  }

  incidentMessage.textContent = message;
  incidentMessage.dataset.type = type;
}

function resetIncidentForm() {
  incidentForm?.reset();
  if (incidentIdInput) {
    incidentIdInput.value = '';
  }
  if (saveIncidentButton) {
    saveIncidentButton.textContent = 'Dodaj zgłoszenie';
  }
  if (cancelEditButton) {
    cancelEditButton.hidden = true;
  }
}

function fillIncidentForm(incident) {
  incidentIdInput.value = incident.id;
  incidentForm.elements.code.value = incident.code;
  incidentForm.elements.title.value = incident.title;
  incidentForm.elements.priority.value = incident.priority;
  incidentForm.elements.district.value = incident.district;
  incidentForm.elements.unit.value = incident.unit;
  incidentForm.elements.status.value = incident.status;
  incidentForm.elements.eta_minutes.value = incident.eta_minutes;
  saveIncidentButton.textContent = 'Zapisz zmiany';
  cancelEditButton.hidden = false;
  setMessage(`Edytujesz zgłoszenie ${incident.code}.`, 'neutral');
  incidentForm.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });
  const data = await response.json();

  if (!response.ok) {
    const message = data.error || data.errors?.join(' ') || 'Operacja nie powiodła się.';
    throw new Error(message);
  }

  return data;
}

async function loadIncidents() {
  if (!incidentsList || !incidentsSummary) {
    return;
  }

  incidentsSummary.textContent = 'Ładowanie zgłoszeń...';
  incidentsList.innerHTML = '';

  try {
    const incidents = await requestJson('/api/incidents');
    incidentsCache = incidents;
    incidentsList.innerHTML = incidents.map(createIncidentCard).join('');
    incidentsSummary.textContent = `Pobrano ${incidents.length} zgłoszeń z bazy danych.`;
  } catch (error) {
    incidentsSummary.textContent = 'Uruchom backend, aby pobrać zgłoszenia z bazy danych.';
    incidentsList.innerHTML = `
      <article class="incident-card incident-card--error">
        <h3>Brak połączenia z API</h3>
        <p>${error.message}</p>
      </article>
    `;
  }
}

async function saveIncident(event) {
  event.preventDefault();
  const incidentId = incidentIdInput.value;
  const payload = getIncidentFormData();
  const url = incidentId ? `/api/incidents/${incidentId}` : '/api/incidents';
  const method = incidentId ? 'PUT' : 'POST';

  try {
    await requestJson(url, {
      method,
      body: JSON.stringify(payload),
    });
    setMessage(incidentId ? 'Zgłoszenie zostało zaktualizowane.' : 'Zgłoszenie zostało dodane.', 'success');
    resetIncidentForm();
    await loadIncidents();
  } catch (error) {
    setMessage(error.message, 'error');
  }
}

async function handleIncidentAction(event) {
  const button = event.target.closest('button[data-action]');
  if (!button) {
    return;
  }

  const incidentId = Number(button.dataset.id);
  const incident = incidentsCache.find((item) => item.id === incidentId);

  if (button.dataset.action === 'edit' && incident) {
    fillIncidentForm(incident);
    return;
  }

  if (button.dataset.action === 'delete') {
    const confirmed = window.confirm(`Usunąć zgłoszenie ${incident?.code || incidentId}?`);
    if (!confirmed) {
      return;
    }

    try {
      await requestJson(`/api/incidents/${incidentId}`, { method: 'DELETE' });
      setMessage('Zgłoszenie zostało usunięte.', 'success');
      await loadIncidents();
    } catch (error) {
      setMessage(error.message, 'error');
    }
  }
}

refreshIncidents?.addEventListener('click', loadIncidents);
incidentForm?.addEventListener('submit', saveIncident);
cancelEditButton?.addEventListener('click', () => {
  resetIncidentForm();
  setMessage('Edycja została anulowana.', 'neutral');
});
incidentsList?.addEventListener('click', handleIncidentAction);
loadIncidents();
