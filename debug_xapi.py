import sys
import os
sys.path.append(os.getcwd())
from etl_app.services.xapi_service import XAPIService
from etl_app.models.xapi_models import Statement

svc = XAPIService()
# Fetch more to be sure
stmts = svc.fetch_statements(limit=1000)
answered = [s for s in stmts if 'answered' in s.get('verb', {}).get('id', '').lower()]

print(f"Total statements: {len(stmts)}")
print(f"Total 'answered' statements: {len(answered)}")

if answered:
    for i, s_data in enumerate(answered[:5]):
        s = Statement(**s_data)
        print(f"--- Sample {i+1} ---")
        print(f"ID: {s.id}")
        print(f"Verb: {s.verb.id}")
        print(f"Object ID: {s.object.id}")
        print(f"Reg: {s.context.registration if s.context else 'None'}")
        if s.context and s.context.contextActivities:
            parent = s.context.contextActivities.parent
            if parent:
                print(f"Parent IDs: {[p.id for p in parent]}")
else:
    print("No answered statements found in the first 1000.")
