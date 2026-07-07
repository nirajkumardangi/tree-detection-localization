/* c:\Users\gadge\Desktop\tree-detection-localization\dashboard\js\app.js */

// UI Elements selection
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');

const uploadSection = document.getElementById('upload-section');
const resultsSection = document.getElementById('results-section');
const errorPanel = document.getElementById('error-panel');
const resultsDataGrid = document.getElementById('results-data-grid');

const displayFilename = document.getElementById('display-filename');
const displayFilesize = document.getElementById('display-filesize');
const imgOriginal = document.getElementById('img-original');
const imgAnnotated = document.getElementById('img-annotated');
const annotatedLoading = document.getElementById('annotated-loading');

const statTreeCount = document.getElementById('stat-tree-count');
const statConfidence = document.getElementById('stat-confidence');
const statValidation = document.getElementById('stat-validation');
const statQuality = document.getElementById('stat-quality');

const cardTreeCount = document.getElementById('card-tree-count');
const cardConfidence = document.getElementById('card-confidence');
const cardValidation = document.getElementById('card-validation');
const cardQuality = document.getElementById('card-quality');

const detectionTableBody = document.getElementById('detection-table-body');
const qualityPillsContainer = document.getElementById('quality-pills-container');

const linkAnnotatedImage = document.getElementById('link-annotated-image');
const linkMetadataJson = document.getElementById('link-metadata-json');

const btnChangeImage = document.getElementById('btn-change-image');
const btnUploadAnother = document.getElementById('btn-upload-another');
const btnRetryUpload = document.getElementById('btn-retry-upload');

const statusBadge = document.getElementById('status-badge');
const statusDot = document.getElementById('status-dot');
const statusText = document.getElementById('status-text');

const footerYear = document.getElementById('footer-year');
footerYear.innerText = new Date().getFullYear();

// State Variables
let selectedFile = null;
const apiBase = window.location.origin;

// API Health Checker
async function checkHealth() {
  try {
    const res = await fetch(`${apiBase}/health`);
    if (res.ok) {
      statusBadge.className = 'flex items-center gap-1.5 px-3 py-1 rounded-full text-[9px] md:text-[10px] tracking-[0.5px] uppercase font-bold border shrink-0 transition-all duration-300 border-green-500/30 bg-green-500/10 text-green-300';
      statusDot.className = 'w-1.5 h-1.5 md:w-2 md:h-2 rounded-full bg-green-400 shadow-[0_0_8px_rgba(46,160,67,0.4)] animate-pulse';
      statusText.innerText = 'Live';
    } else {
      setOffline();
    }
  } catch (e) {
    setOffline();
  }
}

function setOffline() {
  statusBadge.className = 'flex items-center gap-1.5 px-3 py-1 rounded-full text-[9px] md:text-[10px] tracking-[0.5px] uppercase font-bold border shrink-0 transition-all duration-300 border-border-primary bg-bg-secondary text-text-muted';
  statusDot.className = 'w-1.5 h-1.5 md:w-2 md:h-2 rounded-full bg-text-muted';
  statusText.innerText = 'Offline';
}

// Initial health check and interval polling
checkHealth();
setInterval(checkHealth, 10000);

// Helper functions
function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function getStatusColor(val) {
  if (!val) return '';
  const v = val.toUpperCase();
  if (v === 'PASS' || v === 'ACCEPTABLE') return 'text-green-300';
  if (v === 'REVIEW' || v === 'NEEDS REVIEW') return 'text-amber-300';
  if (v === 'FAIL' || v === 'REJECT') return 'text-red-300';
  return 'text-text-primary';
}

function getPillClass(value) {
  if (!value) return '';
  const v = value.toLowerCase();
  if (['acceptable', 'normal', 'pass'].includes(v)) {
    return 'bg-green-500/10 text-green-300 border-green-500/25';
  }
  if (['review', 'slightly_blurry'].includes(v)) {
    return 'bg-amber-500/10 text-amber-300 border-amber-500/25';
  }
  return 'bg-red-500/10 text-red-300 border-red-500/25';
}

// File Input trigger
function triggerFileInput() {
  fileInput.click();
}

// Drag and drop event handlers
function handleFileDrag(e) {
  e.preventDefault();
  e.stopPropagation();
  if (e.type === "dragenter" || e.type === "dragover") {
    dropZone.classList.add('border-green-500', 'bg-green-500/5');
  } else if (e.type === "dragleave" || e.type === "drop") {
    dropZone.classList.remove('border-green-500', 'bg-green-500/5');
  }
}

function handleFileDrop(e) {
  e.preventDefault();
  e.stopPropagation();
  dropZone.classList.remove('border-green-500', 'bg-green-500/5');
  
  if (e.dataTransfer.files && e.dataTransfer.files[0]) {
    handleFileSelection(e.dataTransfer.files[0]);
  }
}

function handleFileChange(e) {
  if (e.target.files && e.target.files[0]) {
    handleFileSelection(e.target.files[0]);
  }
}

// Process selected file
function handleFileSelection(file) {
  const validTypes = ["image/jpeg", "image/png", "image/heic"];
  const ext = file.name.split(".").pop().toLowerCase();
  const validExts = ["jpg", "jpeg", "png", "heic"];

  if (!validTypes.includes(file.type) && !validExts.includes(ext)) {
    alert("Unsupported file format. Please upload JPG, PNG, or HEIC.");
    return;
  }

  selectedFile = file;
  displayFilename.innerText = file.name;
  displayFilesize.innerText = formatFileSize(file.size);
  
  // Set original image preview source
  const objectUrl = URL.createObjectURL(file);
  imgOriginal.src = objectUrl;
  imgAnnotated.src = "";
  
  // Update view visibility states
  uploadSection.classList.add('hidden');
  errorPanel.classList.add('hidden');
  resultsSection.classList.remove('hidden');
  annotatedLoading.classList.remove('hidden');
  resultsDataGrid.classList.add('hidden');

  runDetection(file);
}

// Reset workspace state
function resetState() {
  selectedFile = null;
  fileInput.value = '';
  imgOriginal.src = '';
  imgAnnotated.src = '';
  uploadSection.classList.remove('hidden');
  resultsSection.classList.add('hidden');
  errorPanel.classList.add('hidden');
}

// Pipeline upload request
async function runDetection(file) {
  const formData = new FormData();
  formData.append("file", file, file.name);

  try {
    const response = await fetch(`${apiBase}/detect`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.detail || `Server error ${response.status}`);
    }

    const data = await response.json();
    
    if (data.annotated_image) {
      imgAnnotated.src = `${apiBase}/${data.annotated_image}`;
    }

    if (data.metadata) {
      // Fetch metadata details JSON
      const metaUrl = data.metadata.startsWith('http') ? data.metadata : `${apiBase}/${data.metadata}`;
      const metaResponse = await fetch(metaUrl);
      if (!metaResponse.ok) {
        throw new Error("Failed to load pipeline metadata details");
      }
      const meta = await metaResponse.json();

      const detObj = meta.detection || {};
      const qualObj = meta.quality || {};
      const scoreObj = meta.score || {};
      const detList = detObj.detections || [];
      
      const maxConf = detList.length > 0
        ? Math.max(...detList.map(d => d.confidence))
        : 0;

      // Render stats card labels and contents
      statTreeCount.innerText = detObj.tree_count !== undefined ? detObj.tree_count : 0;
      statConfidence.innerText = maxConf > 0 ? (maxConf * 100).toFixed(0) + '%' : '—';
      
      const valStatus = scoreObj.validation_status || meta.status || '—';
      statValidation.innerText = valStatus;
      statValidation.className = `stat-value text-xl font-bold tracking-tight transition-all ${getStatusColor(valStatus)}`;
      
      const qualStatus = qualObj.overall_quality || '—';
      statQuality.innerText = qualStatus;
      statQuality.className = `stat-value text-xl font-bold tracking-tight transition-all ${getStatusColor(qualStatus)}`;

      // Highlight stats cards borders
      if (detObj.tree_count > 0) {
        cardTreeCount.classList.add('border-green-500/40', 'bg-green-500/[0.03]');
      } else {
        cardTreeCount.classList.remove('border-green-500/40', 'bg-green-500/[0.03]');
      }

      if (maxConf >= 0.75) {
        cardConfidence.classList.add('border-blue-500/40', 'bg-blue-500/[0.03]');
      } else {
        cardConfidence.classList.remove('border-blue-500/40', 'bg-blue-500/[0.03]');
      }

      // Update downstream link destinations
      linkAnnotatedImage.href = `${apiBase}/${data.annotated_image}`;
      linkMetadataJson.href = metaUrl;

      // Populate coordinates data rows into details table
      detectionTableBody.innerHTML = '';
      if (detList.length === 0) {
        detectionTableBody.innerHTML = `
          <tr>
            <td colSpan="4" class="text-center text-text-secondary py-6">
              No trees detected
            </td>
          </tr>
        `;
      } else {
        detList.forEach((det) => {
          const confPct = (det.confidence * 100).toFixed(1);
          const box = det.bounding_box || {};
          const tr = document.createElement('tr');
          tr.className = 'border-b border-border-primary/40 hover:bg-white/[0.02] transition-colors';
          tr.innerHTML = `
            <td class="p-3 font-medium">${det.detection_id}</td>
            <td class="p-3">${det.class_label || 'tree'}</td>
            <td class="p-3">
              <div class="conf-cell flex items-center gap-3">
                <span class="w-12">${confPct}%</span>
                <div class="conf-bar w-20 h-1.5 bg-bg-primary rounded-full overflow-hidden">
                  <div class="conf-bar-fill h-full bg-gradient-to-r from-green-500 to-green-300 rounded-full" style="width: ${confPct}%" />
                </div>
              </div>
            </td>
            <td class="p-3 font-mono text-xs text-text-secondary">
              (${box.x_min || 0}, ${box.y_min || 0}) &rarr; (${box.x_max || 0}, ${box.y_max || 0})
            </td>
          `;
          detectionTableBody.appendChild(tr);
        });
      }

      // Render quality indicator pills list
      qualityPillsContainer.innerHTML = '';
      const subQualities = [
        { key: 'blur', label: 'Blur', value: qualObj.blur_status },
        { key: 'brightness', label: 'Brightness', value: qualObj.brightness },
        { key: 'contrast', label: 'Contrast', value: qualObj.contrast },
        { key: 'resolution', label: 'Resolution', value: qualObj.resolution_status }
      ];

      subQualities.forEach((q) => {
        if (q.value) {
          const span = document.createElement('span');
          span.className = `pill px-3 py-1.5 rounded-full text-xs font-semibold border tracking-wide uppercase transition-all duration-300 ${getPillClass(q.value)}`;
          span.innerText = `${q.label}: ${q.value}`;
          qualityPillsContainer.appendChild(span);
        }
      });

    } else {
      // Fallback
      statTreeCount.innerText = 0;
      statConfidence.innerText = '—';
      statValidation.innerText = data.status || '—';
      statQuality.innerText = '—';
    }

    annotatedLoading.classList.add('hidden');
    resultsDataGrid.classList.remove('hidden');

  } catch (err) {
    console.error(err);
    document.getElementById('error-message').innerText = err.message || 'Detection request failed.';
    resultsSection.classList.add('hidden');
    errorPanel.classList.remove('hidden');
  }
}

// Bind event listeners
dropZone.addEventListener('click', triggerFileInput);
dropZone.addEventListener('dragenter', handleFileDrag);
dropZone.addEventListener('dragover', handleFileDrag);
dropZone.addEventListener('dragleave', handleFileDrag);
dropZone.addEventListener('drop', handleFileDrop);
fileInput.addEventListener('change', handleFileChange);

btnChangeImage.addEventListener('click', resetState);
btnUploadAnother.addEventListener('click', resetState);
btnRetryUpload.addEventListener('click', resetState);
