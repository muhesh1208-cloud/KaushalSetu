/**
 * KaushalSetu - Voice Input & Speech-to-Text Module
 * Uses standard Web Speech API for hands-free voice narrative capture.
 * Designed with multilingual support (Hindi, English, regional dialects).
 */

let recognition = null;
let isRecording = false;

document.addEventListener('DOMContentLoaded', () => {
  const micButton = document.getElementById('micButton');
  const micStatusText = document.getElementById('micStatusText');
  const micDot = document.getElementById('micDot');
  const textarea = document.getElementById('experience_text');
  const inputMethodField = document.getElementById('input_method');
  const languageSelect = document.getElementById('voiceLanguage');

  // Check Web Speech API availability
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (SpeechRecognition && micButton) {
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = languageSelect ? languageSelect.value : 'en-IN';

    if (languageSelect) {
      languageSelect.addEventListener('change', () => {
        if (recognition) {
          recognition.lang = languageSelect.value;
        }
      });
    }

    recognition.onstart = () => {
      isRecording = true;
      if (micDot) micDot.classList.add('recording');
      if (micStatusText) micStatusText.textContent = 'Listening... Speak clearly about your work';
      if (micButton) {
        micButton.innerHTML = '<span>⏹️</span> Stop Recording';
        micButton.classList.replace('btn-outline', 'btn-danger');
      }
      if (inputMethodField) inputMethodField.value = 'voice';
    };

    recognition.onresult = (event) => {
      let interimTranscript = '';
      let finalTranscript = '';

      for (let i = event.resultIndex; i < event.results.length; ++i) {
        if (event.results[i].isFinal) {
          finalTranscript += event.results[i][0].transcript + ' ';
        } else {
          interimTranscript += event.results[i][0].transcript;
        }
      }

      if (finalTranscript && textarea) {
        textarea.value += (textarea.value.length > 0 && !textarea.value.endsWith(' ') ? ' ' : '') + finalTranscript;
        // Trigger auto-expand or input event
        textarea.dispatchEvent(new Event('input'));
      }
    };

    recognition.onerror = (event) => {
      console.warn('Speech recognition status:', event.error);
      stopRecording();
      if (micStatusText) {
        if (event.error === 'not-allowed') {
          micStatusText.textContent = 'Microphone permission blocked. Please allow mic access.';
        } else {
          micStatusText.textContent = `Microphone paused (${event.error}). Click to speak again.`;
        }
      }
    };

    recognition.onend = () => {
      stopRecording();
    };

    micButton.addEventListener('click', (e) => {
      e.preventDefault();
      if (!isRecording) {
        startRecording();
      } else {
        stopRecording();
      }
    });

  } else if (micButton) {
    // Graceful fallback for non-supported browsers
    micButton.addEventListener('click', (e) => {
      e.preventDefault();
      alert('Your browser does not natively support the Web Speech API. Please type your experience in the box or test on Google Chrome / Microsoft Edge.');
    });
    if (micStatusText) {
      micStatusText.textContent = 'Voice input ready (Requires Chrome/Edge or Gemini Live backend)';
    }
  }
});

function startRecording() {
  if (recognition) {
    try {
      recognition.start();
    } catch (e) {
      console.error(e);
    }
  }
}

function stopRecording() {
  isRecording = false;
  if (recognition) {
    try {
      recognition.stop();
    } catch (e) {}
  }
  const micButton = document.getElementById('micButton');
  const micStatusText = document.getElementById('micStatusText');
  const micDot = document.getElementById('micDot');

  if (micDot) micDot.classList.remove('recording');
  if (micStatusText) micStatusText.textContent = 'Click to record your experience with voice';
  if (micButton) {
    micButton.innerHTML = '<span>🎤</span> Start Voice Input';
    micButton.classList.replace('btn-danger', 'btn-outline');
  }
}

/**
 * 1-Click sample loader for rapid testing by hackathon evaluators
 */
function loadSampleStory(sampleText) {
  const textarea = document.getElementById('experience_text');
  if (textarea && sampleText) {
    textarea.value = sampleText;
    textarea.focus();
    // Scroll smoothly to textarea
    textarea.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
}
