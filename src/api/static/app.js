 // CLIENT-SIDE CACHE
 const flags = [];

 // UTILS
 function showToast(message, type = "success") {
     const toastId = `toast-${Date.now()}`;
     const toastHTML = `
      <div id="${toastId}" class="toast align-items-center text-bg-${type} border-0 mb-2" role="alert">
        <div class="d-flex">
          <div class="toast-body">${message}</div>
          <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
      </div>`;
     document.getElementById('toastContainer').insertAdjacentHTML('beforeend', toastHTML);
     const el = document.getElementById(toastId);
     new bootstrap.Toast(el, {
         delay: 2500
     }).show();
     el.addEventListener('hidden.bs.toast', () => el.remove());
 }

 function formatDateDDMMYYYY(d) {
     if (!d) return '';
     const dt = new Date(d);
     const dd = String(dt.getDate()).padStart(2, '0');
     const mm = String(dt.getMonth() + 1).padStart(2, '0');
     const yyyy = dt.getFullYear();
     return `${dd}/${mm}/${yyyy}`;
 }

 async function fetchFlags() {
     try {
         const res = await fetch('/flags', {
             method: 'GET',
             headers: {
                 'Accept': 'application/json'
             },
             credentials: 'same-origin'
         });
         if (!res.ok) {
             const txt = await res.text().catch(() => '');
             console.error('fetchFlags failed', res.status, res.statusText, txt);
             showToast('Failed to load flags', 'danger');
             return;
         }
         const data = await res.json();
         flags.length = 0;
         if (Array.isArray(data)) flags.push(...data);
         renderFlags();
     } catch (err) {
         console.error(err);
         showToast('Error fetching flags', 'danger');
     }
 }

 async function createFlagAPI(payload) {
     try {
         const res = await fetch('/flags', {
             method: 'POST',
             headers: {
                 'Content-Type': 'application/json'
             },
             credentials: 'same-origin',
             body: JSON.stringify(payload),
         });
         if (!res.ok) {
             const body = await res.text().catch(() => '');
             showToast(`Create failed: ${res.status}`, 'danger');
             console.error('createFlag failed', res.status, res.statusText, body);
             return false;
         }
         showToast(`Flag "${payload.name}" created`, 'primary');
         bootstrap.Collapse.getOrCreateInstance(document.getElementById('collapseCreate')).hide();
         await fetchFlags();
         return true;
     } catch (err) {
         console.error(err);
         showToast('Error creating flag', 'danger');
         return false;
     }
 }

 async function patchFlagAPI(id, updates) {
     try {
         const res = await fetch(`/flags/${encodeURIComponent(id)}`, {
             method: 'PATCH',
             headers: {
                 'Content-Type': 'application/json'
             },
             credentials: 'same-origin',
             body: JSON.stringify(updates),
         });
         if (!res.ok) {
             const body = await res.text().catch(() => '');
             console.error('patchFlag failed', res.status, res.statusText, body);
             showToast('Update failed', 'danger');
             return false;
         }
         showToast('Flag updated', 'info');
         await fetchFlags();
         return true;
     } catch (err) {
         console.error(err);
         showToast('Error updating flag', 'danger');
         return false;
     }
 }

 async function deleteFlagAPI(id) {
     try {
         const res = await fetch(`/flags/${encodeURIComponent(id)}`, {
             method: 'DELETE',
             credentials: 'same-origin',
         });
         if (!res.ok) {
             const body = await res.text().catch(() => '');
             console.error('deleteFlag failed', res.status, res.statusText, body);
             showToast('Delete failed', 'danger');
             return false;
         }
         showToast('Flag deleted', 'warning');
         await fetchFlags();
         return true;
     } catch (err) {
         console.error(err);
         showToast('Error deleting flag', 'danger');
         return false;
     }
 }

 async function toggleFlagAPI(name, id, value) {
     try {
         const res = await fetch(`/flags/${encodeURIComponent(id)}`, {
             method: 'PATCH',
             headers: {
                 'Content-Type': 'application/json'
             },
             credentials: 'same-origin',
             body: JSON.stringify({
                 value
             }),
         });
         if (!res.ok) {
             const body = await res.text().catch(() => '');
             console.error('toggleFlag failed', res.status, res.statusText, body);
             showToast('Toggle failed', 'danger');
             await fetchFlags();
             return false;
         }
         showToast(`Flag ${name} ${value ? 'ON' : 'OFF'}`, value ? 'success' : 'danger');
         await fetchFlags();
         return true;
     } catch (err) {
         console.error(err);
         showToast(`Error toggling flag ${name}`, 'danger');
         return false;
     }
 }

 // Helper for filter value
 function getFilterValue() {
     const activeBtn = document.querySelector('.btn-retro-filter.active');
     return activeBtn ? activeBtn.getAttribute('data-value') : 'all';
 }

 // RENDERING all flags based on current filters
 function renderFlags() {
     const flagsContainer = document.getElementById('flagsContainer');
     flagsContainer.innerHTML = '';
     const now = new Date();
     const filterName = (document.getElementById('filterName').value || '').toLowerCase();
     const filterValue = getFilterValue();

     const visible = flags
         .filter(f => (f.name || '').toLowerCase().includes(filterName))
         .filter(f => {
             if (filterValue === 'all') return true;
             if (filterValue === 'expired') return Boolean(f.expired);
             if (filterValue === 'true' || filterValue === 'false') {
                 return String(Boolean(f.value)) === filterValue;
             }
             return true;
         })
         .sort((a, b) => (a.name || '').localeCompare(b.name || ''));



     visible.forEach(flag => {
         let expiryText = 'No expiration';
         let expireBadgeHTML = '';
         let isExpired = flag.expired;
         if (flag.expired) {
             const expDate = new Date(flag.expiration_date);
             if (isNaN(expDate.getTime())) {
                 expiryText = 'Invalid date';
             } else {
                 const diffMs = expDate - now;
                 const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24));
                 expiryText = formatDateDDMMYYYY(expDate);
                 if (diffMs < 0) {
                     isExpired = true;
                     expireBadgeHTML = `<span class="badge bg-danger ms-2">Expired</span>`;
                     expiryText = `Expired on ${formatDateDDMMYYYY(expDate)}`;
                 } else if (diffDays <= 7) {
                     expireBadgeHTML = `<span class="badge bg-warning text-dark ms-2">⚠ Expires in ${diffDays} day${diffDays > 1 ? 's' : ''}</span>`;
                 }
             }
         }

         const cardCol = document.createElement('div');
         cardCol.innerHTML = `
  <div class="card flag-card ${flag.value ? 'flag-on' : 'flag-off'}">
    <div class="card-body">
      <div class="flag-header d-flex align-items-center justify-content-between">
        <h5 class="card-title mb-0">${escapeHtml(flag.name)}</h5>
        <span class="retro-switch ${flag.value ? 'on' : 'off'}" title="Toggle flag">
          <i class="bi ${flag.value ? 'bi-toggle-on' : 'bi-toggle-off'}"></i>
        </span>
      </div>
      <p class="card-text mt-2">${escapeHtml(flag.desc)}</p>
      <p><strong>Status:</strong> ${flag.value ? 'ON' : 'OFF'}</p>
      <p class="text-muted mb-1">Created: ${flag.date_created ? formatDateDDMMYYYY(flag.date_created) : ''}</p>
      <p class="text-muted mb-1">Updated: ${flag.date_updated ? formatDateDDMMYYYY(flag.date_updated) : ''}</p>
      <p class="text-muted mb-1">Expiry: ${flag.expiration_date ? formatDateDDMMYYYY(flag.expiration_date) : ''}</p>
      <div class="flag-footer d-flex align-items-center">
      ${expireBadgeHTML}
        <button class="btn btn-sm btn-warning update-btn"><i class="bi bi-pencil-square"></i></button>
        <button class="btn btn-sm btn-outline-danger delete-btn"><i class="bi bi-trash"></i></button>
        
      </div>
    </div>
  </div>`;

         cardCol.className = 'col-md-4';

         flagsContainer.appendChild(cardCol);

         // Retro switch handler
         const switchEl = cardCol.querySelector('.retro-switch');
         switchEl.addEventListener('click', async () => {

             await toggleFlagAPI(flag.name, flag.id, !flag.value);
             renderFlags();
         });

         cardCol.querySelector('.delete-btn').addEventListener('click', async () => {
             if (!confirm(`Delete flag "${flag.name}"?`)) return;
             await deleteFlagAPI(flag.id);
         });

         cardCol.querySelector('.update-btn').addEventListener('click', () => {
             document.getElementById('updateId').value = flag.id;
             document.getElementById('updateDesc').value = flag.desc || '';
             document.getElementById('updateValue').value = flag.value ? 'true' : 'false';
             document.getElementById('updateExpiry').value = flag.expiration_date ? (new Date(flag.expiration_date)).toISOString().split('T')[0] : '';
             new bootstrap.Modal(document.getElementById('updateModal')).show();
         });
     });

     if (visible.length === 0) {
         flagsContainer.innerHTML = '<div class="col-12"><div class="alert alert-secondary">No flags found.</div></div>';
     }
 }

 function escapeHtml(str) {
     return String(str)
         .replaceAll('&', '&amp;')
         .replaceAll('<', '&lt;')
         .replaceAll('>', '&gt;')
         .replaceAll('"', '&quot;')
         .replaceAll("'", '&#39;');
 }

 document.getElementById('createFlagForm').addEventListener('submit', async (e) => {
     e.preventDefault();
     const name = document.getElementById('flagName').value.trim();
     if (!name) {
         showToast('Flag name is required', 'danger');
         return;
     }
     const payload = {
         name,
         desc: document.getElementById('flagDesc').value.trim() || null,
         value: document.getElementById('flagValue').value === 'true',
         // expiration_date: document.getElementById('flagExpiry').value || null,
     };
     const ok = await createFlagAPI(payload);
     if (ok) {
         e.target.reset();
         // document.getElementById('flagExpiry').value = '';
     }
 });

 document.getElementById('updateFlagForm').addEventListener('submit', async (e) => {
     e.preventDefault();
     const id = document.getElementById('updateId').value;
     if (!id) {
         showToast('Invalid flag id', 'danger');
         return;
     }
     const updates = {
         desc: document.getElementById('updateDesc').value || null,
         value: document.getElementById('updateValue').value === 'true',
         expiration_date: document.getElementById('updateExpiry').value || null,
     };
     const ok = await patchFlagAPI(id, updates);
     if (ok) {
         bootstrap.Modal.getInstance(document.getElementById('updateModal')).hide();
     }
 });

 // Filters wiring (real-time)
 document.getElementById('filterName').addEventListener('input', debounce(renderFlags, 150));
 // Removed filterValue select event listener

 function debounce(fn, wait) {
     let t;
     return function(...args) {
         clearTimeout(t);
         t = setTimeout(() => fn.apply(this, args), wait);
     };
 }

 document.querySelectorAll('.btn-retro-filter').forEach(btn => {
     btn.addEventListener('click', function() {
         document.querySelectorAll('.btn-retro-filter').forEach(b => b.classList.remove('active'));
         btn.classList.add('active');
         renderFlags();
     });
 });

 document.addEventListener('DOMContentLoaded', () => {
     document.querySelector('.btn-retro-filter[data-value="all"]').classList.add('active');
     fetchFlags();
 });