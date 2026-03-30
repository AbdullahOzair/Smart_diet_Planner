import re

new_ui = r"""                <!-- Goals View -->
                {% if view == 'goals' %}
                <div class="row align-items-center mb-4">
                    <div class="col-md-6">
                        <h2 class="h3 mb-0 text-gray-800"><i class="bi bi-bullseye text-primary me-2"></i>My Goals</h2>
                        <p class="text-muted mb-0">Track and achieve your health objectives</p>
                    </div>
                    <div class="col-md-6 text-md-end mt-3 mt-md-0">
                        <a href="{{ url_for('user_add_goal') }}" class="btn btn-primary shadow-sm" style="background-color: #2563EB; border:none;">
                            <i class="bi bi-plus-circle me-2"></i>Create New Goal
                        </a>
                    </div>
                </div>

                {% if goals and goals|length > 0 %}
                    {% for goal in goals %}
                    <div class="card border-0 shadow-sm rounded-4 mb-4 overflow-hidden">
                        <div class="card-body p-0">
                            <div class="row g-0">
                                <!-- LEFT CARD -->
                                <div class="col-lg-7 p-4 border-end-lg bg-white">
                                    <div class="d-flex justify-content-between align-items-center mb-3">
                                        <div class="d-flex align-items-center">
                                            <div class="icon-circle bg-primary bg-opacity-10 text-primary me-3" style="width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                                                <i class="bi {% if goal.goal_type == 'Weight Loss' %}bi-graph-down-arrow{% else %}bi-graph-up-arrow{% endif %} fs-4"></i>
                                            </div>
                                            <div>
                                                <h4 class="mb-0 fw-bold" style="color: #1a1a1a;">{{ goal.goal_type }}</h4>
                                                <span class="badge {% if goal.status == 'Active' %}bg-success{% elif goal.status == 'Completed' %}bg-primary{% else %}bg-secondary{% endif %} rounded-pill fw-normal mt-1">
                                                    <i class="bi bi-record-circle me-1"></i>{{ goal.status }}
                                                </span>
                                            </div>
                                        </div>
                                        <div class="text-end">
                                             <div class="fs-4 fw-bold text-dark" style="color: #1a1a1a;">{{ goal.current_value }}</div>
                                             <div class="text-muted small">Current (kg)</div>
                                        </div>
                                    </div>

                                    <div class="row mt-4">
                                        <div class="col-6">
                                            <div class="p-3 bg-light rounded-3">
                                                <div class="text-muted small mb-1"><i class="bi bi-calendar2-event me-1"></i>Start Date</div>
                                                <div class="fw-semibold" style="color: #1a1a1a;">{{ goal.start_date }}</div>
                                            </div>
                                        </div>
                                        <div class="col-6">
                                            <div class="p-3 bg-light rounded-3">
                                                <div class="text-muted small mb-1"><i class="bi bi-calendar-check me-1"></i>Target Date</div>
                                                <div class="fw-semibold" style="color: #1a1a1a;">{{ goal.target_date }}</div>
                                            </div>
                                        </div>
                                    </div>

                                    <div class="mt-4">
                                        <div class="d-flex justify-content-between mb-2">
                                             <span class="text-muted small">Progress: <strong class="text-primary">{{ goal.progress_pct|round(1) }}%</strong></span>
                                             <span class="text-muted small">Target: <strong class="text-dark" style="color: #1a1a1a;">{{ goal.target_value }} kg</strong></span>
                                        </div>
                                        <div class="progress" style="height: 10px;">
                                            <div class="progress-bar progress-bar-striped progress-bar-animated bg-primary" role="progressbar" style="width: {{ goal.progress_pct|round }}%; background-color: #2563EB !important;" aria-valuenow="{{ goal.progress_pct|round }}" aria-valuemin="0" aria-valuemax="100"></div>
                                        </div>
                                        <div class="d-flex justify-content-between mt-2 text-muted" style="font-size: 0.75rem;">
                                            <span>Start <strong>{{ goal.initial_weight }}kg</strong></span>
                                            <span>Target <strong>{{ goal.target_value }}kg</strong></span>
                                        </div>
                                    </div>
                                    
                                    <!-- Action Buttons -->
                                    <div class="d-flex gap-2 mt-4 pt-3 border-top">
                                        <button class="btn btn-outline-primary flex-grow-1" style="color:#2563EB; border-color:#2563EB;" onclick="showUpdateGoalModal({{ goal.goal_id }}, '{{ goal.goal_type }}', {{ goal.current_value }}, '{{ goal.target_value }}', '{{ goal.target_date }}')">
                                            <i class="bi bi-pencil-square me-2"></i>Update Goal
                                        </button>
                                        {% if goal.status == 'Active' %}
                                        <form action="{{ url_for('update_user_goal_status', goal_id=goal.goal_id) }}" method="POST" class="flex-grow-1" style="margin:0;">
                                            <button type="submit" class="btn btn-success w-100" style="background-color:#22C55E; color: white; border:none; padding:0.375rem 0.75rem;">
                                                <i class="bi bi-check2-all me-2"></i>Mark as Completed
                                            </button>
                                        </form>
                                        {% endif %}
                                    </div>
                                </div>

                                <!-- RIGHT PANEL (NEW 🔥) -->
                                <div class="col-lg-5 p-4 bg-light d-flex flex-column">
                                    <h5 class="fw-bold mb-3" style="color: #1a1a1a;"><i class="bi bi-lightbulb text-warning me-2"></i>Goal Insights</h5>
                                    
                                    <div class="card shadow-sm border-0 mb-3 border-start border-4 border-success">
                                        <div class="card-body py-2 px-3">
                                            <div class="d-flex justify-content-between align-items-center">
                                                <span class="text-muted small">Status</span>
                                                <span class="badge bg-success bg-opacity-10 text-success fw-bold px-2 py-1"><i class="bi bi-check-circle-fill me-1"></i>{{ goal.progress_status }}</span>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div class="row g-2 mb-4">
                                        <div class="col-6">
                                            <div class="card border-0 shadow-sm h-100">
                                                <div class="card-body p-3 text-center">
                                                    <div class="fs-3 mb-1">⚖️</div>
                                                    <h4 class="mb-0 fw-bold text-dark" style="color: #1a1a1a;">{{ goal.remaining_weight|round(1) }} <span class="fs-6 text-muted fw-normal">kg</span></h4>
                                                    <div class="text-muted" style="font-size: 0.75rem;">Remaining</div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="col-6">
                                            <div class="card border-0 shadow-sm h-100">
                                                <div class="card-body p-3 text-center">
                                                    <div class="fs-3 mb-1">📅</div>
                                                    <h4 class="mb-0 fw-bold text-dark" style="color: #1a1a1a;">{% if goal.status == 'Active' %}32{% else %}0{% endif %} <span class="fs-6 text-muted fw-normal">days</span></h4>
                                                    <div class="text-muted" style="font-size: 0.75rem;">Time Estimate</div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- AI SUGGESTION -->
                                    <div class="card border-0 flex-grow-1" style="background-color: #E0E7FF; color: #4338CA;">
                                        <div class="card-body">
                                            <h6 class="fw-bold"><i class="bi bi-robot me-2"></i>AI Recommendation</h6>
                                            <p class="small mb-3" style="color: #1a1a1a;">Based on your goal to reach {{ goal.target_value }}kg:</p>
                                            <ul class="small mb-3 ps-3" style="color: #1a1a1a;">
                                                <li>Consume ~1800 kcal/day.</li>
                                                <li>Focus on high-protein meals.</li>
                                                <li>Drink 2.5L water daily.</li>
                                            </ul>
                                            <a href="{{ url_for('user_diet') }}" class="btn btn-sm w-100 rounded-pill" style="background-color: #4F46E5; color: white; border:none; padding:0.375rem 0.75rem;">
                                                <i class="bi bi-stars me-1"></i>Generate Full Diet Plan
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                {% else %}
                    <div class="card border-0 shadow-sm rounded-4 text-center p-5" style="background: white;">
                        <div class="card-body">
                            <div class="display-1 text-muted mb-3"><i class="bi bi-target"></i></div>
                            <h4 class="text-dark fw-bold" style="color: #1a1a1a;">No Goals Yet</h4>
                            <p class="text-muted mb-4">Set your first health goal to start tracking your progress and get personalized AI recommendations.</p>
                            <a href="{{ url_for('user_add_goal') }}" class="btn btn-primary px-4 py-2 shadow-sm rounded-pill" style="background-color: #2563EB; border:none;">
                                <i class="bi bi-plus-circle me-2"></i>Create Your First Goal
                            </a>
                        </div>
                    </div>
                {% endif %}
                {% endif %}
"""

file_path = r'D:\7th semester\merge semester project\Smart_diet_Planner\SmartDietPlanner\flask_app\templates\user_dashboard.html'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace `<!-- Goals View -->` until the next `{% endif %}` that matches
new_text = re.sub(r'<!-- Goals View -->(.*?)(?=<!-- Add/Update Goal)', new_ui + '\n                ', text, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_text)

print('Replaced Successfully!')
