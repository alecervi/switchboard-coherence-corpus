This is the official repository of the Switchboard Coherence corpus (SWBD-Coh), described in the 2020 SIGDIAL paper:

    Cervone, A. and Riccardi, G. (2020) "Is this Dialogue Coherent? Learning from Dialogue Acts and Entities". In Proceedings of the 21st Annual SIGdial Meeting on Discourse and Dialogue.

SWBD-Coh is a resource of open-domain dialogues annotated with human coherence ratings at the turn level. More specifically, annotators were asked to rate a list of potential next turn candidates according to their coherence with a given context (dialogue history). The rating scale was:
- 1 = not coherent
- 2 = not sure it fits
- 3 = coherent

The resource consists of 1000 context * 7 next turn candidates = 7000 annotated context/candidate pairs.
The annotation has been performed using Amazon Mechanical Turk. Each turn has been annotated by 5 workers, selected after passing a pre-selection test (also on turn coherence rating).

# Getting started

## Download the Switchboard Dialogue Act (SWBD-DA) corpus

Download the Switchboard Dialogue Act corpus.
You can find a version of the Switchboard Dialogue Act corpus available for download here: https://web.stanford.edu/~jurafsky/swb1_dialogact_annot.tar.gz


## Build the resource

Clone our repository:
```
git clone https://github.com/alecervi/switchboard-coherence-corpus.git
```
The file coh_annotations.json in data contains the coherence annotations. However, in order to augment it with the textual part you need to run the build.py script:
```
python build.py
```

# JSON format

The data structure of SWBD-Coh (in json format) is:

```
{
    "<example_id>": 
    {
        "candidates": 
        [
            {
                "cand_type": <cand_type>,
                "avg_score": <avg score>
            }
        ], 
        "context": 
        [
            {
                "speaker": <speaker>, 
                "turn": <turn>
            }
        ]
        "info":
        {
            "dialog_id": <dialog_id>, 
            "time_info": 
                        [
                            {
                                "ann_id": <ann_id>,
                                "time": <time>
                            }
                        ], 
            "candidates_info":
                                [
                                    {
                                        "cand_type": <cand_type>,
                                        "turn_idx": <turn_idx>, 
                                        "dialog_id": <dialog_id>, 
                                        "annotators_info":
                                                            [
                                                                {
                                                                    "ann_id": <ann_id>,
                                                                    "score": <score> 
                                                                }
                                                            ]
                                    }
                                ]
        }
    }
}
```

Where:
- example id: the id of that annotated example, consisting of 1 context, paired with 7 annotated next turn candidates
- candidates:
    - cand_type: the type of candidate, which can be either: original (where the turn was the original one following that context in the dialogue), internal_swap (a random turn from a subsequent part of the same dialogue), external_swap (a random turn from another dialogue)
    - turn: the next turn candidate text
    - avg_score: the coherence score of that next turn candidate obtained by averaging the scores of all 5 annotators
- context: the dialogue history formatted a sequence of speaker turns
    - speaker: either "A" or "B"
    - turn: the text of the speaker turn
- info:
    - dialog_id: the id of the source dialogue in SWBD-DA
    - time_info: per annotator annotation time information
        - ann_id: the id of the annotator
        - time: the time (in seconds) spent by the annotator on this example 
    - candidates_info: additional information for each next turn candidate
        - cand_type: the type of candidate (see previous cand_type)
        - turn_idx: the index of the turn in the source SWBD-DA dialogue
        - dialog_id: the id of the source dialogue in SWBD-DA
        - annotators_info:
            - ann_id: the id of the annotator
            - score: the score given by the annotator



# Citation

If you find our resource useful, please cite our work:

```
@inproceedings{cervone2020dialogue,
  title={Is this Dialogue Coherent? Learning from Dialogue Acts and Entities},
  author={Cervone, Alessandra and Riccardi, Giuseppe},
  booktitle={Proceedings of the 21st Annual SIGdial Meeting on Discourse and Dialogue},
  year={2020}
}
```


