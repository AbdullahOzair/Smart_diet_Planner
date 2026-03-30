import re

with open('templates/user_dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

mood_ui_old = """<label class="form-label">Mood Rating (1-5)</label>
                                        <select class="form-select" name="mood_rating" required {{ 'disabled' if not has_daily_log else '' }}>
                                            <option value="">Select your mood...</option>
                                            <option value="5">?? Very Happy (5)</option>
                                            <option value="4">?? Happy (4)</option>
                                            <option value="3">?? Neutral (3)</option>
                                            <option value="2">?? Sad (2)</option>
                                            <option value="1">?? Very Sad (1)</option>
                                        </select>"""

mood_ui_new = """<label class="form-label mt-3 mb-3"><b>How are you feeling?</b></label>
                                        <div class="d-flex justify-content-between mb-4 text-center emoji-selector">
                                            <label class="cursor-pointer" style="cursor:pointer;">
                                                <input type="radio" name="mood_rating" value="5" class="d-none" required {{ 'disabled' if not has_daily_log else '' }}>
                                                <div class="fs-1 emoji-btn">??</div>
                                                <small class="text-muted fw-bold d-block mt-1 pt-1">Excellent</small>
                                            </label>
                                            <label class="cursor-pointer" style="cursor:pointer;">
                                                <input type="radio" name="mood_rating" value="4" class="d-none" {{ 'disabled' if not has_daily_log else '' }}>
                                                <div class="fs-1 emoji-btn">??</div>
                                                <small class="text-muted fw-bold d-block mt-1 pt-1">Good</small>
                                            </label>
                                            <label class="cursor-pointer" style="cursor:pointer;">
                                                <input type="radio" name="mood_rating" value="3" class="d-none" {{ 'disabled' if not has_daily_log else '' }}>
                                                <div class="fs-1 emoji-btn">??</div>
                                                <small class="text-muted fw-bold d-block mt-1 pt-1">Neutral</small>
                                            </label>
                                            <label class="cursor-pointer" style="cursor:pointer;">
                                                <input type="radio" name="mood_rating" value="2" class="d-none" {{ 'disabled' if not has_daily_log else '' }}>
                                                <div class="fs-1 emoji-btn">??</div>
                                                <small class="text-muted fw-bold d-block mt-1 pt-1">Low</small>
                                            </label>
                                            <label class="cursor-pointer" style="cursor:pointer;">
                                                <input type="radio" name="mood_rating" value="1" class="d-none" {{ 'disabled' if not has_daily_log else '' }}>
                                                <div class="fs-1 emoji-btn">??</div>
                                                <small class="text-muted fw-bold d-block mt-1 pt-1">Very Low</small>
                                            </label>
                                        </div>"""

if mood_ui_old in html:
    html = html.replace(mood_ui_old, mood_ui_new)
else:
    print('Mood UI old not found')

triggers_html = """
                                    <div class="mb-4 mt-2">
                                        <label class="form-label mb-3"><b>What affected your mood today?</b></label>
                                        <div class="d-flex flex-wrap gap-2">
                                            <div class="form-check p-0 m-0">
                                                <input class="btn-check" type="radio" name="triggers" id="triggerWork" value="Work??" {{ 'disabled' if not has_daily_log else '' }}>
                                                <label class="btn btn-outline-secondary rounded-pill" for="triggerWork">Work ??</label>
                                            </div>
                                            <div class="form-check p-0 m-0">
                                                <input class="btn-check" type="radio" name="triggers" id="triggerExercise" value="Exercise??" {{ 'disabled' if not has_daily_log else '' }}>
                                                <label class="btn btn-outline-secondary rounded-pill" for="triggerExercise">Exercise ??</label>
                                            </div>
                                            <div class="form-check p-0 m-0">
                                                <input class="btn-check" type="radio" name="triggers" id="triggerSleep" value="Sleep??" {{ 'disabled' if not has_daily_log else '' }}>
                                                <label class="btn btn-outline-secondary rounded-pill" for="triggerSleep">Sleep ??</label>
                                            </div>
                                            <div class="form-check p-0 m-0">
                                                <input class="btn-check" type="radio" name="triggers" id="triggerFood" value="Food??" {{ 'disabled' if not has_daily_log else '' }}>
                                                <label class="btn btn-outline-secondary rounded-pill" for="triggerFood">Food ??</label>
                                            </div>
                                            <div class="form-check p-0 m-0">
                                                <input class="btn-check" type="radio" name="triggers" id="triggerSocial" value="Social??" {{ 'disabled' if not has_daily_log else '' }}>
                                                <label class="btn btn-outline-secondary rounded-pill" for="triggerSocial">Social ??</label>
                                            </div>
                                        </div>
                                    </div>"""

notes_html = """<div class="mb-3">
                                        <label class="form-label">Notes (Optional)</label>"""
if triggers_html not in html:
    html = html.replace(notes_html, triggers_html + '\n                                    ' + notes_html)

emoji_css = """<style>
.emoji-btn { transition: transform 0.2s, filter 0.2s; cursor: pointer; filter: grayscale(100%) opacity(0.6); }
.emoji-btn:hover { filter: grayscale(50%) opacity(0.8); transform: scale(1.1); }
input[type="radio"]:checked + .emoji-btn { transform: scale(1.3); filter: grayscale(0%) opacity(1); }
input[type="radio"]:checked ~ small { color: #f39c12 !important; }
</style>
"""
if 'emoji-btn' not in html:
    html = html.replace('</head>', emoji_css + '</head>', 1)

history_old = """                                    {% for log in mood_logs %}
                                    <div class="mood-log-item mb-3 p-3 border rounded">
                                        <div class="d-flex justify-content-between align-items-center mb-2">
                                            <h6 class="mb-0">{{ log[1] }}</h6>
                                            <span class="badge bg-warning text-dark">{{ log[2] }}</span>
                                        </div>
                                        <div class="mb-2">
                                            <small class="text-muted">     
                                                <i class="bi bi-bar-chart"></i> Stress: <strong>{{ log[3] }}/10</strong> |
                                                <i class="bi bi-lightning"></i> Energy: <strong>{{ log[4] }}/10</strong>
                                            </small>
                                        </div>
                                        {% if log[5] %}
                                        <p class="mb-0 small"><em>{{ log[5] }}</em></p>
                                        {% endif %}"""

history_new = """                                    {% for log in mood_logs %}
                                    <div class="mood-log-item mb-3 p-3 border rounded border-start border-4 border-warning">
                                        <div class="d-flex justify-content-between align-items-center mb-2">
                                            <h6 class="mb-0">{{ log[1] }}</h6>
                                            <span class="badge bg-warning text-dark px-2 py-1 fs-6">
                                                {% if log[2] == 5 %}?? Excellent{% elif log[2] == 4 %}?? Good{% elif log[2] == 3 %}?? Neutral{% elif log[2] == 2 %}?? Low{% else %}?? Very Low{% endif %}
                                            </span>
                                        </div>
                                        <div class="mb-2 d-flex flex-wrap gap-2">
                                            <span class="badge bg-light text-dark shadow-sm">? Energy: {{ log[4] }}/10</span>
                                            <span class="badge bg-light text-dark shadow-sm">?? Stress: {{ log[3] }}/10</span>
                                            {% if log[6] %}
                                            <span class="badge bg-info text-dark shadow-sm"><i class="bi bi-tag-fill me-1"></i>{{ log[6] }}</span>
                                            {% endif %}
                                        </div>
                                        {% if log[5] %}
                                        <div class="p-2 bg-light rounded mt-2 border-start border-2 border-secondary small text-muted"><i class="bi bi-chat-left-text me-1"></i><em>{{ log[5] }}</em></div>
                                        {% endif %}"""

if history_old in html:
    html = html.replace(history_old, history_new)
else:
    print('History old not found')

with open('templates/user_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('UI Updated Successfully')
