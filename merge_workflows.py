import json

with open('telecomiq_workflow.json', 'r', encoding='utf-8') as f:
    main_wf = json.load(f)

with open('proactive_care_workflow.json', 'r', encoding='utf-8') as f:
    proactive_wf = json.load(f)

# Update node IDs in proactive_wf to ensure uniqueness
for i, node in enumerate(proactive_wf['nodes']):
    node['id'] = f"proactive_node_{i}"
    # Move them lower on the canvas so they don't overlap with the existing nodes
    # The existing nodes are at y=0, let's put proactive ones at y=400
    if 'position' in node:
        node['position'][1] += 400

# Append nodes
main_wf['nodes'].extend(proactive_wf['nodes'])

# Append connections
if 'connections' not in main_wf:
    main_wf['connections'] = {}

for source_node, outgoing in proactive_wf.get('connections', {}).items():
    main_wf['connections'][source_node] = outgoing

with open('telecomiq_workflow_combined.json', 'w', encoding='utf-8') as f:
    json.dump(main_wf, f, indent=2, ensure_ascii=False)

print("Workflows combined successfully into telecomiq_workflow_combined.json")
