import sys
sys.path.insert(0, './flask_app')
from app import get_user_health_metrics

metrics1 = get_user_health_metrics(1)
metrics2 = get_user_health_metrics(2)
print('User 1:', metrics1)
print('User 2:', metrics2)
