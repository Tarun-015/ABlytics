# ABlytics

ABlytics is an A/B testing and experiment analytics platform built with
Python and Streamlit.

## Modes

### Manual Analysis

Users enter Variant A and Variant B data manually.

### Historical Comparison

Users connect Google Analytics 4 and compare two historical date ranges.

### True A/B Experiment

Users connect Google Analytics 4 and analyze experiment variants.

## Architecture

```text
Streamlit UI
      |
      v
Configuration
      |
      v
Validation
      |
      v
StandardDataset
      |
      +----------------+
      |                |
      v                v
   Analytics       Statistics
      |                |
      +-------+--------+
              |
              v
        Analysis Engine
              |
              v
          Dashboard