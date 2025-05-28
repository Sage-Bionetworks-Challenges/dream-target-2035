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
- id: synid
  type: string
- id: task_number
  type: int
- id: hidden_annots
  type:
    type: array
    items: string

expression: |2-

  ${
    // Step 1
    if (inputs.queue == "9615945") {
      return {
        synid: "syn66503497",
        task_number: 1,
        hidden_annots: ["submission_errors","Clusters_Sel_200", "Clusters_Sel_500", "Hits_Sel_200", "Hits_Sel_500", "ClusterPRAUC_Sel_200", "ClusterPRAUC_Sel_500", "ROCAUC", "PRAUC", "P_value_Sel_200", "P_value_Sel_500"]
      };
    } 
    // Step 2
    else if (inputs.queue == "9615946") {
      return {
        synid: "syn66503497",
        task_number: 2,
        hidden_annots: ["submission_errors", "ROCAUC", "PRAUC", "Clusters_Sel_50", "Hits_Sel_50", "ClusterPRAUC_Sel_50", "P_value_Sel_50"]
      };
    } 
    else {
      throw 'invalid queue';
    }
  }
