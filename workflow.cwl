#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
label: First DREAM Target 2035 Drug Discovery Challenge evaluation workflow

requirements:
  - class: StepInputExpressionRequirement

inputs:
  adminUploadSynId:
    label: Synapse Folder ID accessible by an admin
    type: string
  submissionId:
    label: Submission ID
    type: int
  submitterUploadSynId:
    label: Synapse Folder ID accessible by the submitter
    type: string
  synapseConfig:
    label: filepath to .synapseConfig file
    type: File
  workflowSynapseId:
    label: Synapse File ID that links to the workflow
    type: string
  organizersId:
    label: User or team ID for challenge organizers
    type: string
    default: "3535713"
  private_annotations:
    label: List of annotation keys to set as private (not visible to submitters)
    type: string[]
    default: []

outputs: []

steps:
  01_organizers_log_access:
    doc: >
      Give challenge organizers `download` permissions to the submission logs folder
    run: |-
      https://raw.githubusercontent.com/Sage-Bionetworks/ChallengeWorkflowTemplates/v4.1/cwl/set_permissions.cwl
    in:
      - id: entityid
        source: "#submitterUploadSynId"
      - id: principalid
        source: "#organizersId"
      - id: permissions
        valueFrom: "download"
      - id: synapse_config
        source: "#synapseConfig"
    out: []

  02_download_submission:
    doc: Download submission
    run: |-
      https://raw.githubusercontent.com/Sage-Bionetworks/ChallengeWorkflowTemplates/v4.1/cwl/get_submission.cwl
    in:
      - id: submissionid
        source: "#submissionId"
      - id: synapse_config
        source: "#synapseConfig"
    out:
      - id: filepath
      - id: entity_id
      - id: entity_type
      - id: evaluation_id
      - id: results

  03_get_task_entities:
    doc: Get goldstandard and label based on task number
    run: steps/get_task.cwl
    in:
      - id: queue
        source: "#02_download_submission/evaluation_id"
    out:
      - id: gt_synid
      - id: ref_synid
      - id: task_number

  04_download_groundtruth:
    doc: Download groundtruth file (clusters JSON)
    run: |-
      https://raw.githubusercontent.com/Sage-Bionetworks-Workflows/cwl-tool-synapseclient/v1.4/cwl/synapse-get-tool.cwl
    in:
      - id: synapseid
        source: "#03_get_task_entities/gt_synid"
      - id: synapse_config
        source: "#synapseConfig"
    out:
      - id: filepath

  04_download_reference_ids:
    doc: Download reference file (catalog IDs)
    run: |-
      https://raw.githubusercontent.com/Sage-Bionetworks-Workflows/cwl-tool-synapseclient/v1.4/cwl/synapse-get-tool.cwl
    in:
      - id: synapseid
        source: "#03_get_task_entities/ref_synid"
      - id: synapse_config
        source: "#synapseConfig"
    out:
      - id: filepath

  05_score:
    doc: Score predictions file
    run: steps/score.cwl
    in:
      - id: entity_type
        source: "#02_download_submission/entity_type"
      - id: input_file
        source: "#02_download_submission/filepath"
      - id: groundtruth
        source: "#04_download_groundtruth/filepath"
      - id: reference
        source: "#04_download_reference_ids/filepath"
      - id: task_number
        source: "#03_get_task_entities/task_number"
    out:
      - id: results
      - id: status
      
  06_send_score_results:
    doc: Send email of the scores to the submitter
    run: steps/email_score.cwl
    in:
      - id: submissionid
        source: "#submissionId"
      - id: synapse_config
        source: "#synapseConfig"
      - id: results
        source: "#05_score/results"
      - id: private_annotations
        source: "#private_annotations"
    out: [finished]

  06_add_score_annots:
    doc: >
      Update `submission_status` and add the scoring metric annotations
    run: |-
      https://raw.githubusercontent.com/Sage-Bionetworks/ChallengeWorkflowTemplates/v4.1/cwl/annotate_submission.cwl
    in:
      - id: submissionid
        source: "#submissionId"
      - id: annotation_values
        source: "#05_score/results"
      - id: to_public
        default: true
      - id: force
        default: true
      - id: synapse_config
        source: "#synapseConfig"
    out: [finished]

  07_check_score_status:
    doc: >
      Check the scoring status of the submission; if 'INVALID', throw an
      exception so that final status is 'INVALID' instead of 'ACCEPTED'
    run: |-
      https://raw.githubusercontent.com/Sage-Bionetworks/ChallengeWorkflowTemplates/v4.1/cwl/check_status.cwl
    in:
      - id: status
        source: "#05_score/status"
      - id: previous_annotation_finished
        source: "#06_add_score_annots/finished"
      - id: previous_email_finished
        source: "#06_send_score_results/finished"
    out: [finished]
 
s:author:
- class: s:Person
  s:identifier: https://orcid.org/0000-0002-5622-7998
  s:email: verena.chung@sagebase.org
  s:name: Verena Chung

s:codeRepository: https://github.com/Sage-Bionetworks-Challenges/dream-target-2035
s:license: https://spdx.org/licenses/Apache-2.0

$namespaces:
  s: https://schema.org/
