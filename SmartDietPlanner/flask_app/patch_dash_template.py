import os

filepath = r'templates/user_dashboard.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

target = '''                                     </div>
                                 </div>
                             </div>
                         </div>
                     </div>
                 </div>

                 <!-- SECTION 2: Daily Nutrition Overview (PREMIUM MACROS VIEW) -->'''

replacement = '''                                     </div>
                                 </div>
                             </div>
                         </div>
                     </div>
                 </div>

                 <!-- NEW SECTION: MOOD INSIGHTS -->
                 <div class="row mb-4">
                     <div class="col-12">
                         <div class="card border-0 shadow-sm" style="border-radius:15px; overflow:hidden;">
                             <div class="card-header bg-white border-0 pt-4 pb-0 px-4 d-flex justify-content-between align-items-center">
                                 <h5 class="mb-0 fw-bold" style="color: #f39c12;"><i class="bi bi-stars text-warning me-2"></i>Mood Insights</h5>
                                 <a href="/user/dashboard?view=add_mood_log" class="btn btn-sm btn-outline-primary rounded-pill px-3">Log Mood</a>
                             </div>
                             <div class="card-body p-4">
                                 <div class="row g-4">
                                     <div class="col-md-5">
                                         <div class="p-3 h-100 rounded-3" style="background: #f8f9fa;">
                                             <h6 class="text-muted mb-3">Today's Vibe</h6>
                                             {% if today_mood %}
                                                 <div class="d-flex align-items-center mb-2">
                                                     <div class="display-4 me-3">
                                                         {% if today_mood[1] == 1 %}??{% elif today_mood[1] == 2 %}??{% elif today_mood[1] == 3 %}??{% elif today_mood[1] == 4 %}??{% elif today_mood[1] == 5 %}??{% else %}??{% endif %}
                                                     </div>
                                                     <div>
                                                         <h4 class="mb-0">{{ today_mood[1] }}/5</h4>
                                                         <span class="badge bg-secondary">Energy: {{ today_mood[2] }}</span>
                                                     </div>
                                                 </div>
                                                 {% if today_mood[5] %}<div class="small text-muted mt-2"><i class="bi bi-tags"></i> {{ today_mood[5] }}</div>{% endif %}
                                             {% else %}
                                                 <div class="text-center py-3 text-muted">
                                                     <i class="bi bi-emoji-neutral display-6 mb-2 d-block opacity-50"></i>
                                                     <p class="mb-0 small">No mood logged yet today.</p>
                                                 </div>
                                             {% endif %}
                                         </div>
                                     </div>
                                     <div class="col-md-7">
                                         <div class="p-3 h-100 rounded-3" style="background: #f8f9fa;">
                                             <h6 class="text-muted mb-3">Smart AI Insight</h6>
                                             <div class="d-flex">
                                                 <div class="me-3 text-primary"><i class="bi bi-lightbulb-fill fs-3"></i></div>
                                                 <div>
                                                     <p class="mb-1"><strong>{{ mood_insights }}</strong></p>
                                                     {% if weekly_mood %}
                                                     <div class="mt-3 small">
                                                         <span class="text-muted me-2">Recent Trend:</span>
                                                         {% for m in weekly_mood %}
                                                             <span title="{{ m[2].strftime('%a') }}: {{ m[0] }}/5" style="cursor:help">
                                                             {% if m[0] == 1 %}??{% elif m[0] == 2 %}??{% elif m[0] == 3 %}??{% elif m[0] == 4 %}??{% elif m[0] == 5 %}??{% else %}??{% endif %}
                                                             </span>
                                                         {% endfor %}
                                                     </div>
                                                     {% endif %}
                                                 </div>
                                             </div>
                                         </div>
                                     </div>
                                 </div>
                             </div>
                         </div>
                     </div>
                 </div>

                 <!-- SECTION 2: Daily Nutrition Overview (PREMIUM MACROS VIEW) -->'''

if target in content:
    content = content.replace(target, replacement)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Successfully patched user_dashboard.html')
else:
    print('Could not find target block.')
