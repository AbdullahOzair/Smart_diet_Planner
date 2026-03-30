import re

with open('templates/user_dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

mood_old = r'<label class="form-label">Mood Rating \(1-5\)</label>\s*<select class="form-select" name="mood_rating" required \{\{ \'disabled\' if not has_daily_log else \'\' \}\}>\s*<option value="">Select your mood...</option>\s*<option value="5">.*?</option>\s*<option value="4">.*?</option>\s*<option value="3">.*?</option>\s*<option value="2">.*?</option>\s*<option value="1">.*?</option>\s*</select>'

mood_new = """<label class="form-label mt-3 mb-3"><b>How are you feeling?</b></label>
                                        <div class="d-flex justify-content-between mb-4 text-center emoji-selector">
                                            <label class="cursor-pointer" style="cursor:pointer;">
                                                <input type="radio" name="mood_rating" value="5" class="d-none" required {{ 'disabled' if not has_daily_log else '' }}>
                                                <div class="fs-1 emoji-btn">😄</div>
                                                <small class="text-muted fw-bold d-block mt-1 pt-1">Excellent</small>
                                            </label>
                                            <label class="cursor-pointer" style="cursor:pointer;">
                                                <input type="radio" name="mood_rating" value="4" class="d-none" {{ 'disabled' if not has_daily_log else '' }}>  
                                                <div class="fs-1 emoji-btn">😊</div>
                                                <small class="text-muted fw-bold d-block mt-1 pt-1">Good</small>
                                            </label>
                                            <label class="cursor-pointer" style="cursor:pointer;">
                                                <input type="radio" name="mood_rating" value="3" class="d-none" {{ 'disabled' if not has_daily_log else '' }}>  
                                                <div class="fs-1 emoji-btn">😐</div>
                                                <small class="text-muted fw-bold d-block mt-1 pt-1">Neutral</small>
                                            </label>
                                            <label class="cursor-pointer" style="cursor:pointer;">
                                                <input type="radio" name="mood_rating" value="2" class="d-none" {{ 'disabled' if not has_daily_log else '' }}>  
                                                <div class="fs-1 emoji-btn">😔</div>
                                                <small class="text-muted fw-bold d-block mt-1 pt-1">Low</small>
                                            </label>
                                            <label class="cursor-pointer" style="cursor:pointer;">
                                                <input type="radio" name="mood_rating" value="1" class="d-none" {{ 'disabled' if not has_daily_log else '' }}>  
                                                <div class="fs-1 emoji-btn">😢</div>
                                                <small class="text-muted fw-bold d-block mt-1 pt-1">Very Low</small>
                                            </label>
                                        </div>"""

triggers_html = """
                                    <div class="mb-4 mt-2">
                                        <label class="form-label mb-3"><b>What affected your mood today?</b></label>
                                        <div class="d-flex flex-wrap gap-2">    
                                            <div class="form-check p-0 m-0">    
                                                <input class="btn-check" type="radio" name="triggers" id="triggerWork" value="Work💼" {{ 'disabled' if not has_daily_log else '' }}>
                                                <label class="btn btn-outline-secondary rounded-pill" for="triggerWork">Work 💼</label>
                                            </div>
                                            <div class="form-check p-0 m-0">    
                                                <input class="btn-check" type="radio" name="triggers" id="triggerExercise" value="Exercise💪" {{ 'disabled' if not has_daily_log else '' }}>
                                                <label class="btn btn-outline-secondary rounded-pill" for="triggerExercise">Exercise 💪</label>
                                            </div>
                                            <div class="form-check p-0 m-0">    
                                                <input class="btn-check" type="radio" name="triggers" id="triggerSleep" value="Sleep😴" {{ 'disabled' if not has_daily_log else '' }}>
                                                <label class="btn btn-outline-secondary rounded-pill" for="triggerSleep">Sleep 😴</label>
                                            </div>
                                            <div class="form-check p-0 m-0">    
                                                <input class="btn-check" type="radio" name="triggers" id="triggerFood" value="Food🍔" {{ 'disabled' if not has_daily_log else '' }}>
                                                <label class="btn btn-outline-secondary rounded-pill" for="triggerFood">Food 🍔</label>
                                            </div>
                                            <div class="form-check p-0 m-0">    
                                                <input class="btn-check" type="radio" name="triggers" id="triggerSocial" value="Social👫" {{ 'disabled' if not has_daily_log else '' }}>
                                                <label class="btn btn-outline-secondary rounded-pill" for="triggerSocial">Social 👫</label>
                                            </div>
                                        </div>
                                    </div>"""

html_new2, count = re.subn(mood_old, mood_new + triggers_html, html)
print('Mood replaced:', count)

history_old = r'<h5 class="mb-1 text-primary"><i class="bi bi-emoji-smile"></i> \{\{ log\[3\] \}\}/5 Rating</h5>.*?<small class="text-muted"><i class="bi bi-clock"></i> \{\{ log\[2\] \}\}</small>.*?</div>.*?<div class="mb-2">.*?<strong>Triggers:</strong> \{\{ log\[4\] \}\}.*?</div>.*?<div class="p-2 bg-light rounded mt-2 border-start border-2 border-secondary small text-muted"><i class="bi bi-chat-left-text me-1"></i><em>\{\{ log\[5\] \}\}</em></div>'

history_new_html = """<h5 class="mb-1 text-primary"><i class="bi bi-emoji-smile"></i> {{ log[3] }}/5 Rating</h5>
                                        </div>
                                        <small class="text-muted"><i class="bi bi-clock"></i> {{ log[2] }}</small>
                                    </div>
                                    <div class="mt-3 mb-1 d-flex flex-wrap gap-2">
                                        {% if log[4] %}
                                        {% for trigger in log[4].split(',') %}
                                        <span class="badge bg-light text-dark border shadow-sm px-3 py-2 rounded-pill"><i class="bi bi-tag-fill me-1 text-secondary"></i>{{ trigger.strip() }}</span>
                                        {% endfor %}
                                        {% endif %}
                                        {% if log[6] %}
                                        <span class="badge bg-info text-dark shadow-sm px-3 py-2 rounded-pill"><i class="bi bi-activity me-1"></i>{{ log[6] }}</span>
                                        {% endif %}
                                    </div>
                                    {% if log[5] %}
                                    <div class="p-3 bg-light rounded-3 mt-3 border-start border-3 border-primary small text-muted"><i class="bi bi-quote fs-4 text-primary opacity-50 me-2"></i><em class="fs-6">{{ log[5] }}</em></div>
                                    {% endif %}"""

html_new3, hcount = re.subn(history_old, history_new_html, html_new2, flags=re.DOTALL)
print('History replaced:', hcount)

with open('templates/user_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_new3)
