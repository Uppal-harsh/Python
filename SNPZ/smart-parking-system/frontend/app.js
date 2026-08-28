/**
 * ═══════════════════════════════════════════════════════════
 *  SENTINEL — No-Parking Zone Detection System
 *  Frontend Application Logic
 *  Includes: Webcam, YOLO plate scanning, polling, modals
 * ═══════════════════════════════════════════════════════════
 */

const API_BASE = "";
const POLL_INTERVAL = 5000; // 5 seconds

// ── State ──
let isConnected = false;
let previousSmsCount = 0;
let previousChallanCount = 0;

// ── Webcam State ──
let cameraStream = null;
let isCameraOn = false;
let isScanning = false;
let detectorAvailable = false;

// ──────────────────────────────────────────────
//   INITIALIZATION
// ──────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
    updateCameraTimestamp();
    setInterval(updateCameraTimestamp, 1000);

    // Initial fetch
    refreshAll();

    // Check if YOLO detector is available
    checkDetectorStatus();

    // Auto-refresh every 5 seconds
    setInterval(refreshAll, POLL_INTERVAL);
});

// ──────────────────────────────────────────────
//   API CALLS
// ──────────────────────────────────────────────

async function apiCall(endpoint, method = "GET", body = null) {
    try {
        const options = {
            method,
            headers: { "Content-Type": "application/json" },
        };
        if (body) options.body = JSON.stringify(body);

        const response = await fetch(`${API_BASE}${endpoint}`, options);
        const data = await response.json();

        setConnectionStatus(true);
        return { ok: response.ok, status: response.status, data };
    } catch (error) {
        setConnectionStatus(false);
        return { ok: false, status: 0, data: null, error };
    }
}

function setConnectionStatus(connected) {
    isConnected = connected;
    const statusEl = document.getElementById("server-status");
    const errorEl = document.getElementById("connection-error");

    if (connected) {
        statusEl.innerHTML = `<div class="status-dot"></div><span>System Active</span>`;
        statusEl.style.color = "#22c55e";
        errorEl.classList.remove("visible");
    } else {
        statusEl.innerHTML = `<div class="status-dot" style="background:#ef4444;animation:none;"></div><span>Disconnected</span>`;
        statusEl.style.color = "#ef4444";
        errorEl.classList.add("visible");
    }
}

// ──────────────────────────────────────────────
//   YOLO DETECTOR STATUS
// ──────────────────────────────────────────────

async function checkDetectorStatus() {
    const res = await apiCall("/api/detector-status");
    if (res.ok) {
        detectorAvailable = res.data.available;
        const scanBtn = document.getElementById("btn-scan");
        if (detectorAvailable) {
            // Enable scan button only when camera is on (handled in toggleCamera)
            scanBtn.title = "Capture frame and scan plate with YOLO + EasyOCR";
        } else {
            scanBtn.title = "YOLO/EasyOCR not installed on server";
            scanBtn.disabled = true;
        }
    }
}

// ──────────────────────────────────────────────
//   WEBCAM CONTROLS
// ──────────────────────────────────────────────

async function toggleCamera() {
    if (isCameraOn) {
        stopCamera();
    } else {
        await startCamera();
    }
}

async function startCamera() {
    const video = document.getElementById("webcam-video");
    const placeholder = document.getElementById("camera-placeholder");
    const cameraBtn = document.getElementById("btn-camera");
    const scanBtn = document.getElementById("btn-scan");
    const labelText = document.getElementById("camera-label-text");
    const feedEl = document.getElementById("camera-feed");

    try {
        // Request webcam access
        cameraStream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: { ideal: 1280 },
                height: { ideal: 720 },
                facingMode: "environment", // Prefer rear camera on mobile
            },
            audio: false,
        });

        video.srcObject = cameraStream;
        video.classList.add("active");
        placeholder.style.display = "none";
        feedEl.classList.add("cam-active");

        cameraBtn.innerHTML = "⏹️ Stop Camera";
        cameraBtn.classList.add("btn-stop");
        labelText.textContent = "REC — No Parking Zone Cam 01";

        // Enable scan button if detector is available
        if (detectorAvailable) {
            scanBtn.disabled = false;
        }

        isCameraOn = true;
        showToast("📷 Camera started successfully", "success");
    } catch (err) {
        console.error("Camera error:", err);
        if (err.name === "NotAllowedError") {
            showToast("❌ Camera access denied. Please allow camera permission.", "error");
        } else if (err.name === "NotFoundError") {
            showToast("❌ No camera found. Connect a webcam and retry.", "error");
        } else {
            showToast(`❌ Camera error: ${err.message}`, "error");
        }
    }
}

function stopCamera() {
    const video = document.getElementById("webcam-video");
    const placeholder = document.getElementById("camera-placeholder");
    const cameraBtn = document.getElementById("btn-camera");
    const scanBtn = document.getElementById("btn-scan");
    const labelText = document.getElementById("camera-label-text");
    const feedEl = document.getElementById("camera-feed");
    const plateDisplay = document.getElementById("detected-plate-display");

    if (cameraStream) {
        cameraStream.getTracks().forEach((track) => track.stop());
        cameraStream = null;
    }

    video.srcObject = null;
    video.classList.remove("active");
    placeholder.style.display = "";
    feedEl.classList.remove("cam-active");

    cameraBtn.innerHTML = "📷 Start Camera";
    cameraBtn.classList.remove("btn-stop");
    labelText.textContent = "CAMERA OFF";
    scanBtn.disabled = true;
    plateDisplay.classList.remove("visible");

    isCameraOn = false;
    showToast("📷 Camera stopped", "info");
}

// ──────────────────────────────────────────────
//   PLATE SCANNING (YOLO + EasyOCR)
// ──────────────────────────────────────────────

async function scanPlate() {
    if (!isCameraOn || isScanning) return;

    const video = document.getElementById("webcam-video");
    const canvas = document.getElementById("capture-canvas");
    const scanOverlay = document.getElementById("scan-overlay");
    const plateDisplay = document.getElementById("detected-plate-display");
    const progressWrapper = document.getElementById("ocr-progress-wrapper");
    const progressFill = document.getElementById("ocr-progress-fill");
    const progressText = document.getElementById("ocr-progress-text");
    const scanBtn = document.getElementById("btn-scan");

    isScanning = true;
    scanBtn.disabled = true;
    scanBtn.textContent = "⏳ Scanning...";

    // Show scan overlay
    scanOverlay.classList.add("active");
    plateDisplay.classList.remove("visible");
    plateDisplay.classList.remove("error");

    // Show progress bar
    progressWrapper.style.display = "flex";
    progressFill.style.width = "10%";
    progressText.textContent = "Capturing frame...";

    // Capture frame from video to canvas
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    progressFill.style.width = "30%";
    progressText.textContent = "Sending to YOLO + EasyOCR...";

    // Convert canvas to base64
    const base64Image = canvas.toDataURL("image/jpeg", 0.85);

    progressFill.style.width = "50%";
    progressText.textContent = "Running vehicle detection...";

    // Send to backend for YOLO + EasyOCR processing
    const res = await apiCall("/api/scan-plate", "POST", { image: base64Image });

    progressFill.style.width = "90%";
    progressText.textContent = "Processing results...";

    // Small delay to show progress
    await new Promise((r) => setTimeout(r, 300));

    scanOverlay.classList.remove("active");

    if (res.ok && res.data) {
        const data = res.data;

        if (data.best_plate) {
            // Plate found!
            progressFill.style.width = "100%";
            progressText.textContent = `✅ Plate detected: ${data.best_plate}`;

            plateDisplay.textContent = `🔍 ${data.best_plate}`;
            plateDisplay.classList.remove("error");
            plateDisplay.classList.add("visible");

            if (data.auto_registered) {
                showToast(
                    `🎯 YOLO detected ${data.vehicles_detected} vehicle(s) — Plate "${data.best_plate}" scanned and registered!`,
                    "success"
                );
                flashCameraFeed();
                await refreshAll();
            } else {
                showToast(
                    `🔍 Plate "${data.best_plate}" detected (already tracked)`,
                    "warning"
                );
            }

            // Auto-hide plate display after 6 seconds
            setTimeout(() => plateDisplay.classList.remove("visible"), 6000);
        } else {
            // No plate found
            progressFill.style.width = "100%";
            progressText.textContent = `⚠️ No plate detected (${data.vehicles_detected} vehicle(s) found)`;

            plateDisplay.textContent = "❌ No plate detected";
            plateDisplay.classList.add("error");
            plateDisplay.classList.add("visible");

            const vehicleMsg =
                data.vehicles_detected > 0
                    ? `Vehicle(s) found but plate not readable.`
                    : `No vehicles in frame.`;
            showToast(`⚠️ ${vehicleMsg} Try moving closer to the plate.`, "warning");

            setTimeout(() => plateDisplay.classList.remove("visible"), 4000);
        }
    } else {
        progressFill.style.width = "100%";
        progressText.textContent = "❌ Scan failed";

        plateDisplay.textContent = "❌ Scan failed";
        plateDisplay.classList.add("error");
        plateDisplay.classList.add("visible");

        const errMsg = res.data?.error || "Server error during detection";
        showToast(`❌ ${errMsg}`, "error");

        setTimeout(() => plateDisplay.classList.remove("visible"), 4000);
    }

    // Reset UI
    isScanning = false;
    scanBtn.disabled = false;
    scanBtn.textContent = "🔍 Scan Plate";

    // Auto-hide progress bar after 5s
    setTimeout(() => {
        progressWrapper.style.display = "none";
        progressFill.style.width = "0%";
    }, 5000);
}

// ──────────────────────────────────────────────
//   REFRESH ALL DATA
// ──────────────────────────────────────────────

async function refreshAll() {
    await Promise.all([
        refreshStats(),
        refreshVehicles(),
        refreshSmsLog(),
        refreshChallans(),
    ]);
}

// ──────────────────────────────────────────────
//   STATS
// ──────────────────────────────────────────────

async function refreshStats() {
    const res = await apiCall("/api/stats");
    if (!res.ok) return;

    const s = res.data;
    animateValue("stat-total", s.total_detected);
    animateValue("stat-active", s.currently_in_zone);
    animateValue("stat-challans", s.challans_issued);
    animateValue("stat-sms", s.sms_sent);
}

function animateValue(elementId, newValue) {
    const el = document.getElementById(elementId);
    const current = parseInt(el.textContent) || 0;
    if (current === newValue) return;
    el.textContent = newValue;
    el.style.transform = "scale(1.15)";
    setTimeout(() => (el.style.transform = "scale(1)"), 200);
}

// ──────────────────────────────────────────────
//   VEHICLES TABLE
// ──────────────────────────────────────────────

async function refreshVehicles() {
    const res = await apiCall("/api/vehicles");
    if (!res.ok) return;

    const vehicles = res.data.vehicles;
    const tbody = document.getElementById("vehicles-tbody");
    const emptyState = document.getElementById("vehicles-empty");
    const badge = document.getElementById("vehicle-count-badge");

    badge.textContent = vehicles.length;

    if (vehicles.length === 0) {
        tbody.innerHTML = "";
        emptyState.style.display = "block";
        return;
    }

    emptyState.style.display = "none";

    tbody.innerHTML = vehicles
        .map((v) => {
            const statusClass = getStatusClass(v.status);
            const statusIcon = getStatusIcon(v.status);
            const entryTime = formatTime(v.entry_time);
            const elapsed = v.elapsed_display;
            const elapsedColor =
                v.elapsed_seconds >= 420
                    ? "#ef4444"
                    : v.elapsed_seconds >= 300
                    ? "#f59e0b"
                    : "#22c55e";

            return `
                <tr>
                    <td class="plate-cell">${v.plate}</td>
                    <td class="time-cell">${entryTime}</td>
                    <td class="elapsed-cell" style="color:${elapsedColor}">${elapsed}</td>
                    <td>
                        <span class="status-badge ${statusClass}">
                            ${statusIcon} ${v.status}
                        </span>
                    </td>
                    <td>
                        <button class="btn btn-danger btn-xs" onclick="simulateExit('${v.plate}')">
                            🚪 Vehicle Left
                        </button>
                    </td>
                </tr>
            `;
        })
        .join("");
}

function getStatusClass(status) {
    switch (status) {
        case "Monitoring":       return "status-monitoring";
        case "ILLEGAL PARKING":  return "status-illegal";
        case "SMS Sent":         return "status-sms-sent";
        case "Challan Issued":   return "status-challan";
        default:                 return "";
    }
}

function getStatusIcon(status) {
    switch (status) {
        case "Monitoring":       return "🟡";
        case "ILLEGAL PARKING":  return "🔴";
        case "SMS Sent":         return "📨";
        case "Challan Issued":   return "🚨";
        default:                 return "";
    }
}

// ──────────────────────────────────────────────
//   SMS LOG
// ──────────────────────────────────────────────

async function refreshSmsLog() {
    const res = await apiCall("/api/sms-log");
    if (!res.ok) return;

    const smsList = res.data.sms_log;
    const container = document.getElementById("sms-log-container");
    const badge = document.getElementById("sms-count-badge");
    const emptyEl = document.getElementById("sms-empty");

    badge.textContent = smsList.length;

    if (smsList.length === 0) {
        container.innerHTML = "";
        container.appendChild(emptyEl);
        emptyEl.style.display = "block";
        return;
    }

    if (smsList.length > previousSmsCount && previousSmsCount > 0) {
        const newest = smsList[smsList.length - 1];
        showToast(`📨 SMS sent to owner of ${newest.plate}`, "warning");
    }
    previousSmsCount = smsList.length;

    container.innerHTML = smsList
        .slice()
        .reverse()
        .map((sms) => {
            const time = formatTime(sms.timestamp);
            return `
                <div class="sms-bubble">
                    <div class="sms-plate">📱 ${sms.plate}</div>
                    <div class="sms-text">${sms.message}</div>
                    <div class="sms-time">${time}</div>
                </div>
            `;
        })
        .join("");
}

// ──────────────────────────────────────────────
//   CHALLANS TABLE
// ──────────────────────────────────────────────

async function refreshChallans() {
    const res = await apiCall("/api/challans");
    if (!res.ok) return;

    const challans = res.data.challans;
    const tbody = document.getElementById("challans-tbody");
    const emptyState = document.getElementById("challans-empty");
    const badge = document.getElementById("challan-count-badge");

    badge.textContent = challans.length;

    if (challans.length === 0) {
        tbody.innerHTML = "";
        emptyState.style.display = "block";
        return;
    }

    if (challans.length > previousChallanCount && previousChallanCount > 0) {
        const newest = challans[challans.length - 1];
        showToast(`🚨 Challan ${newest.challan_id} issued for ${newest.plate}`, "error");
    }
    previousChallanCount = challans.length;

    emptyState.style.display = "none";

    tbody.innerHTML = challans
        .map((c) => {
            const time = c.violation_time_display || formatTime(c.violation_time);
            const gps = `${c.gps.lat}°N, ${c.gps.lng}°E`;

            return `
                <tr>
                    <td class="challan-id-cell">${c.challan_id}</td>
                    <td class="plate-cell">${c.plate}</td>
                    <td class="time-cell">${time}</td>
                    <td>${c.location}</td>
                    <td class="time-cell">${gps}</td>
                    <td class="fine-cell">₹${c.fine_amount}</td>
                    <td>
                        <span class="challan-status-badge">🚨 ${c.status}</span>
                    </td>
                    <td>
                        <button class="btn btn-ghost btn-xs" onclick='viewChallan(${JSON.stringify(c).replace(/'/g, "&#39;")})'>
                            📄 View
                        </button>
                    </td>
                </tr>
            `;
        })
        .join("");
}

// ──────────────────────────────────────────────
//   ACTIONS (Simulate)
// ──────────────────────────────────────────────

async function simulateDetection() {
    const btn = document.getElementById("btn-detect");
    btn.disabled = true;
    btn.textContent = "⏳ Detecting...";

    const res = await apiCall("/api/vehicle/detect", "POST");

    btn.disabled = false;
    btn.textContent = "🚘 Simulate Detection";

    if (res.ok) {
        showToast(`🚘 Vehicle detected: ${res.data.plate}`, "success");
        flashCameraFeed();
        await refreshAll();
    } else if (res.data) {
        showToast(`⚠️ ${res.data.error || "Detection failed"}`, "error");
    }
}

async function simulateDetectionCustom() {
    const plate = prompt("Enter custom number plate (e.g., DL 03 AB 1234):");
    if (!plate || plate.trim() === "") return;

    const res = await apiCall("/api/vehicle/detect", "POST", {
        plate: plate.trim().toUpperCase(),
    });

    if (res.ok) {
        showToast(`🚘 Vehicle detected: ${res.data.plate}`, "success");
        flashCameraFeed();
        await refreshAll();
    } else if (res.data) {
        showToast(`⚠️ ${res.data.error || "Detection failed"}`, "error");
    }
}

async function simulateExit(plate) {
    const res = await apiCall("/api/vehicle/exit", "POST", { plate });

    if (res.ok) {
        showToast(`🚪 Vehicle ${plate} has left the zone`, "info");
        await refreshAll();
    } else if (res.data) {
        showToast(`⚠️ ${res.data.error || "Exit failed"}`, "error");
    }
}

// ──────────────────────────────────────────────
//   CHALLAN MODAL
// ──────────────────────────────────────────────

function viewChallan(challan) {
    const modal = document.getElementById("challan-modal");
    const body = document.getElementById("challan-modal-body");

    const gps = `${challan.gps.lat}°N, ${challan.gps.lng}°E`;
    const time = challan.violation_time_display || formatTime(challan.violation_time);

    body.innerHTML = `
        <div class="challan-doc">
            <div class="challan-doc-header">
                <h3>🚨 Traffic Violation eChallan</h3>
                <p>Delhi Traffic Police — Automated System</p>
            </div>
            <div class="challan-doc-id">
                <span>${challan.challan_id}</span>
            </div>
            <div class="challan-doc-field">
                <span class="label">Vehicle No.</span>
                <span class="value mono">${challan.plate}</span>
            </div>
            <div class="challan-doc-field">
                <span class="label">Violation</span>
                <span class="value">Parking in No-Parking Zone</span>
            </div>
            <div class="challan-doc-field">
                <span class="label">Date & Time</span>
                <span class="value mono">${time}</span>
            </div>
            <div class="challan-doc-field">
                <span class="label">Location</span>
                <span class="value">${challan.location}</span>
            </div>
            <div class="challan-doc-field">
                <span class="label">GPS</span>
                <span class="value mono">${gps}</span>
            </div>
            <div class="challan-doc-field">
                <span class="label">Section</span>
                <span class="value">MV Act Sec. 177 / 184</span>
            </div>
            <div class="challan-doc-field">
                <span class="label">Fine Amount</span>
                <span class="value fine">₹${challan.fine_amount}</span>
            </div>
            <div class="challan-doc-field">
                <span class="label">Status</span>
                <span class="value" style="color:#ef4444;font-weight:700;">${challan.status}</span>
            </div>
            <div class="challan-doc-footer">
                <p>This is a system-generated eChallan. Please pay the fine within 60 days to avoid further action.</p>
            </div>
        </div>
    `;

    modal.classList.add("active");
}

function closeModal() {
    document.getElementById("challan-modal").classList.remove("active");
}

// Close modal on overlay click
document.addEventListener("click", (e) => {
    if (e.target.id === "challan-modal") closeModal();
});

// Close modal on Escape
document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeModal();
});

// ──────────────────────────────────────────────
//   UTILITIES
// ──────────────────────────────────────────────

function formatTime(isoString) {
    try {
        const date = new Date(isoString);
        return date.toLocaleTimeString("en-IN", {
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: true,
        });
    } catch {
        return isoString;
    }
}

function updateCameraTimestamp() {
    const el = document.getElementById("camera-timestamp");
    const now = new Date();
    el.textContent = now.toLocaleTimeString("en-IN", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false,
    });
}

function flashCameraFeed() {
    const feed = document.getElementById("camera-feed");
    feed.style.boxShadow = "inset 0 0 60px rgba(34, 197, 94, 0.3)";
    setTimeout(() => {
        feed.style.boxShadow = "";
    }, 600);
}

// ──────────────────────────────────────────────
//   TOAST NOTIFICATIONS
// ──────────────────────────────────────────────

function showToast(message, type = "info") {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    container.appendChild(toast);

    // Auto-remove after 4 seconds
    setTimeout(() => {
        toast.classList.add("fadeOut");
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}
