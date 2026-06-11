#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: ExpressionTool
label: Get goldstandard based on evaluationid

requirements:
- class: InlineJavascriptRequirement

inputs:
- id: queue
  type: string

outputs:
- id: ref_synid
  label: Synapse ID for reference IDs
  type: string
- id: gt_synid
  label: Synapse ID for groundtruth data (clusters JSON)
  type: string
- id: task_number
  type: int

expression: |2-

  ${
    // Step 1
    if (inputs.queue == "9619685") {
      return {
        gt_synid: "syn75383336",
        ref_synid: "syn75383338",
        task_number: 1,
      };
    } 
    // Step 2
    else if (inputs.queue in ["9619687", "9619686"]) {
      return {
        gt_synid: "syn75383335",
        ref_synid: "syn75383337",
        task_number: 2,
      };
    } 
    else {
      throw 'invalid queue';
    }
  }
