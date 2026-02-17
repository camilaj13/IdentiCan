// IdentiCan Admin Web App
(function () {
  'use strict';

  const API_BASE = window.location.origin;
  let token = localStorage.getItem('identican_admin_token');
  let currentUser = null;
  let usersData = [];
  let statsData = null;

  // ── Helpers ──────────────────────────────────────────────

  async function api(path, options = {}) {
    const headers = { 'Content-Type': 'application/json', ...options.headers };
    if (token) headers['Authorization'] = 'Bearer ' + token;
    const res = await fetch(API_BASE + path, { ...options, headers });
    if (res.status === 401) {
      logout();
      throw new Error('Session expired');
    }
    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail || 'Request failed');
    }
    return res.json();
  }

  function $(sel) { return document.querySelector(sel); }
  function $$(sel) { return document.querySelectorAll(sel); }

  function formatDate(iso) {
    if (!iso) return '—';
    const d = new Date(iso);
    return d.toLocaleDateString('en-US', {
      year: 'numeric', month: 'short', day: 'numeric',
    });
  }

  function formatDateTime(iso) {
    if (!iso) return '—';
    const d = new Date(iso);
    return d.toLocaleDateString('en-US', {
      year: 'numeric', month: 'short', day: 'numeric',
      hour: '2-digit', minute: '2-digit',
    });
  }

  function escapeHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // ── Login ────────────────────────────────────────────────

  function showLogin() {
    $('#login-screen').style.display = 'flex';
    $('#app-screen').style.display = 'none';
  }

  function showApp() {
    $('#login-screen').style.display = 'none';
    $('#app-screen').style.display = 'flex';
  }

  async function handleLogin(e) {
    e.preventDefault();
    const email = $('#login-email').value.trim();
    const password = $('#login-password').value;
    const errEl = $('#login-error');
    errEl.style.display = 'none';

    if (!email || !password) {
      errEl.textContent = 'Please enter email and password.';
      errEl.style.display = 'block';
      return;
    }

    try {
      const data = await api('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });

      if (data.user.role !== 'admin') {
        errEl.textContent = 'Access denied. Admin account required.';
        errEl.style.display = 'block';
        return;
      }

      token = data.access_token;
      currentUser = data.user;
      localStorage.setItem('identican_admin_token', token);
      showApp();
      initApp();
    } catch (err) {
      errEl.textContent = err.message || 'Invalid credentials.';
      errEl.style.display = 'block';
    }
  }

  function logout() {
    token = null;
    currentUser = null;
    localStorage.removeItem('identican_admin_token');
    showLogin();
    $('#login-password').value = '';
  }

  // ── App Init ─────────────────────────────────────────────

  async function initApp() {
    if (currentUser) {
      $('#admin-display-name').textContent = currentUser.name;
    } else {
      try {
        currentUser = await api('/api/auth/me');
        $('#admin-display-name').textContent = currentUser.name;
        if (currentUser.role !== 'admin') {
          logout();
          return;
        }
      } catch {
        logout();
        return;
      }
    }

    navigateTo('dashboard');
  }

  // ── Navigation ───────────────────────────────────────────

  function navigateTo(page) {
    $$('.page-section').forEach(s => s.classList.remove('active'));
    $$('.nav-item').forEach(n => n.classList.remove('active'));

    const section = $(`#page-${page}`);
    const navItem = $(`.nav-item[data-page="${page}"]`);
    if (section) section.classList.add('active');
    if (navItem) navItem.classList.add('active');

    if (page === 'dashboard') loadDashboard();
    else if (page === 'users') loadUsers();
  }

  // ── Dashboard ────────────────────────────────────────────

  async function loadDashboard() {
    $('#dashboard-content').innerHTML = '<div class="loading"><div class="spinner"></div></div>';

    try {
      statsData = await api('/api/admin/stats');
      renderDashboard();
    } catch (err) {
      $('#dashboard-content').innerHTML = `<div class="empty-state"><div class="icon">!</div><p>Error loading stats: ${escapeHtml(err.message)}</p></div>`;
    }
  }

  function renderDashboard() {
    const s = statsData;
    $('#dashboard-content').innerHTML = `
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">&#128100;</div>
          <div class="stat-value">${s.total_users}</div>
          <div class="stat-label">Total Users</div>
        </div>
        <div class="stat-card success">
          <div class="stat-icon">&#128054;</div>
          <div class="stat-value">${s.total_dogs}</div>
          <div class="stat-label">Registered Dogs</div>
        </div>
        <div class="stat-card warning">
          <div class="stat-icon">&#11088;</div>
          <div class="stat-value">${s.premium_users}</div>
          <div class="stat-label">Premium Users</div>
        </div>
        <div class="stat-card info">
          <div class="stat-icon">&#128269;</div>
          <div class="stat-value">${s.total_verifications}</div>
          <div class="stat-label">Total Verifications</div>
        </div>
      </div>

      <div class="stats-grid">
        <div class="stat-card success">
          <div class="stat-icon">&#9989;</div>
          <div class="stat-value">${s.successful_verifications}</div>
          <div class="stat-label">Successful Matches</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">&#128200;</div>
          <div class="stat-value">${s.success_rate}%</div>
          <div class="stat-label">Success Rate</div>
        </div>
      </div>
    `;
  }

  // ── Users ────────────────────────────────────────────────

  async function loadUsers() {
    $('#users-table-body').innerHTML = '<tr><td colspan="6"><div class="loading"><div class="spinner"></div></div></td></tr>';

    try {
      usersData = await api('/api/admin/users-detail');
      renderUsers(usersData);
    } catch (err) {
      $('#users-table-body').innerHTML = `<tr><td colspan="6"><div class="empty-state"><p>Error: ${escapeHtml(err.message)}</p></div></td></tr>`;
    }
  }

  function renderUsers(users) {
    const tbody = $('#users-table-body');

    if (!users.length) {
      tbody.innerHTML = '<tr><td colspan="6"><div class="empty-state"><div class="icon">&#128100;</div><p>No users found</p></div></td></tr>';
      return;
    }

    tbody.innerHTML = users.map(u => {
      const roleBadge = u.role === 'admin'
        ? '<span class="badge badge-admin">Admin</span>'
        : '<span class="badge badge-user">User</span>';

      const premiumBadge = u.is_premium
        ? '<span class="badge badge-premium">Premium</span>'
        : '<span class="badge badge-free">Free</span>';

      const dogsHtml = u.dogs.length
        ? '<div class="dogs-list">' + u.dogs.map(d =>
            `<span class="dog-chip" data-dog-id="${d.id}" data-user-id="${u.id}" title="View ${escapeHtml(d.name)}">&#128054; ${escapeHtml(d.name)}</span>`
          ).join('') + '</div>'
        : '<span class="no-dogs">No dogs registered</span>';

      return `<tr>
        <td><strong>${escapeHtml(u.name)}</strong></td>
        <td>${escapeHtml(u.email)}</td>
        <td>${formatDate(u.created_at)}</td>
        <td>${roleBadge} ${premiumBadge}</td>
        <td>${dogsHtml}</td>
        <td>
          ${u.role !== 'admin' ? `<button class="btn-toggle-premium" data-user-id="${u.id}" title="Toggle premium">${u.is_premium ? 'Remove Premium' : 'Grant Premium'}</button>` : ''}
        </td>
      </tr>`;
    }).join('');

    // Attach dog chip click handlers
    tbody.querySelectorAll('.dog-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        const userId = parseInt(chip.dataset.userId);
        const dogId = parseInt(chip.dataset.dogId);
        const user = usersData.find(u => u.id === userId);
        const dog = user ? user.dogs.find(d => d.id === dogId) : null;
        if (dog) showDogModal(dog, user);
      });
    });

    // Attach premium toggle handlers
    tbody.querySelectorAll('.btn-toggle-premium').forEach(btn => {
      btn.addEventListener('click', async () => {
        const userId = parseInt(btn.dataset.userId);
        try {
          await api(`/api/admin/users/${userId}/premium`, { method: 'POST' });
          loadUsers();
        } catch (err) {
          alert('Error: ' + err.message);
        }
      });
    });
  }

  function filterUsers() {
    const query = $('#user-search').value.toLowerCase().trim();
    if (!query) {
      renderUsers(usersData);
      return;
    }
    const filtered = usersData.filter(u =>
      u.name.toLowerCase().includes(query) ||
      u.email.toLowerCase().includes(query) ||
      u.dogs.some(d => d.name.toLowerCase().includes(query))
    );
    renderUsers(filtered);
  }

  // ── Dog Modal ────────────────────────────────────────────

  function showDogModal(dog, owner) {
    const sexLabel = dog.sex === 'M' ? 'Male' : 'Female';
    const originLabel = dog.origin.charAt(0).toUpperCase() + dog.origin.slice(1);

    $('#modal-dog-title').textContent = dog.name;
    $('#modal-dog-body').innerHTML = `
      <div class="detail-grid">
        <div class="detail-item">
          <label>Owner</label>
          <span>${escapeHtml(owner.name)}</span>
        </div>
        <div class="detail-item">
          <label>Owner Email</label>
          <span>${escapeHtml(owner.email)}</span>
        </div>
        <div class="detail-item">
          <label>Breed</label>
          <span>${escapeHtml(dog.breed) || '—'}</span>
        </div>
        <div class="detail-item">
          <label>Sex</label>
          <span>${sexLabel}</span>
        </div>
        <div class="detail-item">
          <label>Age</label>
          <span>${dog.age_years != null ? dog.age_years + ' years' : '—'}</span>
        </div>
        <div class="detail-item">
          <label>Weight</label>
          <span>${dog.weight_kg != null ? dog.weight_kg + ' kg' : '—'}</span>
        </div>
        <div class="detail-item">
          <label>Color</label>
          <span>${escapeHtml(dog.color) || '—'}</span>
        </div>
        <div class="detail-item">
          <label>Origin</label>
          <span>${originLabel}</span>
        </div>
        <div class="detail-item">
          <label>QR Code</label>
          <span style="font-family:monospace">${escapeHtml(dog.qr_code)}</span>
        </div>
        <div class="detail-item">
          <label>Microchip ID</label>
          <span>${escapeHtml(dog.microchip_id) || '—'}</span>
        </div>
        <div class="detail-item">
          <label>Registered</label>
          <span>${formatDateTime(dog.created_at)}</span>
        </div>
        <div class="detail-item">
          <label>Last Updated</label>
          <span>${formatDateTime(dog.updated_at)}</span>
        </div>
        ${dog.from_shelter ? `
        <div class="detail-item">
          <label>Shelter</label>
          <span>${escapeHtml(dog.shelter_name) || 'Yes (unnamed)'}</span>
        </div>` : ''}
        ${dog.behavior_notes ? `
        <div class="detail-item full">
          <label>Behavior Notes</label>
          <span>${escapeHtml(dog.behavior_notes)}</span>
        </div>` : ''}
        ${dog.likes ? `
        <div class="detail-item full">
          <label>Likes</label>
          <span>${escapeHtml(dog.likes)}</span>
        </div>` : ''}
        ${dog.allergies ? `
        <div class="detail-item full">
          <label>Allergies</label>
          <span>${escapeHtml(dog.allergies)}</span>
        </div>` : ''}
      </div>
      <div style="margin-top:16px; font-size:12px; color:var(--text-secondary);">
        Nose images: ${dog.nose_images && dog.nose_images.length ? dog.nose_images.length + ' uploaded' : 'None'}
      </div>
    `;

    $('#dog-modal').classList.add('active');
  }

  function closeDogModal() {
    $('#dog-modal').classList.remove('active');
  }

  // ── Boot ─────────────────────────────────────────────────

  document.addEventListener('DOMContentLoaded', () => {
    // Login form
    $('#login-form').addEventListener('submit', handleLogin);

    // Logout
    $('#btn-logout').addEventListener('click', logout);

    // Navigation
    $$('.nav-item').forEach(item => {
      item.addEventListener('click', () => navigateTo(item.dataset.page));
    });

    // Search
    $('#user-search').addEventListener('input', filterUsers);

    // Modal close
    $('#modal-close-btn').addEventListener('click', closeDogModal);
    $('#dog-modal').addEventListener('click', (e) => {
      if (e.target === $('#dog-modal')) closeDogModal();
    });

    // Check existing token
    if (token) {
      showApp();
      initApp();
    } else {
      showLogin();
    }
  });
})();
