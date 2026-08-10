/**
 * EmotionAI Dashboard - Frontend JavaScript Engine
 * Manages file uploads, AI API execution, dynamic results rendering & history updates
 */

document.addEventListener('DOMContentLoaded', () => {
    initDropzone();
    initUploadForm();
});

// Global state tracking
let selectedFile = null;

/**
 * Initialize Drag & Drop functionality
 */
function initDropzone() {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('imageInput');

    if (!dropzone || !fileInput) return;

    // Click to select file
    dropzone.addEventListener('click', () => fileInput.click());

    // Drag events
    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.remove('dragover');
        }, false);
    });

    // Handle dropped file
    dropzone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;

        if (files && files.length > 0) {
            handleFileSelection(files[0]);
        }
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });
}

/**
 * Handle image file selection & update live preview
 */
function handleFileSelection(file) {
    if (!file.type.match('image.*')) {
        showAlert('Please upload a valid image file (JPG or PNG).', 'warning');
        return;
    }

    if (file.size > 16 * 1024 * 1024) {
        showAlert('Image file size must be less than 16MB.', 'danger');
        return;
    }

    selectedFile = file;

    // Display image preview
    const reader = new FileReader();
    reader.onload = (e) => {
        const rawPreviewImg = document.getElementById('rawPreviewImg');
        const annotatedResultImg = document.getElementById('annotatedResultImg');
        const emptyState = document.getElementById('emptyState');
        const previewContainer = document.getElementById('previewContainer');
        const btnRunAI = document.getElementById('btnRunAI');

        if (rawPreviewImg) {
            rawPreviewImg.src = e.target.result;
            rawPreviewImg.classList.remove('d-none');
        }
        if (annotatedResultImg) {
            annotatedResultImg.classList.add('d-none');
        }
        if (emptyState) {
            emptyState.classList.add('d-none');
        }

        if (btnRunAI) {
            btnRunAI.disabled = false;
        }

        // Show filename in upload card
        const fileInfoText = document.getElementById('fileInfoText');
        if (fileInfoText) {
            fileInfoText.innerHTML = `<i class="fa-solid fa-circle-check text-success me-2"></i> Selected: <strong>${file.name}</strong> (${(file.size / 1024).toFixed(1)} KB)`;
        }
    };
    reader.readAsDataURL(file);
}

/**
 * Handle form submission & call REST API endpoint
 */
function initUploadForm() {
    const uploadForm = document.getElementById('uploadForm');
    if (!uploadForm) return;

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!selectedFile) {
            showAlert('Please select an image file first.', 'info');
            return;
        }

        // Show Scanner Loading Animation
        showScannerLoader(true);

        const formData = new FormData();
        formData.append('image', selectedFile);

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            showScannerLoader(false);

            if (!response.ok || !data.success) {
                showAlert(data.error || 'Failed to process AI analysis.', 'danger');
                return;
            }

            // Render AI Analysis Results
            renderResults(data);

            // Fetch and refresh History Table
            refreshHistoryTable();

            showAlert('AI Emotion & Age Analysis completed successfully!', 'success');

        } catch (error) {
            showScannerLoader(false);
            console.error('AI Processing Error:', error);
            showAlert('Network or server error during AI analysis.', 'danger');
        }
    });
}

/**
 * Show/Hide Scanner Loading Overlay
 */
function showScannerLoader(show) {
    const scannerOverlay = document.getElementById('scannerOverlay');
    const btnRunAI = document.getElementById('btnRunAI');

    if (scannerOverlay) {
        scannerOverlay.classList.toggle('d-none', !show);
    }
    if (btnRunAI) {
        btnRunAI.disabled = show;
        btnRunAI.innerHTML = show 
            ? `<span class="spinner-border spinner-border-sm me-2" role="status"></span> Running AI Model...`
            : `<i class="fa-solid fa-wand-magic-sparkles me-2"></i> Run AI Analysis`;
    }
}

/**
 * Render AI analysis results on dashboard cards
 */
function renderResults(data) {
    const { results, recommendations } = data;

    // 1. Update Preview to AI Annotated Image
    const rawPreviewImg = document.getElementById('rawPreviewImg');
    const annotatedResultImg = document.getElementById('annotatedResultImg');

    if (rawPreviewImg) rawPreviewImg.classList.add('d-none');
    if (annotatedResultImg) {
        // Add cache-busting timestamp query parameter
        annotatedResultImg.src = results.annotated_url + '?t=' + new Date().getTime();
        annotatedResultImg.classList.remove('d-none');
    }

    // 2. Card 3: AI Analysis Results
    const resFaceDetected = document.getElementById('resFaceDetected');
    const resAge = document.getElementById('resAge');
    const resEmotionPill = document.getElementById('resEmotionPill');
    const resConfidenceBar = document.getElementById('resConfidenceBar');
    const resConfidenceVal = document.getElementById('resConfidenceVal');

    if (resFaceDetected) {
        resFaceDetected.innerHTML = results.face_detected === 'YES' 
            ? `<span class="badge bg-success-subtle text-success px-3 py-2 border border-success"><i class="fa-solid fa-check me-1"></i> YES (${results.faces_count} Face Detected)</span>`
            : `<span class="badge bg-warning-subtle text-warning px-3 py-2 border border-warning"><i class="fa-solid fa-exclamation-triangle me-1"></i> NO (Global Image Model Used)</span>`;
    }

    if (resAge) {
        resAge.innerText = `${results.age} years`;
    }

    if (resEmotionPill) {
        const emotionLower = results.emotion.toLowerCase();
        resEmotionPill.className = `emotion-pill ${emotionLower}`;
        resEmotionPill.innerHTML = `<i class="fa-solid fa-face-smile me-1"></i> ${results.emotion}`;
    }

    if (resConfidenceBar && resConfidenceVal) {
        resConfidenceBar.style.width = `${results.confidence}%`;
        resConfidenceVal.innerText = `${results.confidence}%`;
    }

    // Unhide Results Card if hidden
    const resultsContainer = document.getElementById('resultsContainer');
    if (resultsContainer) {
        resultsContainer.classList.remove('d-none');
    }

    // 3. Card 4: Music Recommendations
    renderMusicRecommendations(results.emotion, recommendations);
}

/**
 * Render Music Recommendations Grid matching User's preferred layout
 * Green "CLICK TO LISTEN SOUND" button plays local audio stream inside card player box!
 */
function renderMusicRecommendations(emotion, songs) {
    const musicContainer = document.getElementById('musicContainer');
    const musicEmotionBadge = document.getElementById('musicEmotionBadge');

    if (musicEmotionBadge) {
        musicEmotionBadge.innerText = `Tailored for: ${emotion}`;
    }

    if (!musicContainer) return;

    if (!songs || songs.length === 0) {
        musicContainer.innerHTML = `<div class="col-12 text-center text-muted py-4">No music recommendations found.</div>`;
        return;
    }

    let html = '';
    songs.forEach((song, idx) => {
        const titleEscaped = escapeHtml(song.title).replace(/'/g, "\\'");
        const artistEscaped = escapeHtml(song.artist).replace(/'/g, "\\'");
        const audioUrl = song.audio_url || '/static/audio/happy.wav';
        const spEmbed = song.spotify_embed || '';
        const cardId = `card_item_${idx}`;

        html += `
        <div class="col-md-6 col-lg-6 mb-4">
            <div class="song-card h-100 p-3">
                
                <!-- Card Header -->
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="badge bg-primary-subtle text-primary border border-primary px-2 py-1" style="font-size: 0.75rem;">
                        <i class="fa-solid fa-music me-1"></i> ${song.badge || song.genre}
                    </span>
                    <a href="${song.youtube_url}" target="_blank" rel="noopener" class="text-muted small text-decoration-none" title="Open YouTube in new tab">
                        <i class="fa-solid fa-arrow-up-right-from-square me-1"></i> Open Tab
                    </a>
                </div>
                
                <!-- Song Title & Artist -->
                <h5 class="fw-bold mb-1 text-white text-truncate">${escapeHtml(song.title)}</h5>
                <p class="text-muted small mb-3 text-truncate"><i class="fa-solid fa-user-astronaut me-1"></i> ${escapeHtml(song.artist)}</p>

                <!-- GREEN CLICK TO LISTEN SOUND BUTTON -->
                <div class="p-2 rounded mb-2" style="background: rgba(139, 92, 246, 0.12); border: 1px solid rgba(139, 92, 246, 0.25);">
                    <button id="btn_play_${cardId}" onclick="playOriginalSongSound('${cardId}', '${titleEscaped}', '${artistEscaped}', '${audioUrl}')" class="btn btn-success w-100 fw-bold py-2 mb-2 d-flex align-items-center justify-content-center gap-2 shadow">
                        <i class="fa-solid fa-volume-high fs-5"></i> <span>CLICK TO LISTEN SOUND</span>
                    </button>
                    
                    <!-- GUARANTEED LOCAL AUDIO PLAYER BOX -->
                    <div id="player_box_${cardId}" class="card-player-box d-none rounded p-2 bg-dark border border-secondary mt-2">
                        <audio id="audio_${cardId}" controls class="w-100" style="height: 38px; filter: invert(0.85) hue-rotate(180deg);">
                            <source id="source_${cardId}" src="${audioUrl}" type="audio/wav">
                            Your browser does not support audio playback.
                        </audio>
                    </div>
                </div>

                <!-- Spotify & YouTube Action Buttons -->
                <div class="d-flex gap-2 mt-3">
                    <a href="${song.youtube_url}" target="_blank" rel="noopener" class="song-btn-youtube flex-fill text-center justify-content-center border-0 text-decoration-none">
                        <i class="fa-brands fa-youtube me-1"></i> Watch Video
                    </a>
                    <a href="${song.spotify_url}" target="_blank" rel="noopener" class="song-btn-spotify flex-fill text-center justify-content-center text-decoration-none">
                        <i class="fa-brands fa-spotify me-1"></i> Spotify Tab
                    </a>
                </div>
            </div>
        </div>
        `;
    });

    musicContainer.innerHTML = html;
}

/**
 * Play Local Audio Stream when user clicks the green "CLICK TO LISTEN SOUND" button
 * Guaranteed sound output through speakers with zero domain errors!
 */
function playOriginalSongSound(cardId, title, artist, audioUrl) {
    const playerBox = document.getElementById(`player_box_${cardId}`);
    const audioElement = document.getElementById(`audio_${cardId}`);
    const btn = document.getElementById(`btn_play_${cardId}`);

    if (!playerBox || !audioElement) return;

    // Pause all other audio players
    document.querySelectorAll('audio').forEach(a => {
        if (a.id !== `audio_${cardId}`) {
            a.pause();
            a.currentTime = 0;
        }
    });

    document.querySelectorAll('[id^="player_box_"]').forEach(b => {
        if (b.id !== `player_box_${cardId}`) b.classList.add('d-none');
    });

    document.querySelectorAll('[id^="btn_play_"]').forEach(b => {
        if (b.id !== `btn_play_${cardId}`) {
            b.className = "btn btn-success w-100 fw-bold py-2 mb-2 d-flex align-items-center justify-content-center gap-2 shadow";
            b.innerHTML = `<i class="fa-solid fa-volume-high fs-5"></i> <span>CLICK TO LISTEN SOUND</span>`;
        }
    });

    if (audioElement.paused) {
        playerBox.classList.remove('d-none');
        audioElement.play().then(() => {
            if (btn) {
                btn.className = "btn btn-danger w-100 fw-bold py-2 mb-2 d-flex align-items-center justify-content-center gap-2 shadow";
                btn.innerHTML = `<i class="fa-solid fa-circle-pause fs-5"></i> <span>PAUSE SOUND</span>`;
            }
            showAlert(`Now Playing Audio Stream: <strong>${title}</strong> by ${artist}`, 'success');
        }).catch(err => {
            console.error("Audio playback error:", err);
            showAlert("Click the play button on the audio bar below to hear sound.", "warning");
        });
    } else {
        audioElement.pause();
        if (btn) {
            btn.className = "btn btn-success w-100 fw-bold py-2 mb-2 d-flex align-items-center justify-content-center gap-2 shadow";
            btn.innerHTML = `<i class="fa-solid fa-volume-high fs-5"></i> <span>CLICK TO LISTEN SOUND</span>`;
        }
    }
}



/**
 * Expand YouTube Video in bottom sticky bar
 */
function playYouTubeVideo(title, artist, embedUrl) {
    const inlinePlayer = document.getElementById('inlineMusicPlayer');
    const playerTitle = document.getElementById('playerTitle');
    const playerArtist = document.getElementById('playerArtist');
    const playerFrame = document.getElementById('playerFrame');

    if (!inlinePlayer || !playerFrame) return;

    if (playerTitle) playerTitle.innerText = title;
    if (playerArtist) playerArtist.innerText = artist;

    playerFrame.src = embedUrl;

    inlinePlayer.classList.remove('d-none');
}

/**
 * Close sticky player
 */
function closeMusicPlayer() {
    const inlinePlayer = document.getElementById('inlineMusicPlayer');
    const playerFrame = document.getElementById('playerFrame');

    if (playerFrame) playerFrame.src = '';
    if (inlinePlayer) inlinePlayer.classList.add('d-none');
}








/**
 * Fetch and render detection history list
 */
async function refreshHistoryTable() {
    const historyTableBody = document.getElementById('historyTableBody');
    if (!historyTableBody) return;

    try {
        const response = await fetch('/api/history');
        const data = await response.json();

        if (!response.ok || !data.success) return;

        const history = data.history;
        if (history.length === 0) {
            historyTableBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-muted py-4">
                    <i class="fa-solid fa-folder-open mb-2 text-secondary" style="font-size: 2rem;"></i><br>
                    No detection history found yet. Upload an image to get started!
                </td>
            </tr>`;
            return;
        }

        let html = '';
        history.forEach(item => {
            const emotionLower = item.emotion.toLowerCase();
            html += `
            <tr>
                <td>
                    <img src="${item.annotated_url}" alt="Prediction" class="rounded border" style="width: 48px; height: 48px; object-fit: cover;">
                </td>
                <td><span class="badge bg-secondary-subtle text-light">${item.created_at}</span></td>
                <td>
                    <span class="emotion-pill ${emotionLower} py-1 px-2" style="font-size: 0.8rem;">
                        ${item.emotion}
                    </span>
                </td>
                <td class="fw-bold">${item.age} yrs</td>
                <td>
                    <div class="d-flex align-items-center gap-2">
                        <div class="progress flex-grow-1" style="height: 6px; background: rgba(255,255,255,0.1);">
                            <div class="progress-bar bg-info" style="width: ${item.confidence}%;"></div>
                        </div>
                        <small class="text-muted">${item.confidence}%</small>
                    </div>
                </td>
                <td class="text-end">
                    <button onclick="deleteHistoryItem(${item.id})" class="btn btn-sm btn-outline-danger border-0">
                        <i class="fa-solid fa-trash-can"></i>
                    </button>
                </td>
            </tr>
            `;
        });

        historyTableBody.innerHTML = html;

    } catch (err) {
        console.error('Error fetching history:', err);
    }
}

/**
 * Delete single detection history entry
 */
async function deleteHistoryItem(id) {
    if (!confirm('Are you sure you want to delete this detection record?')) return;

    try {
        const response = await fetch(`/api/history/${id}`, { method: 'DELETE' });
        const data = await response.json();

        if (response.ok && data.success) {
            showAlert('History record deleted.', 'success');
            refreshHistoryTable();
        } else {
            showAlert(data.error || 'Failed to delete record.', 'danger');
        }
    } catch (err) {
        showAlert('Network error deleting history item.', 'danger');
    }
}

/**
 * Alert Popup helper
 */
function showAlert(message, type = 'info') {
    const alertBox = document.getElementById('globalAlert');
    if (!alertBox) return;

    alertBox.className = `alert alert-${type} alert-dismissible fade show glass-card shadow-lg mb-4`;
    alertBox.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fa-solid fa-circle-info me-2 fs-5"></i>
            <div>${message}</div>
        </div>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="alert"></button>
    `;
    alertBox.classList.remove('d-none');

    // Auto dismiss after 5 seconds
    setTimeout(() => {
        alertBox.classList.add('d-none');
    }, 5000);
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
