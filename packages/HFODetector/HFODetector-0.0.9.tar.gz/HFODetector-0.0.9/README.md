# HFODetector
## RMS detector
#### Installation
`pip install HFODetector==0.0.9`

#### Example usage 
`test.py`
```
import numpy as np
from HFODetector.RMSDetector import RMS_detector

if __name__ == "__main__":
    edf_path = "example_edf.edf"
    detector = RMS_detector()
    channel_names, start_end = detector.predict_edf(edf_path)
    np.savez_compressed("test_results.npz", channels=channel_names, start_end=HFOs)
```
`python3 test.py` to generate `test_results.npz`

`test_results.npz` will contain the following:
- `start_end` : start and end timestamps of detected edfs ((N,2) array)
- `channel_names` : names of channels corresponding to the detected edfs ((N,) array)