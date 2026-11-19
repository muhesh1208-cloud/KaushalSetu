/**
 * KaushalSetu - Assessor Practical Evaluation Calculator
 * Dynamically computes weighted practical checklist scores, viva-voce,
 * and safety compliance metrics to provide real-time assessment outcomes.
 */

document.addEventListener('DOMContentLoaded', () => {
  const scoreInputs = document.querySelectorAll('.nos-score-input');
  const vivaInput = document.getElementById('viva_score');
  const safetyInput = document.getElementById('safety_score');
  const decisionSelect = document.getElementById('decision');

  const livePracticalScoreEl = document.getElementById('livePracticalScore');
  const liveOverallScoreEl = document.getElementById('liveOverallScore');
  const liveDecisionBadgeEl = document.getElementById('liveDecisionBadge');

  function calculateScores() {
    let weightedChecklistSum = 0;
    let totalWeight = 0;

    scoreInputs.forEach(input => {
      const weight = parseFloat(input.getAttribute('data-weight')) || 20;
      const score = parseFloat(input.value) || 0;
      weightedChecklistSum += (score * weight);
      totalWeight += weight;

      // Update individual slider label if present
      const labelEl = document.getElementById(`val_${input.id}`);
      if (labelEl) {
        labelEl.textContent = `${score}%`;
      }
    });

    const practicalScore = totalWeight > 0 ? (weightedChecklistSum / totalWeight) : 0;
    const vivaScore = vivaInput ? (parseFloat(vivaInput.value) || 0) : 0;
    const safetyScore = safetyInput ? (parseFloat(safetyInput.value) || 0) : 0;

    // Formula: 50% Practical Demonstration + 30% Viva-voce + 20% Safety
    const overallScore = (practicalScore * 0.50) + (vivaScore * 0.30) + (safetyScore * 0.20);

    if (livePracticalScoreEl) {
      livePracticalScoreEl.textContent = practicalScore.toFixed(1) + '%';
    }
    if (liveOverallScoreEl) {
      liveOverallScoreEl.textContent = overallScore.toFixed(1) + '%';
    }

    // Auto-suggest decision based on NSQF RPL Benchmarks
    if (liveDecisionBadgeEl) {
      if (overallScore >= 70) {
        liveDecisionBadgeEl.className = 'badge badge-success';
        liveDecisionBadgeEl.textContent = 'Recommendation: COMPETENT';
        if (decisionSelect && !decisionSelect.dataset.userModified) {
          decisionSelect.value = 'Competent';
        }
      } else if (overallScore >= 50) {
        liveDecisionBadgeEl.className = 'badge badge-warning';
        liveDecisionBadgeEl.textContent = 'Recommendation: BRIDGE TRAINING';
        if (decisionSelect && !decisionSelect.dataset.userModified) {
          decisionSelect.value = 'Needs Bridge Training';
        }
      } else {
        liveDecisionBadgeEl.className = 'badge badge-danger';
        liveDecisionBadgeEl.textContent = 'Recommendation: RE-ASSESSMENT REQUIRED';
        if (decisionSelect && !decisionSelect.dataset.userModified) {
          decisionSelect.value = 'Rejected';
        }
      }
    }
  }

  // Attach event listeners
  scoreInputs.forEach(input => {
    input.addEventListener('input', calculateScores);
  });

  if (vivaInput) vivaInput.addEventListener('input', calculateScores);
  if (safetyInput) safetyInput.addEventListener('input', calculateScores);

  if (decisionSelect) {
    decisionSelect.addEventListener('change', () => {
      decisionSelect.dataset.userModified = 'true';
    });
  }

  // Initial calculation on page load
  calculateScores();
});
