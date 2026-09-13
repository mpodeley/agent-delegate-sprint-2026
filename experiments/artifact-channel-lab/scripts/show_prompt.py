"""Print complete initial messages and tool schemas; no model/network calls."""
import argparse,json
from inspect_ai.tool import ToolDef
from channel_lab.cli import ROOT
from channel_lab.attestation_policy import HELP
from channel_lab.attestation_setting import get_environment
from channel_lab.attestation_scoring import trusted_review
from channel_lab.worker_tools import worker_a_bash
from channel_lab.delegate import delegate_tool

p=argparse.ArgumentParser();p.add_argument('--delegate',action='store_true');args=p.parse_args()
env=get_environment();task=(ROOT/'environments/artifact_attestation/codebase/workers/TASK.md').read_text()
tools=[worker_a_bash()]
if args.delegate:tools.append(delegate_tool('worker-a',task,'unused',trusted_review))
submit=env.task_space().get(main_id='verify_receipt').main_task.submit_config.get_tool_def()
schemas=[{'name':d.name,'description':d.description,'parameters':d.parameters.model_dump(mode='json',exclude_none=True)} for d in [*[ToolDef(t) for t in tools],submit]]
print(json.dumps({'messages':[{'role':'system','content':env.description+(HELP if args.delegate else '')},{'role':'user','content':task}],'tools':schemas},indent=2))
