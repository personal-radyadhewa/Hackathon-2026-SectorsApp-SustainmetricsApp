/** API client for SustainMetric IDX Harness backend */

const BASE_URL = '/api/v1';

export async function fetchAudits() {
  const res = await fetch(`${BASE_URL}/audits`);
  if (!res.ok) throw new Error('Failed to fetch audits');
  return res.json();
}

export async function triggerAudit(tickers) {
  const res = await fetch(`${BASE_URL}/audits/trigger`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ tickers }),
  });
  if (!res.ok) throw new Error('Failed to trigger audit');
  return res.json();
}

export async function fetchAuditDetail(auditId) {
  const res = await fetch(`${BASE_URL}/audits/${auditId}`);
  if (!res.ok) throw new Error('Failed to fetch audit detail');
  return res.json();
}

export async function fetchTKBIEntries(auditId) {
  const res = await fetch(`${BASE_URL}/audits/${auditId}/tkbi`);
  if (!res.ok) throw new Error('Failed to fetch TKBI entries');
  return res.json();
}

export async function updateHITLEntry(auditId, entryId, auditorFeedback, auditorOverride) {
  const res = await fetch(`${BASE_URL}/audits/${auditId}/tkbi/${entryId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      auditor_feedback: auditorFeedback,
      auditor_override: auditorOverride,
    }),
  });
  if (!res.ok) throw new Error('Failed to update TKBI entry');
  return res.json();
}

export async function fetchAuditTraces(auditId) {
  const res = await fetch(`${BASE_URL}/audits/${auditId}/traces`);
  if (!res.ok) throw new Error('Failed to fetch traces');
  return res.json();
}

export async function fetchBenchmarks() {
  const res = await fetch(`${BASE_URL}/benchmarks`);
  if (!res.ok) throw new Error('Failed to fetch benchmarks');
  return res.json();
}

export async function fetchSchedules() {
  const res = await fetch(`${BASE_URL}/schedules`);
  if (!res.ok) throw new Error('Failed to fetch schedules');
  return res.json();
}

export async function createSchedule(data) {
  const res = await fetch(`${BASE_URL}/schedules`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to create schedule');
  return res.json();
}

export async function deleteSchedule(scheduleId) {
  const res = await fetch(`${BASE_URL}/schedules/${scheduleId}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error('Failed to delete schedule');
  return res.json();
}

export function getExportXLSXUrl(auditId) {
  return `${BASE_URL}/audits/${auditId}/export/xlsx`;
}

export function getExportPDFUrl(auditId) {
  return `${BASE_URL}/audits/${auditId}/export/pdf`;
}
