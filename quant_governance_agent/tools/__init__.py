from .research import RegisterResearchTool, RecordBacktestTool
from .governance import ValidateResearchTool, RequestApprovalTool

def default_tools(workspace):
    return [RegisterResearchTool(workspace), RecordBacktestTool(workspace), ValidateResearchTool(workspace), RequestApprovalTool(workspace)]
