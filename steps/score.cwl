#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
label: Score predictions file

requirements:
- class: InlineJavascriptRequirement

inputs:
- id: input_file
  type: File
- id: groundtruth
  type: File
- id: task_number
  type: int
- id: check_validation_finished
  type: boolean?

outputs:
- id: results
  type: File
  outputBinding:
    glob: results.json
- id: status
  type: string
  outputBinding:
    glob: results.json
    outputEval: $(JSON.parse(self[0].contents)['submission_status'])
    loadContents: true

baseCommand: /usr/local/bin/score.py
arguments:
- prefix: -p
  valueFrom: $(inputs.input_file)
- prefix: -g
  valueFrom: $(inputs.groundtruth.path)
- prefix: -o
  valueFrom: results.json
- prefix: -t
  valueFrom: $(inputs.task_number)

hints:
  DockerRequirement:
    dockerPull: docker.synapse.org/syn65660836/evaluation:v2.0.0

s:author:
- class: s:Person
  s:identifier: https://orcid.org/0000-0002-5622-7998
  s:email: verena.chung@sagebase.org
  s:name: Verena Chung

s:codeRepository: https://github.com/Sage-Bionetworks-Challenges/dream-target-2035
s:license: https://spdx.org/licenses/Apache-2.0

$namespaces:
  s: https://schema.org/