# Evaluation for SLAM Challenge 2023

## Quick start
```
python3 batch_evaluation.py <path/to/submission> <path/to/output> <path/to/groundtruth> [option]
```

- `path/to/submission`: Folder containing your `.txt` trajectories in TUM format.
- `path/to/output`: Where CSV/PNG outputs are copied.
- `path/to/groundtruth`: Path to the groundtruth folder (for example: `../groundtruth_2023`).
- `option` (optional): Session mode selector:
	- `0`: Single session evaluation only
	- `1`: Multi session evaluation only
	- `2`: Single and multi session evaluation (default)

## Single pair evaluation
```
python3 evaluation.py <path/to/estimation.txt> <path/to/reference.txt>
```

This prints APE statistics and writes a plot to `test.png` in the current directory.

## Diagnostic tools
```
python3 track_trajectories.py <path/to/trajectory1> <path/to/trajectory2>
```

This compares two trajectories in a scatter plot for QA/inspection.

## Outputs
- `results_single.csv` and/or `results_multi.csv` with per-dataset metrics and totals.
- `score_single.png` and/or `score_multi.png` score tables.
- `combined_single.png` and/or `combined_multi.png` combined report images.
- Per-dataset trajectory/error plots (`*.png`) in the output folder.



