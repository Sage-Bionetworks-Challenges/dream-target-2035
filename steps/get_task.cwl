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
- id: label
  type: string
expression: |2-

  ${
    // Step 1
    if (inputs.queue == "9615945") {
      return {
        synid: "syn66503497",
      };
    } 
    // Step 2
    else if (inputs.queue == "9615946") {
      return {
        synid: "syn123",  // TODO
      };
    } 
    else {
      throw 'invalid queue';
    }
  }
